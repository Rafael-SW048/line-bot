from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from google.oauth2 import service_account

import os
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

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SERVICE_ACCOUNT_FILE = 'keys.json'


CREDS = None
CREDS = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '1OSZXvGldMHw4fgkMMinsAv0L19W_U_8ZmFVVz-DFohw'
SAMPLE_RANGE_NAME = 'B1:F'

try:
    service = build('sheets', 'v4', credentials=CREDS)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')

    else:
        print(values)   

except HttpError as err:
    print(err)

# LINE Massager API
app = Flask(__name__)

line_bot_api = LineBotApi('YXLm/vqJIXGcmuNqyaEu5yYf/l8ElZ1fFm/8rmDbNhwea4bT5Cm4x1qKdm3FyIVWdxXmCX6osVoMtxhR1YJBk8sKzIpliaOgT4MAxqLvPdmBCCoRQNkc/TSu3du9x8yfLT8SDCO5OGtjaIKyDwpoIQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('651cab7325f1467ef97ad60952d5b0e6')

@app.route("/callback", methods=['POST'])
def callback():
    # Get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # Get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # Handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    """ Here's all the messages will be handled and processed by the program """
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
