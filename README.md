# yaml2mongo

Program to load documents in yaml format into a mongo database.

## Usage

```bash
usage: yaml2mongo.py [-h] -c COLLECTION -d DATABASE -k KEY [-u USERNAME]
                     [-p PASSWORD] [--uri URI]
                     filename [filename ...]

Load Yaml files into MongoDB collection

positional arguments:
  filename              The name of Yaml file

options:
  -h, --help            show this help message and exit
  -c COLLECTION, --collection COLLECTION
                        The name of the collection to load the file into
  -d DATABASE, --database DATABASE
                        The database to load the file into
  -k KEY, --key KEY     The unique key(s) of the document. Multiple -k
                        possible
  -u USERNAME, --username USERNAME
                        The mongodb username. Default: env variable
                        MONGODB_USERNAME
  -p PASSWORD, --password PASSWORD
                        The mongodb password. Default: env variable
                        MONGODB_PASSWORD
  --uri URI             The mongodb uri. Default: env variable MONGODB_URI

```