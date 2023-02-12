# yaml2mongo

Program to load documents in yaml format into a mongo database.

## Usage

```bash
usage: yaml2mongo.py [-h] -f FILENAME -c COLLECTION -d DATABASE [-k KEY]
                     [-u USERNAME] [-p PASSWORD] [--uri URI]

Load Yaml files into MongoDB collections

options:
  -h, --help            show this help message and exit
  -f FILENAME, --filename FILENAME
                        The name of Yaml file
  -c COLLECTION, --collection COLLECTION
                        The name of the collection do load the file into
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