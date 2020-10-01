# -*- coding: utf-8 -*-
# @Author: TomLotze
# @Date:   2020-08-11 19:01
# @Last Modified by:   TomLotze
# @Last Modified time: 2020-08-14 00:25

from bs4 import BeautifulSoup as BS
import requests
import json

def scrape(url):
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

    # find the script to extract information
    raw = html.find_all("script", type="application/ld+json", id=None)[-1]
    raw = json.loads(raw.string)

    taxonomy = json.loads(html.find("div", {"data-test" : "taxonomy_data"}).string)['pdpTaxonomyObj']

    # create output dictionary for all the info
    info = dict()

    info["link"] = url
    info["title"] = raw['name']
    info["description"] = raw['description']
    try:
        info["authors"] = raw["author"]['name']
    except:
        try:
            info["authors"] = html.find("a", attrs={'data-role' : True}).string
        except:
            info["authors"] = raw['brand']['name']

    try:
        info["isbn"] = raw['workExample']["isbn"]
    except:
        pass

    try:
        info["language"] = raw["workExample"]["inLanguage"].upper()
        info["publication_date"] = raw["workExample"]["datePublished"]
        info['nrPages'] = raw["workExample"]['numberOfPages']
    except:
        pass


    info["image_url"] = raw['image']['url']


    return info
