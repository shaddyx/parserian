import random
import threading

import requests
from bs4 import BeautifulSoup


class UserAgentRoller:

    def __init__(self, auto_fetch=True):
        self.user_agents = []
        self.auto_fetch = auto_fetch
        self.lock = threading.RLock()

    def add(self, user_agent):
        self.user_agents.append(user_agent)

    def next(self):
        with self.lock:
            if not len(self.user_agents) and self.auto_fetch:
                self.fetch()
            return random.choice(self.user_agents)

    def fetch(self):
        res = requests.get("https://www.useragentstring.com/pages/Browserlist/")
        soup = BeautifulSoup(res.text, "html.parser")
        res = soup.select("li a")
        for k in res:
            self.add(k.text)