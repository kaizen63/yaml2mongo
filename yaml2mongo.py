import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from bson import ObjectId
import yaml
import pathlib
import argparse

import logging
from pymongo.errors import ConnectionFailure, OperationFailure
from urllib.parse import quote_plus
from setup_logging import setup_logging
from read_config import read_config
from timer import Timer


class AuthenticationFailedError(Exception):
    pass


def update_database(collection: Collection, document: dict, search_keys: list[str]) -> tuple[ObjectId, bool]:
    """
    Updates or inserts a document into a collection
    Args:
        collection: The collection to insert/update
        document:  The document to insert
        search_keys: The search search_keys to find a document in a collection

    Returns:
        Tuple: (_id, True if updated, False if inserted)
    """
    logger = logging.getLogger(__name__)
    search_values = {}
    for k in search_keys:
        search_values[k] = document[k]

    try:
        find_result: dict = collection.find_one_and_update(search_values, {'$set': document})
        if not find_result:
            inserted_id = collection.insert_one(document).inserted_id
            return inserted_id, False
        else:
            return find_result['_id'], True
    except OperationFailure as err:
        logger.exception(f'Operation failed {err}')
        auth_failed = 8000
        if err.code == auth_failed:
            raise AuthenticationFailedError(err)
        raise
    except Exception as err:
        logger.exception(f'failed {err}')
        raise


def read_yaml(filename: pathlib.Path) -> dict:
    """
    Loads a yaml file and returns the dict of it
    Args:
        filename: Yaml file

    Returns:
        Dictionary containing the yaml file
    """
    with open(filename) as p:
        file_content: dict = yaml.load(p, Loader=yaml.SafeLoader)
    return file_content


def load_document(collection: Collection, document: dict, search_keys: list) -> tuple[ObjectId, int]:
    """
    Loads a document into a collection
    Args:
        collection: The collection to load into
        document: The document as a dictionary
        search_keys: The search key to identify a document

    Returns:
        Tuple: _id, True if updated, False if inserted
    """
    logger = logging.getLogger(__name__)
    try:
        document_id, updated = update_database(collection, document, search_keys)
    except AuthenticationFailedError as err:
        logger.error(err)
        raise
    except Exception as err:
        logger.exception(f'Failed to load: {document}. Error: {err}')
        raise

    return document_id, updated


def load_collection(filename: pathlib.Path, collection: Collection, search_keys: list) -> dict:
    """
    Loads a yaml file into a collection
    Args:
        filename: The Yaml file
        collection: The collection
        search_keys: The search keys to identify a document

    Returns:
        Dictionary with following keys: total, inserted, updated
    """
    yaml_docs = read_yaml(filename)
    insert_count = update_count = 0

    for yaml_doc in yaml_docs:
        _, updated = load_document(collection, yaml_doc, search_keys)
        if updated:
            update_count += 1
        else:
            insert_count += 1

    return {'total': len(yaml_docs), 'inserted': insert_count, 'updated': update_count}


def main():
    """Load a yaml file into a mongodb database"""

    load_dotenv('.env', override=False)
    setup_logging()
    logger = logging.getLogger(__name__)
    config = read_config(pathlib.Path(pathlib.Path(__file__).name).with_suffix('.toml'))
    if not config:
        logger.debug('No configuration.')

    parser = argparse.ArgumentParser(description='Load Yaml files into MongoDB collections')
    parser.add_argument('-f', '--filename', help='The name of Yaml file', required=True)
    parser.add_argument('-c', '--collection', help='The name of the collection to load the file into', required=True)
    parser.add_argument('-d', '--database', help='The database to load the file into', required=True)
    parser.add_argument('-k', '--key', help='The unique key(s) of the document. Multiple -k possible',
                        action='append', required=True)
    parser.add_argument('-u', '--username', help='The mongodb username. Default: env variable MONGODB_USERNAME',
                        default=os.getenv('MONGODB_USERNAME'))
    parser.add_argument('-p', '--password', help='The mongodb password. Default: env variable MONGODB_PASSWORD',
                        default=os.getenv('MONGODB_PASSWORD'))
    parser.add_argument('--uri', help='The mongodb uri. Default: env variable MONGODB_URI',
                        default=os.getenv('MONGODB_URI'))

    args = parser.parse_args()
    commandline_args = {k: v for k, v in vars(args).items() if v}

    filename = commandline_args.get('filename')
    database = commandline_args.get('database')
    collection = commandline_args.get('collection')
    keys = commandline_args.get('key')
    username = commandline_args.get('username')
    password = commandline_args.get('password')
    mongodb_uri = commandline_args.get('uri')

    if not mongodb_uri:
        logger.error(f'Please provide MONGODB_URI env variable or --uri commandline arg')
        raise SystemExit(1)

    if '{username}' in mongodb_uri:
        mongodb_uri = mongodb_uri.replace('{username}', quote_plus(username))

    if '{password}' in mongodb_uri:
        mongodb_uri = mongodb_uri.replace('{password}', quote_plus(password))

    with Timer(logger=logger.info):
        try:
            client = MongoClient(host=mongodb_uri, tz_aware=True, connect=True)
        except ConnectionFailure as err:
            logger.exception(f'Cannot connect to mongo: {err}')
            raise SystemExit(1)

        db: Database = client[database]
        statistics = load_collection(pathlib.Path(filename).resolve(), db[collection], keys)
        logger.info(
            f'{filename}: total docs: {statistics["total"]}, updated: {statistics["updated"]}, inserted: {statistics["inserted"]}')


if __name__ == '__main__':
    main()
