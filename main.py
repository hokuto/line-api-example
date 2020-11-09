from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import os

app = Flask(__name__)

line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))


@app.route("/callback", methods=['POST', 'GET'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@app.route("/", methods=['GET'])
def index():
    return hello_world(request)

def hello_world(request):
    to = 'h_yamada'

    try:
        # line_bot_api.push_message(to, TextSendMessage(text='Hello World!'))
        line_bot_api.broadcast(TextSendMessage(text='Hello World!'))
        print("------------ push_message succeeded ------------")
        return 'OK'
    except Exception as e:
        print("------------ ERROR ------------")
        print(e)
        return 'ERROR'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

if __name__ == "__main__":
    app.run(debug=True)
    print(hello_world(1))
