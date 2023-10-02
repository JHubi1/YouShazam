from youtubesearchpython import VideosSearch
import pytube
import shutil
import sys
import os
import re
import requests
from unidecode import unidecode

if not __name__ == "__main__":
    def print(*args, **kwargs): pass
    def input(*args, **kwargs): pass

try: file = os.path.abspath(sys.argv[1])
except: file = os.path.abspath("./shazamlibrary.csv")

try: shutil.rmtree("output")
except: pass

print("<<YouShazam>>", end="")

try:
    requests.head("http://google.com", timeout=2)
except requests.ConnectionError:
    print("\nFor this tool to work, you need a valid internet connection!")
    sys.exit()

failed = 0
failed_list = []

with open(file, "r") as f:
    lines = f.read().split("\n")
    lines.pop(0)
    lines.pop(0)
    titles = []
    for i in lines:
        i = i.split(",")
        if not i[0] == "":
            titles.append([i[0], unidecode(i[2]).replace('"', ""), i[3].replace('"', "")])
    os.makedirs("output", exist_ok=True)
    for i in titles:
        print(f"\nDownloading (#{i[0]}): '{i[1]}' by '{i[2]}'", end="")
        x = 0
        while True:
            x += 1
            url = VideosSearch(f"music '{i[1]}' by {i[2]} (lyrics)", 1).result()["result"][0]["link"].strip()

            if len(i[0]) == 1: num = "00" + str(i[0])
            elif len(i[0]) == 2: num = "0" + str(i[0])
            else: num = str(i[0])

            title = str(i[1]).strip()
            title = title.replace(" ", "_")
            title = re.sub(r"\(.*?\) {0,1}", "", title)
            title = re.sub(r"\[.*?\] {0,1}", "", title)
            title = title.strip()
        
            try:
                yt = pytube.YouTube(url)
                yt = yt.streams.filter(only_audio=True).first()
                yt.download(os.path.abspath("output"), f"{num}-{title}.mp3")
                print(" - success", end="")
                break
            except:
                if x > 10:
                    failed += 1
                    failed_list.append([i[0], i[1], i[2], url.replace('https://www.youtube.com/watch?v=', '')])
                    with open(os.path.abspath(f"output/{num}-{title}.txt"), "w") as f:
                        f.write(f"AgeRestrictedError: {url.replace('https://www.youtube.com/watch?v=', '')} is age restricted, and can't be accessed without logging in.")
                    print(" - failed", end="")
                    break

print("\n<<Report>>")
try: os.remove("report.txt")
except: pass
f = open("report.txt", "a+")
print(f"Failed: {failed}")
if failed > 0:
    for i in failed_list:
        text = f"Song #{i[0]} failed: '{i[1]}' by '{i[2]}'; last checked id: '{i[3]}'"
        print(f" |--> {text}")
        f.write(text)
f.close()
print("<<Report End>>")

if os.path.isfile("keep.txt"):
    input("\nPress enter to close ... ")