import jieba
from py2neo import Graph
import os
import re
import threading

os.environ["DJANGO_SETTINGS_MODULE"] = "gwcomments.settings"
curr_dir = os.path.dirname(os.path.abspath(__file__))





class InsertRule:
    def __init__(self, ruleName):
        self.rule_path = os.path.join(curr_dir, "rule/" + ruleName + ".txt")
        self.ruleName = ruleName

    @staticmethod
    def is_slot(slot, all_slots):
        return slot in all_slots

    def create(self, ruleInfo):
        with open(self.rule_path, "w") as file:
            slots = ruleInfo.get('slots', '').split(',')
            for slot in slots:
                if self.is_slot(slot, all_slots):

            file.write()