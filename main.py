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
import json

app = Flask(__name__)

line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))
print('---------------------------------------- app started')
app.logger.info('---------------------------------------- app started')

@app.route("/callback", methods=['POST', 'GET'])
def callback():
    print('---------------------------------------- callback')
    app.logger.info('---------------------------------------- callback')

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


@app.route("/phone_number_push", methods=['GET'])
def phone_number_push(request):
    to = '9e483b827f1b0b2e4b627b03ffdffa0da910ba4d3e21fa9f85dffa759afcc929'
    messages = TextSendMessage(text='pnp test')
    send_phone_number_push(to, messages)

def send_phone_number_push(to, messages, delivery_tag=None, notification_disabled=False, timeout=None):
    if not isinstance(messages, (list, tuple)):
        messages = [messages]

    if delivery_tag:
        self.headers['X-Line-Delivery-Tag'] = delivery_tag

    data = {
        'to': to,
        'messages': [message.as_json_dict() for message in messages],
    }
    line_bot_api._post(
        '/bot/pnp/push', data=json.dumps(data), timeout=timeout
    )


@app.route("/", methods=['GET'])
def index():
    return hello_world(None)

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
        print("------------ ERROR ------------")
        return 'ERROR'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

if __name__ == "__main__":
    # app.run(debug=True)
    app.run()
    print(hello_world(1))
