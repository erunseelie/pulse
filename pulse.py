import re
import requests
import sys
import zipfile

# first, one file POC

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
