import re
import requests
import sys
import zipfile
from urllib.request import urlopen
import json


def pulseCF(url):
    data = json.loads(urlopen(url).read().decode("utf-8"))
    print(data.get("gameSlug"))
    # TODO verify equals "minecraft"
    print(data.get("categorySection").get("path"))
    # TODO verify "path" = "mods"
    print(data.get("id"))
    print(data.get("name"))
    print(data.get("authors")[0].get("name"))
    print(data.get("websiteUrl"))
    latestFiles = (data.get("latestFiles"))
    # -> downloadUrl
    # -> gameVersion
    # compare filenames & sizes?
    # show date -> fileDate
    return data


pulseCF("https://addons-ecs.forgesvc.net/api/v2/addon/377056/")

# first, one file POC


def parseFiles():

    for filename in sys.argv[1:]:
        z = zipfile.ZipFile(open(filename, 'rb'))
        contents = (z.read("META-INF/mods.toml")).replace(" ", "")
        # print(contents)
        regex = r"^displayURL\S+"
        matches = re.search(regex, contents, re.MULTILINE)
        try:
            url = matches.group(0).partition("=")[2].replace("\"", '')
            r = requests.get(url)
            print(r.content.decode())
        except AttributeError:
            url = "Update URL not present or invalid."
            # print(contents)
        print(url)
        z.close()
