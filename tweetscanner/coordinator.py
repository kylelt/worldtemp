from threading import Thread
from preprocessing import TweetProcessor
import queue

class TweetCoordinator(Thread):
    def __init__(self, queue_len=10000, worker_threads=2, worker_sleep_time_sec=0.2):
        self.in_queue = queue.Queue(queue_len)
        self.worker_threads = worker_threads
        self.worker_sleep_time_sec = worker_sleep_time_sec
        self.workers = []
        print("coord start up")
        self.working = False

    def put_tweet(self, tweet):
        try:
            self.in_queue.put(tweet)
        except Exception:
            print("queue put failed")


    def start_work(self):
        self.working = True
        for i in range(self.worker_threads):
            control_queue = queue.Queue(1)
            worker = Thread(target=TweetProcessor, args=(self.in_queue, control_queue, self.worker_sleep_time_sec))
            self.workers.append({'thread': worker, 'state_control_queue': control_queue})
            print("start worker")
            worker.start()

    def stop_work(self):
        """ Send a lets stop message to everybody """ 
        for i in self.workers:
            i['state_control_queue'].put('stop')
        
        for i in self.workers:
            i['thread'].join(i)

        self.working = False