import json
import glob
import os
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

MODS = {}

TRACKERS = {
    "urls_scanned": 0,
    "mods_found": 0
}

# populate master dict...
# refer to online master dict
# (wait) populate local dict
# (wait) update local dict
# show mods available to update
# check dependencies
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
        "slug": data.get("slug"),
        "url": data.get("websiteUrl"),
        "owner": data.get("authors")[0].get("name"),
        "files": data.get("gameVersionLatestFiles")
    }
    return mod


def getRemoteFiles(id):
    """Get the latest file versions available for a given mod."""
    data = json.loads(urlopen(URLS["CF_WATCHDOG"] + id).read().decode("utf-8"))
    return data["gameVersionLatestFiles"]

    # TODO
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
                slug = mod.pop("slug")
                del(mod["files"])
                mods.update({slug: mod})
        total = t.yellow(
            str(TRACKERS["urls_scanned"] + TRACKERS["mods_found"]))
        found = t.cyan(str(TRACKERS["mods_found"]))
        print(t.bold("Scanned a total of " + total +
                     " CurseForge projects and found " + found + " mods."))
        json.dump(mods, file, indent=4)
        # if DEBUG:
        # print(json.dumps(mods, indent=4))
    print(t.bold(t.white_on_teal("Local file successfully updated.")))


def parseLocalFiles():

    # assume that MODS{} has already been populated.

    os.chdir(os.path.dirname(__file__))

    for file in glob.glob("*.jar"):
        z = zipfile.ZipFile(open(file, 'rb'))
        contents = z.read("META-INF/mods.toml").decode().replace(" ", "")
        # print(contents)

        regex = r"^displayURL\S+"
        matches = re.search(regex, contents, re.MULTILINE)
        try:
            url = matches.group(0).partition("=")[2].replace("\"", '')
            slug = url.split("/")[-1]
            print("The ID of mod with slug " +
                  slug + " is probably: " + str(MODS.get(slug)))
            # compare against MODS{} vals

        except AttributeError:
            url = "Update URL not present or invalid."
            # print(contents)
        print(url)

        # url = ""  # TODO
        # svc_data = json.loads(urlopen(URLS["CF_WATCHDOG"] + url).read())

        z.close()
    return


def loadLocal():
    # TODO
    return


def loadRemote():
    # TODO
    MODS.update(json.loads(urlopen(URLS["CF_MODS"]).read()))
    return


# populate()
loadRemote()
parseLocalFiles()
