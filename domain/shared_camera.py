import threading
import time

MIN_PERIOD = 1
COOLDOWN_SEC = 2
COOLDOWN_DECREASE_SEC = 0.0333 * 5

class SharedCamera:
    def __init__(self, video_capture):
        self.cap = video_capture
        self.frame = None
        self.lock = threading.Lock()
        self.running = True
        self.last_minute_frame = int(time.time())
        self.curr_period = 1
        self.thread = threading.Thread(target=self._update, daemon=True)
        self.thread.start()

    def _update(self):
        while self.running:
            if int(time.time()) - self.last_minute_frame > COOLDOWN_SEC:
                self.last_minute_frame = int(time.time())
                print(f"Cooldown {self.curr_period}")
                self.curr_period = min(self.curr_period + COOLDOWN_DECREASE_SEC, MIN_PERIOD)
            ret, frame = self.cap.read()
            if ret:
                with self.lock:
                    self.frame = frame
            time.sleep(self.curr_period)  # Prevent CPU overuse

    def get_frame(self, target_period_sec: float):
        with self.lock:
            self.curr_period = min(target_period_sec, self.curr_period)
            return self.frame.copy() if self.frame is not None else None

    def stop(self):
        self.running = False
        self.thread.join()
        self.cap.release()
