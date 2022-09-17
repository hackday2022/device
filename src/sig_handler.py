import signal


class SigHandler:
    killed = False

    def __init__(self):
        signal.signal(signal.SIGINT, self.set_kill)
        signal.signal(signal.SIGTERM, self.set_kill)

    def set_kill(self, *args):
        self.killed = True
