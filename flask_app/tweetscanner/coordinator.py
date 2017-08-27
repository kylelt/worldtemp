from threading import Thread
import threading
from preprocessing import TweetProcessor
import logging
from multiprocessing import Process, Queue

class TweetCoordinator:
    def __init__(self, queue_len=10000, worker_threads=4, worker_sleep_time_sec=0.1):
        self.in_queue = Queue(queue_len)
        self.worker_threads = worker_threads
        self.worker_sleep_time_sec = worker_sleep_time_sec
        self.workers = []
        self.working = False
        self.sent = Sentinel()

    def put_tweet(self, tweet):
        try:
            self.in_queue.put(tweet)
        except Exception:
            print("queue put failed")
            self.stop_work()

    def show_thread_count(self):
        print(multiprocessing.active_count())

    def start_work(self):
        print("starting workers")
        self.working = True
        for i in range(self.worker_threads):
            control_queue = Queue(1)
            worker= TweetProcessor(self.in_queue, self.worker_sleep_time_sec, self.sent)
            worker.start()

    def stop_work(self):
        print("stopping workers")
        self.sent.stop()

class Sentinel():
    def __init__(self):
        self.run_thread = True

    def is_running(self):
        return self.is_running

    def stop(self):
        self.is_running = False