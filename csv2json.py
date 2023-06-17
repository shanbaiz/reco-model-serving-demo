import csv
import json

csvFilePath = './ml-latest-small/ratings.csv'
jsonFilePath = './ml-latest-small/ratings.json'

# Read CSV file and convert to a list of dictionaries
with open(csvFilePath, 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    rows = list(reader)

# Write JSON data to file
with open(jsonFilePath, 'w') as jsonfile:
    jsonfile.write(json.dumps(rows))
    print('Conversion complete!')