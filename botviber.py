import json
import logging

import requests
from flask import Flask, request, Response
from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.messages.text_message import TextMessage
from viberbot.api.messages.url_message import URLMessage
from viberbot.api.viber_requests import ViberFailedRequest, ViberConversationStartedRequest
from viberbot.api.viber_requests import ViberMessageRequest
from viberbot.api.viber_requests import ViberSubscribedRequest

app = Flask(__name__)
viber = Api(BotConfiguration(
	name='Test3312bot',
	avatar='',
	auth_token='4b3779249f67d35f-c9f6a69dd4d7a4b2-6e59c785345fb8b2'
))

viber.set_webhook('https://viberbotapp.herokuapp.com/botviber.py')

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

@app.route('/incoming', methods=['POST'])
def incoming():
	logger.debug("received request. post data: {0}".format(request.get_data()))
	# handle the request here
	return Response(status=200)

	if not viber.verify_signature(request.get_data(), request.headers.get('X-Viber-Content-Signature')):

			return Response(status=403)

		# this library supplies a simple way to receive a request object

	viber_request = viber.parse_request(request.get_data())

	if isinstance(viber_request, ViberMessageRequest):
		message = viber_request.message 
		viber.send_messages(viber_request.sender.id, [
			message
		])

	elif isinstance(viber_request, ViberSubscribedRequest):
		viber.send_messages(viber_request.user.id, [
			TextMessage(text="thanks for subscribing!")
		])

	elif isinstance(viber_request, ViberFailedRequest):
		logger.warn("client failed receiving message. failure: {0}".format(viber_request))

	return Response(status=200)



if __name__ == "__main__":
	app.run(host='0.0.0.0', debug=True)
