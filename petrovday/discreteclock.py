import threading
import time
import collections

class DiscreteClock:
  def __init__(self, current_time=0):
    self.current_time = current_time
    self.mutex = threading.Lock()
    self.conditions = collections.defaultdict(lambda: threading.Condition(self.mutex))

  def wait_until(self, wakeup, timeout=None):
    with self.mutex:
      if wakeup <= self.current_time:
        return True
    with self.conditions[wakeup]:
      self.conditions[wakeup].wait(timeout=timeout)

  def tick(self):
    with self.mutex:
      self.current_time += 1
      self.conditions[self.current_time].notify_all()
      del self.conditions[self.current_time]

  def start(self):
    t0 = time.monotonic()
    def tick_forever():
      while True:
        now = time.monotonic()
        then = t0 + self.current_time + 1
        if then > now:
          time.sleep(then-now)
        self.tick()
    threading.Thread(target=tick_forever, daemon=True).start()
