# reco-model-serving-demo
This is a demo project to serve a basic movie recommeding model using docker and AWS services including S3, ECR, Lambda function, API Gateway and DynamoDB.  It supports real-time predict, as well as retrain upon request.

![Project Flowchart](https://github.com/shanbaiz/reco-model-serving-demo/blob/main/reco-model-demo-flowchart.png)

### Public data source
http://files.grouplens.org/datasets/movielens/ml-latest-small.zip

### Prerequisite
AWS Account
AWS CLI
Docker
requirements.txt

### Usage
1. Upload the data to your S3 bucket, feel free to change the bucket name to yours in lambda_function.py
2. Build and push the image to AWS ECR, then load the image with Lambda function. Please note I used a M1 Mac to build the image and remember to choose Arm64 when you load the image in this case.
3. (Optional) If you want to test it without using api calls, please uncomment the lambda_handler() under #Use for Lambda testing
4. Create a new API using AWS API Gateway, and you can test it with Postman. Sample test case: {"UID":1}
5. To make it more practical, we can read user rating data from DynamoDB. Create a new table in DynamoDB and use RecordNo(Number) as the partition key.
6. Run csv2json.py and dynamo_upload.py.
7. Uncomment the load_feature() under #Use this if loading data from Amazon DynamoDB
8. Rebuild image and update image in lambda function
9. Test with another api call. Example: curl -X POST "<YOUR API PATH>/predict" -H "Content-Type:application/json"  -d '{"UID":2}'
