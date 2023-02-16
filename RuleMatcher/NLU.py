import jieba
from py2neo import Graph
import os
import re
import threading

os.environ["DJANGO_SETTINGS_MODULE"] = "gwcomments.settings"
curr_dir = os.path.dirname(os.path.abspath(__file__))


class Slots:
    def __init__(self):
        self.slot_path = os.path.join(curr_dir, "rule/" + ruleName + ".txt")