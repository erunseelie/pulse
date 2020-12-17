import re
import requests
import sys
import zipfile
from urllib.request import urlopen
from blessed import Terminal
import json

t = Terminal()

# Repo: https://github.com/mstiller7/pulse

DEBUG = True

URLS = {
    "CF_WATCHDOG": "https://addons-ecs.forgesvc.net/api/v2/addon/",
    "CF_MODS": "https://raw.githubusercontent.com/mstiller7/pulse/main/mods-cf.json"
}

TRACKERS = {
    "urls_scanned": 0,
    "mods_found": 0
}

# populate master dict...
# refer to online master dict
# (wait) populate local dict
# (wait) update local dict
# show mods available to update
# download latest mod for version
# disable older mod file
# GUIs? https://realpython.com/python-gui-tkinter/


def pulseCF(url):
    """Pulses the CurseForge watchdog at the specified URL for a mod's data."""
    if DEBUG:
        print(url)
    data = json.loads(urlopen(url).read().decode("utf-8"))
    if (data.get("gameSlug") == "minecraft"):
        # null-check.
        if (data.get("categorySection")):
            if (data.get("categorySection").get("path") == "mods"):
                TRACKERS["mods_found"] += 1
                return data
    TRACKERS["urls_scanned"] += 1
    return False


def parseCF(data):
    """Parse a JSON object into usable data."""

    print(data.get("id"))
    print(data.get("name"))
    print(data.get("authors")[0].get("name"))
    print(data.get("websiteUrl"))
    files = (data.get("gameVersionLatestFiles"))

    # for file id 3112851, the DL link is
    # https://edge.forgecdn.net/files/3112/851/Coins-1.16.4-5.0.1.jar
    # https://edge.forgecdn.net/files/2934/454/Coins-1.15.2-1.0.1.jar
    # muahaha
    # thus, get the file id and split
    # an array -> projectFileId + projectFileName
    # -> gameVersion
    # compare filenames & sizes?
    # show date -> fileDate


def populate():
    start = 377056
    for i in range(start, start+10):
        data = pulseCF(URLS.get("CF_WATCHDOG") + str(i))
        if data is not False:
            parseCF(data)
    total = t.yellow(str(TRACKERS["urls_scanned"] + TRACKERS["mods_found"]))
    found = t.cyan(str(TRACKERS["mods_found"]))
    print(t.bold("Scanned a total of " + total +
                 " CurseForge projects and found " + found + " mods."))


populate()


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
