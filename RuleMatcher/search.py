# from ltp import LTP
import jieba
from py2neo import Graph
import os
import re
import threading

env_list = os.environ
address = env_list.get('post_address', "0.0.0.0")
graphIP = env_list.get('graph_ip', "neo4j://neoforj.zhinengwenda-test.svc.cluster.hz:30665")
username = env_list.get('graph_username', "neo4j")
password = env_list.get('graph_password', "mercy-france-collect-gong-window-7317")

os.environ["DJANGO_SETTINGS_MODULE"] = "gwcomments.settings"
curr_dir = os.path.dirname(os.path.abspath(__file__))
# wordfilter_path = os.path.join(curr_dir, rule + ".txt")

class ruleLoader:
    def __init__(self, rule, dict):
        self.rule_path = os.path.join(curr_dir, "rule/" + rule + ".txt")
        with open(self.rule_path, encoding='utf-8') as f:
            self.lines = f.read().splitlines()[0:4]
        print(self.lines)
        self.dict = dict

    def create_qrl(self):
        slots = self.lines[0][7:].split(',')
        qrl = self.lines[1][5:]
        for slot in slots:
            print(slot + " : " + self.dict[slot])
            qrl = qrl.replace("[???]", self.dict[slot], 1)
            print(qrl)
        return qrl

    def response(self, state=True, answer=""):
        if state:
            rep = self.lines[2][9:]
        else:
            rep = self.lines[3][6:]
        rep = rep.replace("[???]", answer)
        return rep

class QABot:
    def __init__(self):
        # self.classifier = SiwiClassifier()
        # self.actions = SiwiActions()
        # self.connection_pool = connection_pool
        self.gap_time = 10800
        self.graph = Graph(graphIP, auth=(username, password))
        self.reconnect()

    def query(self, rule, dict):

        loader = ruleLoader(rule, dict)
        qrl = loader.create_qrl()
        result = self.graph.run(qrl)
        result = list(set(result))
        answer = ""
        for record in result:
            if answer != "":
                answer += ','
            answer += record[0]

        # intent = self.classifier.get(sentence)  # <--- a.
        # action = self.actions.get(intent)       # <--- b.
        return loader.response(answer != "", answer)


    # def vehical_exist(self, num):
    #     qrl = 'match (vehical:车辆) where vehical.name = "' + num + '" return vehical.name'
    #     result = self.graph.run(qrl)
    #     for line in result:
    #         return True
    #     return False

    def reconnect(self):
        reconnect_to_graph_timer = threading.Timer(self.gap_time, self.reconnect)
        print("Reconnect to neo4j database as " + username)
        self.graph = Graph(graphIP, auth=(username, password))
        reconnect_to_graph_timer.start()

    def disconnect(self):
        return 0


# class find_roadnum:
#     def __init__(self):


if __name__ == "__main__":
    bot = QABot()
    ans = bot.query("search_for_driver", {"车牌号": "桂B11555"})
    print(ans)
    # loader = ruleLoader("search_for_driver", {"车牌号": "桂B12345"})
    # print(loader.create_qrl())
    # print(loader.response(True))
