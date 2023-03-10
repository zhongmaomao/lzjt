from flask import Flask, request, Response, jsonify
import filter.filter as Filter
import os
from gjc import QABot

app = Flask(__name__)
env_list = os.environ

address = env_list.get('post_address', "0.0.0.0")
graphIP = env_list.get('graph_ip', "neo4j://neoforj.zhinengwenda-test.svc.cluster.hz:30665")
username = env_list.get('graph_username', "neo4j")
password = env_list.get('graph_password', "mercy-france-collect-gong-window-7317")

@app.route('/api/lzjt-zhinengwenda/')
def hello():
    return 'Hello! Here is lzjt-zhinengwenda system.'

# @app.route('/register', methods=['POST'])
# def register():
#     print(request.headers)
#     # print(request.stream.read()) # 不要用，否则下面的form取不到数据
#     print(request.form)
#     print(request.form.get('name', default='username'))
#     return 'welcome'
#

# @app.route('/add', methods=['POST'])
# def add():
#     result = {'sum': request.json['a'] + request.json['b']}
#     # resp = Response(json.dumps(result), mimetype='application/json')
#     # resp.headers.add('Server', 'python flask')
#     # return resp
#     return jsonify(result)


@app.route("/api/lzjt-zhinengwenda/kgqa", methods=["GET"])
def kgqa():
    # request_data = request.json
    # question = request_data['question']  # <----- 1.
    question = request.args.get('question', '')
    question = filter_part.words_replace(question)
    if question:
        answer = bot.query(question)   # <----- 2.
        if answer != "no record":
            msg = "查询成功"
        else:
            msg = "查询无结果"
        code = '1'
    else:
        answer = "Sorry, what did you say?"
        msg = "查询失败"
        code = '0'
    res = {'code': code,
           'msg': msg,
           'question': question,
           'answer': answer
           }
    return jsonify(res)


if __name__ == '__main__':
    bot = QABot()
    filter_part = Filter.ac_automation()
    app.config['JSON_AS_ASCII'] = False
    app.run(host=address, port=5000, debug=False)
