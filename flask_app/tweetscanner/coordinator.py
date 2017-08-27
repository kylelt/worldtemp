from threading import Thread
import threading
from preprocessing import TweetProcessor
import logging
from multiprocessing import Process, Queue, active_children

class TweetCoordinator:
    """
        Manages the worker processes that handle a torrent of tweets
        from the twitter api
    """
    def __init__(self, queue_len=0, worker_threads=4, worker_sleep_time_sec=0.1):
        """
            :param queue_len Queue the maximum length the input queue can be before it blocks
            :param worker_threads
            :pram worker_threads how many threads (processes) to spawn
            :param worker_sleep_time how long a worker should sleep after processing a tweet
        """
        self.in_queue = Queue(queue_len)
        self.worker_threads = worker_threads
        self.worker_sleep_time_sec = worker_sleep_time_sec
        self.workers = []
        self.working = False
        self.sent = Sentinel()

    def put_tweet(self, tweet):
        """
            push a dict tweet into the queue to be processed by our worker threads
        """
        try:
            self.in_queue.put(tweet)
        except Exception:
            print("queue put failed")
            self.stop_work()

    def show_thread_count(self):
        """
            :return list of active threads
        """
        print(active_children())

    def start_work(self):
        """
            Starts all the worker threads that process tweets incomming from
            self.in_queue
        """
        print("starting workers")
        self.working = True
        for i in range(self.worker_threads):
            control_queue = Queue(1)
            worker= TweetProcessor(self.in_queue, self.worker_sleep_time_sec, self.sent)
            worker.start()

    def stop_work(self):
        """
            send a stop signal the worker processes
        """
        print("stopping workers")
        self.sent.stop()

class Sentinel():
    """
        Wrapper around a boolean flag
    """

    def __init__(self):
        self.run_thread = True

    def is_running(self):
        return self.is_running

    def stop(self):
        self.is_running = False