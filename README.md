# sw-dept-pubs

Script to read Esploro asset data from a JSON file and extract recent publications with a given dept/unit afiliation. Results are in a JSON file for use by a web application.

## Setup

Github action triggers on cron defined in actions.yml, to run main.py.

## Requirements

Environment variables:

- JSON_URL: The location of the Esploro asset data in another repo
- PAT: Personal asset token issued by the repo hosting the Esploro data to allow private connection to retrieve data.
- BASE_URL

Packages:

- Python 3.9
- requests
