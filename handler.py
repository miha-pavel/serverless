import json
import boto3
import time
import urllib


def post_test(event, context):
    urls = event
    durations = {}
    for url in urls:
        start = time.time()
        urllib.request.urlopen(url)
        duration = time.time() - start
        durations[url] = duration
    response = {
        "statusCode": 200,
        "body": json.dumps(durations)
        }
    return response