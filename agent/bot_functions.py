#!/usr/bin/env python
import requests
import json

# Handle token vales
with open("secrets.json") as json_file:
    data = json.load(json_file)
bot_token = data['bot_token']

class bot:
    def __init__(self, bot_token, botname):
        self.bot_token = bot_token
        self.botname = botname
        self.url = 'https://api.telegram.org/' + bot_token  # Telegram bot url link

    def get_updates(self, offset = 0):
        # Reference: https://core.telegram.org/bots/api#getupdates
        try:
            response = requests.get(self.url + f'/getUpdates?offset={offset}')
        except:
            print('This did not worked!')
        #print(response.text)
        return json.loads(response.text)

    def send_message(self, chat_id, message):
        # Reference: https://core.telegram.org/bots/api#sendmessage
        payload = {'chat_id': chat_id, 'text': message}
        response = requests.post(self.url + '/sendMessage', payload)
        print(response.text)
    
    def send_photo(self, chat_id, photo_link):
        # Reference: https://core.telegram.org/bots/api#sendphoto
        payload = {"chat_id": chat_id, "photo": photo_link}
        response = requests.post (self.url + '/sendPhoto', payload)

    def send_chat_action(self, chat_id, action):
        # Reference: https://core.telegram.org/bots/api#sendchataction
        payload = {'chat_id': chat_id, 'action': action}
        response = requests.post (self.url + '/sendChatAction', payload)
        print(response.text)

if __name__ == '__main__':
    my_bot = bot(bot_token, 'bot name')
    print(my_bot.get_updates())
    #my_bot.send_message('@nebulaenvisions', 'Hola, como estas!')
    #my_bot.send_chat_action('@nebulaenvisions', 'upload_photo')
    #my_bot.send_photo('@nebulaenvisions', 'https://i5.walmartimages.com/asr/3bbb1151-d69a-43fb-b132-47e0bc066307.1f28c1acf3df725a6a39ba4c8738e025.jpeg')
    