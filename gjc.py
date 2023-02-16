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


# 解析器，用于解析问题中的意图
# 返回包含主题词，问题词，问题焦点等在内的问题意图
class Resolver:
    def __init__(self):
        self.model = 'jieba'
        # self.ltp = LTP()

    # 解析问题
    def resolve_question(self, text):
        # 先交给ltp模型处理，主要获得分词的词性和语法依存关系
        # output = self.ltp.pipeline([text], tasks=["cws", "pos", "ner", "srl", "dep", "sdp"])
        # output = self.ltp.pipeline([text], tasks=["cws"])
        # seg = output.cws[0]
        # pos = output.pos[0]
        # srl = output.srl
        # sdp = output.sdp
        seg = jieba.cut(text, cut_all=False)

        # 依据词性，找到问题的动词和主题词
        # qverb = None
        # for i in range(len(seg)):
        #     p = pos[i]
        #     if p is "v":
        #         qverb = seg[i]
        #         break

        # 根据预定义的关键词，找到问题的问题词是什么以及位置
        # keywords = ["路线", "什么", "谁"]
        # qwords = []
        # for i in range(len(seg)):
        #     word = seg[i]
        #     for key in keywords:
        #         if word.__contains__(key):
        #             qwords.append((word, i))
        #
        # # 依据语义角色关系，确定问题的主题词
        # qtopics = []
        # for line in srl:
        #     if len(line) != 0:
        #         for role in line:
        #             role_name = role['predicate']
        #             role_content = role['arguments'][0][1] + role['arguments'][1][1]
        #             test = True
        #             for key in keywords:
        #                 test = True
        #                 if role_content.__contains__(key):
        #                     test = False
        #                     break
        #             if test:
        #                 qtopics.append((role_content, role_name))

        # 确定问题的问题焦点

        return {"intent": "find_roadnum", "seg": seg}


class QABot:
    def __init__(self):
        # self.classifier = SiwiClassifier()
        # self.actions = SiwiActions()
        # self.connection_pool = connection_pool
        self.resolver = Resolver()
        self.gap_time = 3600
        self.graph = Graph(graphIP, auth=(username, password))
        self.reconnect()

    def query(self, sentence):
        res = self.resolver.resolve_question(sentence)
        intent = res['intent']
        seg = res['seg']
        pattern = '([桂]{1}[A-Z]{1}[A-Z0-9]{5})'
        m = re.search(pattern, sentence)
        if m == None:
            return "对不起，我还需要更多的学习，暂时无法理解您的问题。"

        num = m.groups()[0]
        # for word in seg:
        #     print(word + '/ ')
        #     if(word[0] == '桂'):
        #         num = word
        # if num == "":
        #     return "no record"
        if not self.vehical_exist(num):
            return "对不起，您输入的车牌号非法或数据库中无对应车牌记录。"

        qrl = 'match (person:人员) -[r:驾驶]->(vehical:车辆) where vehical.name = "' + num + '" return person.name'
        print(qrl)
        result = self.graph.run(qrl)
        answer = ""
        for record in result:
            if answer != "":
                answer += ','
            answer += record[0]

        # intent = self.classifier.get(sentence)  # <--- a.
        # action = self.actions.get(intent)       # <--- b.
        if answer == "":
            return "对不起，记录中暂时没有任何人驾驶过车辆" + num
        else:
            return "驾驶过车辆" + num + "的司机有:" + answer  #action.execute(self.connection_pool)

    def vehical_exist(self, num):
        qrl = 'match (vehical:车辆) where vehical.name = "' + num + '" return vehical.name'
        result = self.graph.run(qrl)
        for line in result:
            return True
        return False

    def reconnect(self):
        reconnect_to_graph_timer = threading.Timer(self.gap_time, self.reconnect)
        print("Reconnect to neo4j database as " + username)
        self.graph = Graph(graphIP, auth=(username, password))
        reconnect_to_graph_timer.start()


# class find_roadnum:
#     def __init__(self):


if __name__ == "__main__":
    bot = QABot()
    answer = bot.query("有哪些人驾驶过桂B11555公交车？")
    print(answer)
