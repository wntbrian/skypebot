import urllib.request, urllib.parse, json, os, ssl
from random import randint

ssl._create_default_https_context = ssl._create_unverified_context
GOOGLE_DEV_KEY = os.getenv('GOOGLE_DEV_KEY', 'dev_key')
GOOGLE_CX_SEARCH = os.getenv('GOOGLE_CX_SEARCH', 'cxtoken')
SEARCHTYPE = os.getenv('SEARCHTYPE', 'image')
IMGSIZE = os.getenv('IMGSIZE', 'medium')
NUM = os.getenv('NUM', '5')
FILETYPE = os.getenv('FILETYPE', 'png')


def get_image_link(query):
    parse = urllib.parse.quote(query)
    searchUrl = f"https://www.googleapis.com/customsearch/v1?q={parse}&key={GOOGLE_DEV_KEY}&cx={GOOGLE_CX_SEARCH}&searchType={SEARCHTYPE}&imgSize={IMGSIZE}&num={NUM}&filetype={FILETYPE}"
    f = urllib.request.urlopen(searchUrl)
    deserialized_output = json.load(f)
    if int(deserialized_output['searchInformation']['totalResults']) != 0:
        return deserialized_output['items'][randint(0, int(NUM)-1)]['link']
    else:
        return "https://cdn3.iconfinder.com/data/icons/modifiers-add-on-1/48/v-17-512.png"