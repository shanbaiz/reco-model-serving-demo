import boto3
import json

TABLE_NAME = 'reco-model-ratings'

session=boto3.Session()
dynamodb = boto3.resource('dynamodb', region_name='us-east-2')

# get a reference to the table
table = dynamodb.Table(TABLE_NAME)

# load data from JSON file
with open('./ml-latest-small/ratings.json') as f:
    data = json.load(f)

count=0
# insert each record into the table
for item in data:
    item['RecordNo'] = count
    table.put_item(Item=item)
    count+=1