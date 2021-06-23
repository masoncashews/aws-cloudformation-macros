import json
import boto3
import urllib3
import uuid

http = urllib3.PoolManager()
elbv2Client = boto3.client('elbv2')
SUCCESS = "SUCCESS"
FAILED = "FAILED"

def handler(event, context):
  #Globals
  try:
    physicalResourceID = event.get('PhysicalResourceId', str(uuid.uuid4()))
    
    #Short circuit deletes
    if event['RequestType'] == 'Delete':
      sendResponse(event, context, responseStatus=SUCCESS, responseData=None, physicalResourceID=physicalResourceID)
    
    listenerRules = elbv2Client.describe_rules(ListenerArn=event['ResourceProperties']['ListenerArn'])
    
    rulePriorities = list(filter(lambda s: s.isdecimal(), [r['Priority'] for r in listenerRules['Rules']]))
    
    newPriority = int(max(rulePriorities, default=1))+1

    #Just in case there were rules deleted, it's better to go through and fill back in the gaps
    #If there are no gaps, it will default out to the last one.
    for rulePriority in range(1, newPriority):
      if not str(rulePriority) in rulePriorities:
        newPriority = rulePriority
        break

    sendResponse(event, context, SUCCESS, {"Priority": newPriority}, physicalResourceID)
  
  except Exception as e:
    print(e)
    return {
        sendResponse(event, context, responseStatus=FAILED if event['RequestType'] != 'Delete' else SUCCESS, responseData=None, physicalResourceID=None)
    }

def sendResponse(event, context, responseStatus, responseData=None, physicalResourceID=None):
  responseBody = {
    'Status': responseStatus,
    'Reason': 'See the details in CloudWatch Log Stream: ' + context.log_stream_name,
    'PhysicalResourceId': physicalResourceID,
    'StackId': event['StackId'],
    'RequestId': event['RequestId'],
    'LogicalResourceId': event['LogicalResourceId'],
    'Data': responseData,
  }

  jsonResponseBody = json.dumps(responseBody)

  responseHeaders = {
    'content-type': '',
    'content-length': str(len(jsonResponseBody))
  }

  response = http.request('PUT',url=event['ResponseURL'], headers=responseHeaders, body=jsonResponseBody.encode('utf-8'))
