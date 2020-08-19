import json
import time
import urllib
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
    start = time.time()
    urllib.request.urlopen(url)
    queue.enque(time.time() - start)


def post_test(event, context):
    urls = event
    durations = {}
    for url in urls:
        t = Thread(target=get_duration, args=(url, ))
        t.start()
        t.join()
        duration = queue.dequeue()
        durations[url] = duration
    response = {
        "statusCode": 200,
        "body": json.dumps(durations)
    }
    return response
