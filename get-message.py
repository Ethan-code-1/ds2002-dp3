import boto3
from botocore.exceptions import ClientError
import requests
import json

# Set up your SQS queue URL and boto3 client
url = "https://sqs.us-east-1.amazonaws.com/440848399208/ebo4dq"
sqs = boto3.client('sqs')

#My gloabl vars
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
        #Fetch messages until the message storage has a length of 10
        #Was done because on queues less than a 1,000 items you sometimes may not get all items back in one request even when asking for 10: https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_ReceiveMessage.html
        while(len(myMessageStorage) != 10): 

            #WaitTimeSeoncds added to ensure message do not return blank incase some network lag
            response = sqs.receive_message(
                WaitTimeSeconds = 3, 
                QueueUrl=url,
                AttributeNames=[
                    'All'
                ],
                MaxNumberOfMessages=10,
                MessageAttributeNames=[
                    'All'
                ], 
            )

            # Check if there is a message in the queue or not
            if "Messages" in response:

                numberOfMessages = len(response['Messages'])

                #print("There are: " , numberOfMessages)

                for i in range(0, numberOfMessages):
                    
                    order = response['Messages'][i]['MessageAttributes']['order']['StringValue']
                    word = response['Messages'][i]['MessageAttributes']['word']['StringValue']
                    handle = response['Messages'][i]['ReceiptHandle']

                    myMessageStorage[order] = word 
                    delete_message(handle)
          
            # If there is no message in the queue, print a message and exit    
            else:
                print("No message in the queue")
                exit(1)

        #Code gets to this point once we have the 10 unique messages

        hiddenMessage = ""
        for i in range(0, 10):
            hiddenMessage += myMessageStorage[str(i)]
            if i != 9:
                hiddenMessage += ' '

        print("The secret phrase is: ")
        print(hiddenMessage)
            
    # Handle any errors that may occur connecting to SQS
    except ClientError as e:
        print(e.response['Error']['Message'])

# Trigger the function
if __name__ == "__main__":
    get_message()