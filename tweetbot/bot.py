import tweepy
import requests
import json
from apscheduler.schedulers.blocking import BlockingScheduler

import logging
from logging.handlers import RotatingFileHandler
 
# creation de l_objet logger qui va nous servir a ecrire dans les logs
logger = logging.getLogger()
# on met le niveau du logger a DEBUG, comme ca il ecrit tout
logger.setLevel(logging.DEBUG)
 
# creation d'un formateur qui va ajouter le temps, le niveau
# de chaque message quand on ecrira un message dans le log
formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
# creation d'un handler qui va rediriger une ecriture du log vers
# un fichier en mode 'append', avec 1 backup et une taille max de 1Mo
file_handler = RotatingFileHandler('activity.log', 'a', 1000000, 1)
# on lui met le niveau sur DEBUG, on lui dit qu'il doit utiliser le formateur
# cree precedement et on ajoute ce handler au logger
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
 
# creation d'un second handler qui va rediriger chaque ecriture de log
# sur la console
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)

#create an OAuthHandler instance
#Twitter requires all requests to use OAuth for authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

#Construct the API instance
api = tweepy.API(auth) # create an API object
user = api.get_user('@ + Your User')

#function to get data and send it
def get_data():
        req = requests.get('https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=EUR')

        price = repr(req.json()['EUR'])
        for follower in user.followers():
                id = follower.id
                event = {
                        "event": {
                                "type": "message_create",
                                "message_create": {
                                        "target": {
                                                "recipient_id": follower.id
                                        },
                                        "message_data": {
                                                "text": "Hi! 1 BTC equals " + price + " EUR."
                                        }
                                }
                        }
                }
                api.send_direct_message_new(event)
                logger.info("Message sent !")

#task scheduler to send message every hour
scheduler = BlockingScheduler()
scheduler.add_job(get_data, 'interval', hours=1)
scheduler.start()
