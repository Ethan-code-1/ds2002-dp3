import boto3
from botocore.exceptions import ClientError
import requests
import json

# Set up your SQS queue URL and boto3 client
url = "https://sqs.us-east-1.amazonaws.com/440848399208/ebo4dq"
sqs = boto3.client('sqs')
myMessageStorage = {}

def delete_message(handle):
    try:
        # Delete message from SQS queue
        sqs.delete_message(
            QueueUrl=url,
            ReceiptHandle=handle
        )
        print("Message deleted")
    except ClientError as e:
        print(e.response['Error']['Message'])

def get_message():
    try:
        # Receive message from SQS queue. Each message has two MessageAttributes: order and word
        # You want to extract these two attributes to reassemble the message
        response = sqs.receive_message(
            WaitTimeSeconds = 19, 
            QueueUrl=url,
            AttributeNames=[
                'All'
            ],
            MaxNumberOfMessages=10,
            MessageAttributeNames=[
                'All'
            ], 
            VisibilityTimeout = 100
            #https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_ReceiveMessage.html 
        )
        # Check if there is a message in the queue or not
        if "Messages" in response:

            numberOfMessages = len(response['Messages'])

            print("There are: " , numberOfMessages)

            for i in range(0, numberOfMessages):
                #print("This is message", i)
                
                order = response['Messages'][i]['MessageAttributes']['order']['StringValue']
                word = response['Messages'][i]['MessageAttributes']['word']['StringValue']
                handle = response['Messages'][i]['ReceiptHandle']

                #print("It has an order of " + order + " and it says: " + word)
                myMessageStorage[order] = word 

            # extract the two message attributes you want to use as variables
            # extract the handle for deletion later
            print(myMessageStorage)
            '''
            order = response['Messages'][0]['MessageAttributes']['order']['StringValue']
            word = response['Messages'][0]['MessageAttributes']['word']['StringValue']
            handle = response['Messages'][0]['ReceiptHandle']

            # Print the message attributes - this is what you want to work with to reassemble the message
            print(f"Order: {order}")
            print(f"Word: {word}")
            ''' 
        # If there is no message in the queue, print a message and exit    
        else:
            print("No message in the queue")
            exit(1)
            
    # Handle any errors that may occur connecting to SQS
    except ClientError as e:
        print(e.response['Error']['Message'])

# Trigger the function
if __name__ == "__main__":
    get_message()