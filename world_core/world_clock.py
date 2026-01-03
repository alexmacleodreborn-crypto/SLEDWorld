def tick(self):
    import time

    if not self.started:
        self.start()
        return

    now = time.time()

    if self.last_time is None:
        self.last_time = now
        return

    delta = now - self.last_time
    self.last_time = now
    self.seconds_elapsed += delta