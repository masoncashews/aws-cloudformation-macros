def handler(event, context):
  #Globals
  params = event['params']
  requestId = event['requestId']
  try:
    fragmentItems=[{}]
    for subnet in params['AllowCidrs']:
      for tcpport in params['AllowPorts']:
          fragmentItems.append({'IpProtocol':'tcp', 'FromPort':tcpport,'ToPort':tcpport,'CidrIp':subnet})
  
    return {
        'requestId': requestId,
        'status': 'SUCCESS',
        'fragment': list(filter(None, fragmentItems)) #have to do the list because the way I initialize causes a leading empty dictionary in the list.
    }
  except Exception as e:
    print(event)
    print(e)
    return {
        'requestId': requestId,
        'status': 'FAILURE',
        'fragment': ''
    }