import urllib
import urllib.request
import json

def count_appearances_of_tag(key, value):
    url = "https://taginfo.openstreetmap.org/api/4/tag/stats?key=" + key + "&value=" + value
    data = json_response_from_url(url)
    print(data)
    return data['data'][0]['count']

def count_appearances_of_key(key):
    url = "https://taginfo.openstreetmap.org/api/4/key/stats?key=" + key
    data = json_response_from_url(url)
    print(data)
    return data['data'][0]['count']

def count_appearances_from_wiki_page_title(osm_wiki_page_title):
    title = osm_wiki_page_title.replace(" ", "_")
    if title.find("Tag:") == 0:
        cleaned = title.replace("Tag:", "")
        key, value = cleaned.split("=")
        return count_appearances_of_tag(key, value)
    elif title.find("Key:") == 0:
        key = title.replace("Key:", "")
        return count_appearances_of_key(key)
    else:
        raise "unhandled"

def count_appearances_of_tag_historic_data(key, value, date): # offset in days??
    pass

def count_appearances_of_key_historic_data(key, date): # offset in days??
    pass

def json_response_from_url(url):
    try:
        data = urllib.request.urlopen(url).read()
        return json.loads(data)
    except UnicodeEncodeError:
        print("failed to process", url)
        raise