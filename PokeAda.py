# Quick hack to find rare Pokemons in House of Ada proximity and shout the alarm! + other stupid stuff
# House of Ada, @danski
# 2016-09-16
#
import requests, json, time, datetime
from twilio.rest import TwilioRestClient

#### STATIC VALUES####
# GPS poly corners
gps_box = [(55.60384486756492,13.004449009895325),(55.60199020536713,13.004706501960754),(55.60335393610511,13.009137511253357),(55.60456610140498,13.007935881614685)]

# Tuple containing cool pokemons IDs
awesome_pokemons_list = (19,41,29,30,31,32,33,35,36,37,40,43,44,50,55,56,58,63,64,66,69,70,74,77,84,88,92,93,109,111,117,122,125,1,2,3,4,5,6,7,8,9,25,26,31,34,38,45,51,57,59,62,65,67,68,71,75,76,78,80,82,85,87,89,91,94,95,99,102,103,104,105,106,107,108,110,112,113,114,123,126,127,130,131,134,135,136,137,138,139,140,141,142,143,144,145,146,147,148,149,150,151)

# Twilio account setting for SMS
account_sid = "AC5ebe14d7bd1440cac4c320a8ae0c1dbc"
auth_token = "c92d1f0de3ef63bfd8a9457d343bd655"
client = TwilioRestClient(account_sid, auth_token)



#### FUNCTIONS, USEFUL AND POINTLESS ALIKE ####
# Check if cords are inside poly
def is_pokemon_at_ada(x,y,poly):
        n = len(poly)
        inside = False

        p1x,p1y = poly[0]
        for i in range(n+1):
                p2x,p2y = poly[i % n]
                if y > min(p1y,p2y):
                        if y <= max(p1y,p2y):
                                if x <= max(p1x,p2x):
                                        if p1y != p2y:
                                                xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                                        if p1x == p2x or x <= xints:
                                                inside = not inside
                p1x,p1y = p2x,p2y
        return inside

# Function for sending SMS, phonenumber must start with +46
def sms_to(phonenumber, pokemon_id):
        message = client.messages.create(to=phonenumber, from_="+17133224203", body="Spring! Hittade en "+str(pokemon_id)+" se http://www.google.com/maps/place/"+str(pokemon.get('Latitude'))+","+str(pokemon.get('Longitude'))+" - Kvar tills "+ datetime.datetime.fromtimestamp(int(pokemon.get('Expiration'))/1000).strftime('%H:%M:%S'))

# Todo: Function for Slackbot spam
def slack_say(pokemon_id):
        pass

# Todo: Function for Larm
def alarm():
        pass



#### GET THEM POKEMONS ####
# List contaning encounters, we don't want the lamp giving Ada-workers epilepsy by going of every tick for same Pokemon
encounter_ids = []

while True:
        time.sleep(30) # How ofter to get them pokemons

        # Get pokemon json from our saviour Magic Mike
        r = requests.get('http://magicmike.se/map/map_data.php')
        pokemons = r.json()

        # Check if pokermon is within Ada proximity
        for pokemon in pokemons:
                if is_pokemon_at_ada(pokemon.get('Latitude'),pokemon.get('Longitude'),gps_box):
                        # Check if Pokemon is awesome
                        if pokemon.get('Number') in awesome_pokemons_list and pokemon.get('EncounterID') not in encounter_ids:
                                print "JAAA, vi har en pokemon med ID " + str(pokemon.get('Number')) + " i nerheten. Kvar tills"
                                print datetime.datetime.fromtimestamp(int(pokemon.get('Expiration'))/1000).strftime('%Y-%m-%d %H:%M:%S')
                                #sms_to("+4670800000",pokemon.get('Number')) #To send SMS, uncomment and add phonenumber
                                print "Wow, hittade en "+str(pokemon.get('Number'))+" se http://www.google.com/maps/place/"+str(pokemon.get('Latitude'))+","+str(pokemon.get('Longitude'))+" - Kvar tills "+ datetime.datetime.fromtimestamp(int(pokemon.get('Expiration'))/1000).strftime('%Y-%m-%d %H:%M:%S')