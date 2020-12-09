import urllib
import json

def status_for_geometry(entity, claim_id):
    if claim_id not in entity["claims"]:
        return None
    magic_status_code_object = entity["claims"][claim_id][0]["mainsnak"]["datavalue"]["value"]
    if "numeric-id" in magic_status_code_object:
        magic_status_code = magic_status_code_object["numeric-id"]
        if magic_status_code == 8001:
            return "no"
        if magic_status_code == 8000:
            return "yes"
        print(magic_status_code)
        print("invalid status code for geometry")
    else:
        print(magic_status_code_object)
        raise "invalid magic object"

def extract_string(entity, claim_id):
    if claim_id not in entity["claims"]:
        return None
    # partial processing, assumes that first value os relevant and ignores any other
    return entity["claims"][claim_id][0]["mainsnak"]["datavalue"]["value"]

def extract_url(entity, claim_id):
    # maybe implementing whatever type matches should be done...
    return extract_string(entity, claim_id)

def turn_api_response_to_parsed(parsed_json):
    returned_ids = list(parsed_json['entities'].keys())
    if len(returned_ids) != 1:
        raise "unexpected"
    item_id = returned_ids[0]
    entity = parsed_json['entities'][item_id]

    returned = {}
    value = extract_string(entity, "P28")
    if value != None:
        returned["image"] = value
    returned["description"] = entity["descriptions"]["en"]["value"]

    magic_status_code_object = entity["claims"]["P6"][0]["mainsnak"]["datavalue"]["value"] # partial processing, assumes that first value os relevant and ignores any other
    if "numeric-id" in magic_status_code_object:
        magic_status_code = magic_status_code_object["numeric-id"]
        if magic_status_code == 13:
            returned["status"] = "De facto"
        else:
            print(magic_status_code)
            raise "unexpected status code"

    status = status_for_geometry(entity, "P33")
    if status != None:
        returned["onNode"] = status 

    status = status_for_geometry(entity, "P34")
    if status != None:
        returned["onWay"] = status 

    status = status_for_geometry(entity, "P35")
    if status != None:
        returned["onArea"] = status 

    status = status_for_geometry(entity, "P36")
    if status != None:
        returned["onRelation"] = status 

    if "P46" in entity["claims"]:
        returned["combination"] = "??????" # TODO, process this horrific mess

    if "P45" in entity["claims"]:
        returned["implies"] = "??????" # TODO, process this horrific mess

    if "P18" in entity["claims"]:
        returned["seeAlso"] = "??????" # TODO, process this horrific mess

    if "P22" in entity["claims"]:
        returned["requires"] = "??????" # TODO, process this horrific mess

    if "P25" in entity["claims"]:
        returned["group"] = "??????" # TODO, process this horrific mess

    if "P11" in entity["claims"]:
        returned["statuslink"] = extract_url(entity, 'P11')
    

    value = extract_string(entity, "P12")
    if value != None:
        returned["wikidata"] = value
    return returned

def page_data(page_title):
    url = "https://wiki.openstreetmap.org/w/api.php?action=wbgetentities&sites=wiki&titles=" + page_title + "&languages=en|fr&format=json"
    data = urllib.request.urlopen(url).read()
    #print(data)
    parsed = json.loads(data)
    return turn_api_response_to_parsed(parsed)

def tag_data(key, value=None):
    if value == None:
        return page_data("Key:" + key)
    else:
        return page_data("Tag:" + key + "=" + value)

    #print(json.dumps(parsed, indent = 4))

    """
    following fails:

    repo = site.data_repository()
    item = pywikibot.ItemPage(repo, "highway=motorway")
    print(item)

    repo = site.data_repository()
    item = pywikibot.ItemPage(repo, "Tag:highway=motorway")
    # fails with 'Tag:highway=motorway' is not a valid item page title
    print(item)

    # https://phabricator.wikimedia.org/T269635
    item = pywikibot.ItemPage(site, "Key:amenity")
    page = pywikibot.Page(pywikibot.Site(), "Key:amenity")
    item = pywikibot.ItemPage.fromPage(page)
    """

    """
    works but requires known id
    repo = site.data_repository()
    item = pywikibot.ItemPage(repo, "Q4980")
    print(item)
    """
    """
    NOT WORKING
    probably due to https://phabricator.wikimedia.org/T269635

    def get_data_item_from_page(site, page):
        data_item_id = get_data_item_id_from_page(page)
        repo = site.data_repository()
        return pywikibot.ItemPage(repo, data_item_id)

    page = pywikibot.Page(pywikibot.Site(), "Tag:building=yes")
    data_item = get_data_item_from_page(site, page)
    print(data_item)
    data_item.get()  # you need to call it to access any data.
    sitelinks = data_item.sitelinks
    aliases = data_item.aliases
    if 'en' in data_item.labels:
        print('The label in English is: ' + data_item.labels['en'])
    if item.claims:
        for claim in data_item.claims: # instance of
            print(claim)
            print(data_item.claims[claim][0].getTarget())
    """