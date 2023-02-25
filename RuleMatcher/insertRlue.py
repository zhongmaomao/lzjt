import jieba
from py2neo import Graph
import os
import re
import threading
import NLU
import json

os.environ["DJANGO_SETTINGS_MODULE"] = "gwcomments.settings"
curr_dir = os.path.dirname(os.path.abspath(__file__))



class RuleInserter:
    def __init__(self):
        self.all_slots = NLU.load_all_slots()
        self.curr_dir = curr_dir

    def is_slot(self, slot):
        return slot in self.all_slots

    def get_path(self, ruleInfo):
        ruleName = ruleInfo.get('ruleName', '未命名')
        return os.path.join(self.curr_dir, "rule/" + ruleName + ".txt")

    def create(self, ruleInfo):
        rule_path = self.get_path(ruleInfo)

        slots_line = "slots: "
        slots = ruleInfo.get('slots', '').split(',')
        is_first_slot = False
        for slot in slots:
            if self.is_slot(slot):
                if is_first_slot:
                    slots_line += ','
                is_first_slot = True
                slots_line += slot
            else:
                return "槽位不存在！添加失败！"

        qrl_line = "qrl: " + ruleInfo.get('qrl', '')
        success_line = "success: " + ruleInfo.get('success', '')
        fail_line = "fail: " + ruleInfo.get('fail', '')
        with open(rule_path, "w") as file:
            file.write(slots_line + '\n')
            file.write(qrl_line + '\n')
            file.write(success_line + '\n')
            file.write(fail_line + '\n\n')

        return "添加规则：" + ruleInfo.get('ruleName', '未命名')

    def append(self, example):
        rule_path = self.get_path(example)
        example_line = example.get('example', '')
        if example_line != '':
            example_line += '\n'
            with open(rule_path, "a") as file:
                file.write(example_line)
        return "添加示例：" + example.get("ruleName", '未命名')



if __name__ == "__main__":
    inserter = RuleInserter()
    ruleinfo = {"ruleName":"test_RuleName", "slots":"slot1,slot2,slot3", "qrl":"test_qrl", "success":"test_success", "fail":"test_fail"}
    inserter.create(ruleinfo)
    for i in range(5):
        inserter.append({"ruleName":"test_RuleName", "example":"example" + str(i)})
    # loader = ruleLoader("search_for_driver", {"车牌号": "桂B12345"})
    # print(loader.create_qrl())
    # print(loader.response(True))