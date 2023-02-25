import jieba
from py2neo import Graph
import os
import re
import threading

os.environ["DJANGO_SETTINGS_MODULE"] = "gwcomments.settings"
curr_dir = os.path.dirname(os.path.abspath(__file__))


def load_all_slots():
    slots_path = os.path.join(curr_dir, "slots.txt")
    all_slots = []
    with open(slots_path, mode='r', encoding='utf8') as file:
        return file.read().splitlines()


