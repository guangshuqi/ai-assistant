import boto3

dyndb = boto3.resource('dynamodb', 'us-east-2')
table = dyndb.Table('conversations')

def get_conversation(thread_id):
    print(thread_id)
    response = table.get_item(Key={'thread_id': str(thread_id)})
    if 'Item' in response:
        return response['Item']
    else:
        return None
    
def update_conversation(thread_id, conversation):
    table.put_item(Item=conversation)

def create_conversation(thread_id, conversation):
    table.put_item(Item={'thread_id': str(thread_id), 'conversation': conversation})