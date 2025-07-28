import json
from awsConfig import sqs, SQS_QUEUE_URL

def pollSQS():
    response = sqs.receive_message(
        QueueUrl = SQS_QUEUE_URL,
        MaxNumberOfMessages = 1,
        WaitTimeSeconds = 10
    )

    messages = response.get("Messages", [])
    if not messages:
        return None, None
    
    message = messages[0]
    receipt_handle = message["ReceiptHandle"]
    body = json.loads(message["Body"])

    return body, receipt_handle