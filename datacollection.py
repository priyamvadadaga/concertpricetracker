import requests
import json
import datetime
import urllib
import pandas as pd

# CHANGE DEPENDING ON SPOTIFY USER vvv
spotify_client_id = '6215857b3bf84219ac8872ce94c3051d'
spotify_client_secret = 'dda4b472f3ba4f9fb2775d5b537d1b01'

# locates city and returns population
def getPopulation(city):
    link = 'https://documentation-resources.opendatasoft.com/api/records/1.0/search/?dataset=geonames-all-cities-with-a-population-1000&q=%s&facet=city'
    url = link % urllib.parse.quote(city)
    resp = requests.get(url)
    respjson = resp.json()

    if(len(respjson['records']) == 0):
        return '???'

    # print(city)
    # print(respjson['records'][0]['fields']['population'])
    return respjson['records'][0]['fields']['population']

# gives price of event given event
def getPrices(id):
    # change this vvv
    key = "n2HVQk1P2e3QAjYYXi8GKfyKgO64niCk"
    request_parameters = {
        'apikey': key
    }
    link = 'https://app.ticketmaster.com/commerce/v2/events/' + id + '/offers'+'.json?{apikey' + '}'
    resp=requests.get(url=link, params=request_parameters)
    jsonresp = resp.json()
    return jsonresp

# gives artist rating
def getPopularity(artist):
    urlartist = artist.replace(" ", "%20")
    body = {"grant_type": "client_credentials"}
    tokenURL = "https://accounts.spotify.com/api/token"
    
    token = requests.post(tokenURL, data=body, auth=(spotify_client_id, spotify_client_secret))
    tokenJSON = token.json()
    
    header = {"Authorization": "Bearer " + tokenJSON['access_token']}
    searchURL = "https://api.spotify.com/v1/search?q={}&type=artist".format(urlartist)

    resp = requests.get(searchURL, headers=header)
    artist_details = resp.json()
    artist_rating = artist_details['artists']['items'][0]['popularity']
    
    return artist_rating

# returns data about upcoming concerts for given artist
def getEventsData(artist):
    print('ARTIST: ', artist)
    # example https://app.ticketmaster.com/discovery/v2/events.json?size=20&keyword=post_malone&sort=relevance,desc&apikey=sPYngrqc3a29GkMAd2SOBDuPm7VdHT9o
    link = 'https://app.ticketmaster.com/discovery/v2/events.json?size=20&keyword=' + artist + '&sort=relevance,desc&apikey=sPYngrqc3a29GkMAd2SOBDuPm7VdHT9o'
    jsonresponse = requests.get(link).json()
    events = {}

    if jsonresponse.get(u'_embedded')==None:
        print(artist + " has no shows!")
        return events

    # iterate over length of embedded events
    for i in range(0, len(jsonresponse.get(u'_embedded').get(u'events'))):
        if jsonresponse.get(u'_embedded').get(u'events')[i].get('priceRanges') != None:
            show = {}
            year = ""
            month = ""
            day = ""


            d8 = jsonresponse.get(u'_embedded').get(u'events')[i].get(u'dates').get(u'start').get(u'localDate')            
            for j in range(0, len(d8)):
                if j >= 0 and j <= 3:
                    year += d8[j]
                elif j >= 5 and j <= 6:
                    month += d8[j]
                elif j > 7 and j <= 9:
                    day += d8[j]
            date = datetime.date(int(year), int(month), int(day))
            eventday = date.weekday()
            weekend = 0

            if (eventday == 5 or eventday == 6):
                weekend = 1

            curr_event = jsonresponse.get(u'_embedded').get(u'events')[i] 

            event_ids = curr_event.get('id')
            event_city = curr_event.get(u'_embedded').get(u'venues')[0].get(u'city').get(u'name')
            population = getPopulation(event_city)
            event_venue = curr_event.get(u'_embedded').get(u'venues')[0].get(u'name')
            price_max = curr_event.get(u'priceRanges')[0].get(u'max')
            price_min = curr_event.get(u'priceRanges')[0].get(u'min')
            event_name = curr_event.get(u'name')
            if (curr_event.get(u'classifications')[0] != None and curr_event.get(u'classifications')[0].get(u'genre') != None):
                event_genre = curr_event.get(u'classifications')[0].get(u'genre').get(u'name')
            else:
                event_genre = '???'
            artist_rating = getPopularity(artist)
            event_id = artist + str(i)

            show.update({'artist' : artist})
            show.update({'city' : event_city})
            show.update({'venue' : event_venue})
            show.update({'showName' : event_name})
            show.update({'genre' : event_genre})
            show.update({'weekend' : weekend})
            show.update({'month' : month})
            show.update({'maxprice' : price_max})
            show.update({'minprice' : price_min})
            show.update({'id' : event_ids})
            show.update({'score' : artist_rating})
            show.update({'pop' : population})

            events.update({event_id : show})
    return events

artists=[
    'Post Malone', 'Drake', 'Childish Gambino', 'Imagine Dragons', 'Cardi B', 'Shinedown',
    'Leon Bridges', 'Ed Sheeran', 'Shawn Mendes', 'Luke Combs', 'Camila Cabello', 'Kendrick Lamar',
    'The Weeknd', 'Jason Aldean', 'Lake Street Dive', 'Bruno Mars', 'Dua Lipa','Taylor Swift', 'Maroon',
    'Migos', 'Keith Urban', 'Kane Brown', 'Ariana Grande', 'Nicki Minaj', 'Chris Stapleton', 'Charlie Puth',
    'Florida Georgia Line', 'Khalid','Kenny Chesney','YoungBoy Never Broke Again','Thomas Rhett', 'Halsey',
    'Bazzi', 'SZA', 'Marshmello', 'P!nk', 'Travis Scott', 'Justin Timberlake', 'Bebe Rexha', 'Rich The Kid',
    'Demi Lovato','BlocBoy JB','Brett Young', 'Luke Bryan','Dan + Shay', 'Royce da', 'Ella Mai', 'Rae Sremmurd',
    'Metallica', 'Blake Shelton', 'Rihanna', 'Eminem','Maren Morris','J Balvin', 'Portugal. The Man',
    'Meghan Trainor', 'Zedd','Ty Dolla $ign', 'Parkway Drive', 'Carrie Underwood', 'G-Eazy', 'Daddy Yankee',
    'Lil Dicky', 'Chris Brown', 'Kanye West', 'Ozuna', 'Bad Bunny', 'NF', 'Adele', 'Kelly Clarkson', 'Maluma',
    'Janelle Monae', 'Darius Rucker', 'Godsmack', 'Grey', 'Bad Wolves', 'Foster The People', 'The Chainsmokers', 
    'MercyMe', 'Anne-Marie', 'Sam Smith', 'Lil Pump','Logic','Niall Horan', 'Bon Jovi', 'Lil Uzi Vert',
    'Lynyrd Skynyrd', 'Dustin Lynch', 'Savage', 'Jordan Davis', 'Sam Hunt', 'Panic! At The Disco', 'Famous Dex'
]

masterlist={}
for i in range(0, len(artists)):
    dict = getEventsData(artists[i])
    masterlist.update(dict)

# print(masterlist)

df = pd.DataFrame.from_dict(masterlist)
dfT = df.transpose()
print(dfT)