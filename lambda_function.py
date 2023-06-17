import json
import pandas as pd
import pickle
from surprise import Dataset, Reader
from datetime import datetime
import boto3
from io import BytesIO

# Define path constants 
BUCKET_NAME = 'wcd-serverless-demo'
PREDICT_PATH = '/predict'
RETRIN_PATH = '/retrain'
MODEL_PREFIX = 'models/'
DATA_PATH = 'data/ratings.csv'


def load_model():
    s3 = boto3.client('s3')
    bucket_name = BUCKET_NAME
    prefix = MODEL_PREFIX

    paginator = s3.get_paginator('list_objects_v2')
    result_iterator = paginator.paginate(Bucket=bucket_name, Prefix=prefix)
    pkl_files = [obj['Key'] for result in result_iterator for obj in result.get('Contents', []) if obj['Key'].endswith('.pkl')]

    latest_file = max(pkl_files, key=lambda x: s3.head_object(Bucket=bucket_name, Key=x)['LastModified'])


    obj = s3.get_object(Bucket=bucket_name, Key=latest_file)
    model_bytes = obj['Body'].read()

    model = pickle.loads(model_bytes)

    return model

def load_feature():
    s3 = boto3.client('s3')

    # Download the CSV file from S3
    bucket_name = BUCKET_NAME
    key = DATA_PATH
    obj = s3.get_object(Bucket=bucket_name, Key=key)
    # body = obj.get()['Body'].read().decode('utf-8')

    df = pd.read_csv(BytesIO(obj['Body'].read()))

    return df


def predict(user_id, n_recommendations=5):
    my_model = load_model()
    df = load_feature()

    rated_items = df[df['userId'] == user_id]['movieId'].tolist()

    # create a list of tuples representing the unrated items and their predicted ratings
    unrated_items = [(item_id, my_model.predict(user_id, item_id).est) for item_id in df['movieId'].unique() if item_id not in rated_items]

    # sort the list by predicted rating and return the top N recommendations
    unrated_items.sort(key=lambda x: x[1], reverse=True)
    recommendations = [x[0] for x in unrated_items[:n_recommendations]]
    return recommendations 


def re_train():
    model = load_model()
    df = load_feature()

    reader = Reader(rating_scale=(1, 5))
    data = Dataset.load_from_df(df[['userId', 'movieId', 'rating']], reader)

    model.fit(data.build_full_trainset())

    model_bytes = pickle.dumps(model)

    now  = datetime.now()
    dt_string = now.strftime("%Y%d%m%H%M")

    s3 = boto3.client('s3')
    bucket_name = BUCKET_NAME
    key_name = MODEL_PREFIX + 'model_' + dt_string + '.pkl'
    s3.put_object(Bucket=bucket_name, Key=key_name, Body=model_bytes)

# Use for lambda testing
# def lambda_handler(event, context):
#     if event['Action'] == 'predict':
#         user_id = event['UID']
#         recommendations = predict(user_id)
#         move_ids = [int(x) for x in recommendations]
#         res = {"recommanded movie ID" : move_ids}
#         return res

#     elif event['Action'] == 're-train':

#         re_train()

#         return "model retrained"
#     else:
#         return "Invalid parameter"


def lambda_handler(event, context):
    if event['rawPath'] == PREDICT_PATH:
        decodedEvent = json.loads(event['body'])
        user_id = decodedEvent['UID']
        recommendations = predict(user_id)
        move_ids = [int(x) for x in recommendations]
        res = {"recommanded movie ID" : move_ids}
        return res

    elif event['rawPath'] == RETRIN_PATH:

        re_train()

        return "Model retrained"
    else:
        return "Invalid parameter"
    

    

