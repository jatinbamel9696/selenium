import boto3
import sys
from botocore.exceptions import ClientError

# Initialize the DynamoDB client
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')  # Adjust region as needed
table_name = 'MyDynamoDBTable'

def insert_request_id(request_id):
    table = dynamodb.Table(table_name)

    # Define the item to insert
    item = {
        'RequestID': request_id  # Assuming 'RequestID' is your primary key
    }

    try:
        # Insert item using put_item
        response = table.put_item(Item=item)
        print(f"Request ID inserted successfully: {response}")
    except ClientError as e:
        print(f"Failed to insert request ID: {e.response['Error']['Message']}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python dynamodb_insert_request_id.py <request_id>")
        sys.exit(1)

    request_id = sys.argv[1]
    insert_request_id(request_id)
