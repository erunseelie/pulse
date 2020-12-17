import json
import re
import sys
import zipfile
from urllib.request import urlopen

import requests
from blessed import Terminal

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
        if (data.get("categorySection")):  # null-check.
            if (data.get("categorySection").get("path") == "mods"):
                TRACKERS["mods_found"] += 1
                return data
    TRACKERS["urls_scanned"] += 1
    return False


def parseCF(data):
    """Parse a JSON object into usable data."""

    mod = {
        "id": data.get("id"),
        "name": data.get("name"),
        "owner": data.get("authors")[0].get("name"),
        "url": data.get("websiteUrl"),
        "files": data.get("gameVersionLatestFiles")
    }
    return mod

    # for file id 3112851, the DL link is
    # https://edge.forgecdn.net/files/3112/851/Coins-1.16.4-5.0.1.jar
    # https://edge.forgecdn.net/files/2934/454/Coins-1.15.2-1.0.1.jar
    # muahaha
    # thus, get the file id and split
    # an array -> projectFileId + projectFileName
    # -> gameVersion
    # compare filenames & sizes?
    # show date -> fileDate


def parseRemoteFiles(mod):
    """Get the latest file versions available for a given mod."""


def populate():
    """Method to populate the local file via defined search amount from the CurseForge watchdog.

    Only call manually when necessary to update remote master dictionary file.
    """
    mods = {}
    # TODO don't write over existing data.
    with open('mods-cf.json', 'w') as file:
        start = 377056
        for i in range(start, start+10):
            data = pulseCF(URLS.get("CF_WATCHDOG") + str(i))
            if data is not False:
                mod = parseCF(data)
                mods.update({mod["id"]: mod["name"]})
        total = t.yellow(
            str(TRACKERS["urls_scanned"] + TRACKERS["mods_found"]))
        found = t.cyan(str(TRACKERS["mods_found"]))
        print(t.bold("Scanned a total of " + total +
                     " CurseForge projects and found " + found + " mods."))
        json.dump(mods, file, indent=4)
        if DEBUG:
            print(json.dumps(mods, indent=4))
    print(t.bold(t.white_on_teal("Local file successfully updated.")))


populate()


def parseLocalFiles():

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
