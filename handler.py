from json import loads, dumps
from time import time
from urllib import request
from threading import Thread


global queue

class Queue:
    def __init__(self):
        self.item = []

    def enque(self, item):
        """
        Insert the elements in queue
        :param item: Any
        :return: Bool
        """
        self.item.insert(0, item)
        return True

    def dequeue(self):
        """
        Return the elements that came first
        :return: Any
        """
        if len(self.item) == 0:
            return None
        else:
            return self.item.pop()


queue = Queue()


def get_duration(url):
    try:
        start = time()
        request.urlopen(url)
        result = time() - start
    except:
        message = f"The {url} was not found"
        result = {
            "statusCode": 404,
            "message": message
        }
    queue.enque(result)


def post_test(event, context):
    urls = loads(event["body"])
    durations = {}
    response = {
        "statusCode": 400,
        "body": {"message": "The urls list is empty"}
    }
    if urls:
        for url in urls:
            t = Thread(target=get_duration, args=(url, ))
            t.start()
            t.join()
            duration = queue.dequeue()
            durations[url] = duration
        response_body = dumps(durations)
        response = {
            "statusCode": 200,
            "body": response_body
        }
    return response
