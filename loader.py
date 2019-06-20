
from queue import Queue, Full
import random
import threading
import time
import numpy as np

class Loader():

  def __init__(self, filenames, capacity, processor, num_threads=1, randomize=False, augment=False):
    self.filenames = filenames
    self.data_queue = Queue(capacity)
    self.randomize = randomize
    self.threads = []
    self.augment = augment
    self.processor = processor
    for i in range(num_threads):
      worker = threading.Thread(target=self.worker)
      worker.daemon = True
      self.threads.append(worker)
    self.done = False


  def start(self):
    for worker in self.threads:
      worker.start()
  

  def stop(self):
    self.done = True
    for worker in self.threads:
      worker.join()


  def get_batch(self, size):
    batch = []
    for i in range(size):
      elt = self.data_queue.get()
      batch.append(elt)
    return list(map(list, zip(*batch)))


        
  def worker(self):
    #range_min = 0
    #range_max = len(self.filenames)
    t = threading.currentThread()
    idx = 0

    while True:
      if self.done: return

      if not self.data_queue.full():
        filename = self.filenames[0]
        try:
          item = self.processor(filename, self)
          self.data_queue.put_nowait(item)
        except Full:
          pass
        except Exception as e:
          pass
          print(e)
      else:
        time.sleep(1)
