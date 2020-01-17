from flask import Flask, request, jsonify
from flask_cors import CORS

from chatbot import ChatBot
from main import init
from utils import get_parser
from utils import MODEL_PATH_MAP

app = Flask(__name__)
CORS(app)
argss = get_parser().parse_args()
# print(argss)
argss.model_name_or_path = MODEL_PATH_MAP[argss.model_type]
init(argss)
chatBot = ChatBot()

@app.route("/api", methods=["GET"])
def api():
    query = request.args.get('query')
    print(query)

    resp = chatBot.main(query)

    return jsonify(
        query=query, answer=resp[0], doSearch=resp[1], searchQuery=resp[2]
    )


if __name__ == '__main__':
    app.run()
