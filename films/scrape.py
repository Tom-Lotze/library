# -*- coding: utf-8 -*-
# @Author: TomLotze
# @Date:   2020-08-15 11:08
# @Last Modified by:   Tom Lotze
# @Last Modified time: 2021-01-31 13:47


from bs4 import BeautifulSoup as BS
import requests
import json
from .models import Genre, Actor, Film
from datetime import timedelta
import re

def scrape_imdb(url):

    def create_genre(name):
        genre = Genre(**{'genre': name})
        try:
            genre.save()
            g_id = genre.id
        except:
            g_id = Genre.objects.get(genre=name).id

        return Genre.objects.get(genre=name)

    def create_actor(name, url):
        actor = Actor(**{"name": name, "url": url})
        try:
            actor.save()
            a_id = actor.id
        except:
            a_id = Actor.objects.get(name=name).id



        return Actor.objects.get(name=name)



    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

    # get the html code
    try:
        response = requests.get(url, headers=headers)
    except:
        return 1

    html = BS(response.text, "html.parser")
    info = dict()



    info['description'] = html.find("meta", property="og:description")['content']
    info["link"] = url

    # find the script to extract information
    raw = html.find_all("script", type="application/ld+json", id=None)[-1]
    raw = json.loads(raw.string)

    info["title"] = raw['name']
    info["imageURL"] = raw['image']

    genres_raw = raw['genre']

    if isinstance(genres_raw, str):
        genres = [create_genre(genres_raw)]
    else:
        genres = [create_genre(n) for n in genres_raw]

    # determine type: film or series
    if raw['@type'] == "TVSeries":
        info['isSerie'] = True
        info["nrEpisodes"] = int(html.find("span", class_="bp_sub_heading").string.split()[0])
        try:
            info['director'] = raw['creator'][0]['name']
        except:
            info['director'] = "unknown"
    else:
        d = raw['duration']
        h, m = map(int, d[2:-1].split("H"))
        info['duration'] = timedelta(hours=h, minutes=m)

        director = raw['director']
        if type(director) == list:
           info['director'] = raw['director'][0]['name']
        else:
            info['director'] = raw['director']['name']


        try:
            metascore_class = html.select('div[class*="metacriticScore"]')[0]

            info['metascore'] = [int(i) for i in metascore_class.stripped_strings][0]
        except:
            info['metascore'] = 0



    # get actors and director
    actors = [create_actor(a['name'], 'https://imdb.com'+a['url']) for a in raw['actor']]


    info['releaseDate'] = raw['datePublished']
    info['rating'] = float(raw['aggregateRating']['ratingValue'])


    # save film
    film = Film(**info)
    try:
        film.save()
        info['id'] = film.id
    except:
        info['duplicate'] = True
        info['id'] = Film.objects.get(title=film.title).id
        return info



    # link genre and actors
    for g in genres:
        film.genre.add(g)

    for a in actors:
        film.starring.add(a)




    return info










