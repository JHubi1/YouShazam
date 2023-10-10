from youtubesearchpython import VideosSearch
import pytube
import os
import sys
import shutil
import re
import csv
import json
import requests
from unidecode import unidecode
import music_tag
import moviepy.editor
from time import sleep

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

config_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "config.json"))
sample_config = {"headlessBrowser": True, "downloadArtworks": True, "downloadLyrics": False}
if not os.path.isfile(config_file):
    with open(config_file, "w") as f:
        json.dump(sample_config, f)
with open(config_file, "r") as f:
    config = json.load(f)

if not __name__ == "__main__":
    def print(*args, **kwargs): pass
    def input(*args, **kwargs): pass

try: file = os.path.abspath(sys.argv[1])
except: file = os.path.abspath("./shazamlibrary.csv")

try: shutil.rmtree("output")
except: pass

print("<<YouShazam>>")

try:
    requests.head("http://google.com", timeout=2)
except requests.ConnectionError:
    print("\nFor this tool to work, you need a valid internet connection!")
    sys.exit()

options = webdriver.ChromeOptions()
if config["headlessBrowser"]:
    options.add_argument("--headless")
options.add_argument("--disable-web-security")
options.add_argument("--disable-site-isolation-trials")
options.add_argument("--log-level=3")
driver = webdriver.Chrome(options=options)

failed = 0
failed_list = []
titles = []

def __download_error(name: str, path: str, title: str, text: str, url: str, critical: bool = True):
    if critical:
        try: os.remove(path + ".mp3")
        except: pass
        try: os.remove(path + ".mp4")
        except: pass
        try: os.remove(path + ".jpg")
        except: pass
        with open(path + ".txt", "w") as f:
            f.write(f"{name} in '{title}': {url.replace('https://www.youtube.com/watch?v=', '')} {text}")
    print(f" - {name}")

with open(file, "r") as f:
    lines = csv.reader(f, delimiter=',')
    count = 0
    for i in lines:
        count += 1
        if count > 2:
            if not i[0] == "":
                titles.append([i[0], unidecode(i[2]).replace('"', ""), i[3].replace('"', ""), i[4], i[5]])
    os.makedirs("output", exist_ok=True)

# MAIN LOOP
for i in titles:
    print(f"\nDownloading (#{i[0]}): '{i[1]}' by '{i[2]}'")
    cover = None

    if len(i[0]) == 1: num = "00" + str(i[0])
    elif len(i[0]) == 2: num = "0" + str(i[0])
    else: num = str(i[0])

    title = str(i[1]).strip()
    title = title.replace(" ", "_")
    title = re.sub(r"\(.*?\) {0,1}", "", title)
    title = re.sub(r"\[.*?\] {0,1}", "", title)
    title = title.strip().removeprefix("_").removesuffix("_")

    x = 0
    while True:
        x += 1
        url = VideosSearch(f"music '{i[1]}' by {i[2]} (official lyrics)", 1).result()["result"][0]["link"].strip()

        try:
            yt = pytube.YouTube(url)
            yt = yt.streams.filter(only_audio=True).first()
            yt.download(os.path.abspath("output"), f"{num}-{title}.mp4")

            video = moviepy.editor.AudioFileClip(os.path.join("./output",  f"{num}-{title}.mp4"))
            video.write_audiofile(os.path.join("./output",  f"{num}-{title}.mp3"), verbose=False, logger=None)
            video.close()
            os.remove(os.path.join("./output",  f"{num}-{title}.mp4"))
            print(" - Downloading successful")
            break
        except:
            if x > 10:
                failed += 1
                failed_list.append([i[0], i[1], i[2], url.replace('https://www.youtube.com/watch?v=', '')])
                __download_error("AgeRestrictedError", os.path.join("./output",  f"{num}-{title}"), i[1], "is age restricted, and can't be accessed without logging in.", url)
                break

    if config["downloadArtworks"]:
        x = 0
        while True:
            x += 1
            try:
                driver.get(i[3])
                element_present = EC.presence_of_element_located((By.CSS_SELECTOR, f"#\/track\/info\/{i[4]} > article.page-hd-v2.preview-avail.variant-b > div.inner-content.grid.grid-vert-top > div.art.flex-reset.audio-play.variant_b > img"))
                WebDriverWait(driver, 10).until(element_present)
                sleep(2)
                image = driver.find_element(By.CSS_SELECTOR, f"#\/track\/info\/{i[4]} > article.page-hd-v2.preview-avail.variant-b > div.inner-content.grid.grid-vert-top > div.art.flex-reset.audio-play.variant_b > img")
                image_url = image.get_dom_attribute("src")
                headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"}
                download = requests.get(image_url, headers=headers)
                with open(os.path.join("./output",  f"{num}-{title}.jpg"), "wb") as f: f.write(download.content)
                cover = True
                print(" - Cover download successful")
                break
            except:
                if x > 10:
                    failed += 1
                    failed_list.append([i[0], i[1], i[2], url.replace('https://www.youtube.com/watch?v=', '')])
                    __download_error("ChromeDriverError", os.path.join("./output",  f"{num}-{title}"), i[1], "has failed in cover downloading. Try it again or disable artwork downloading.", url, False)
                    del driver
                    driver = webdriver.Chrome(options=options)
                    cover = False
                    break
    else:
        print(" - Cover download skipped")
        cover = False

    if config["downloadLyrics"]:
        x = 0
        while True:
            x += 1
            try:
                driver.get(f"https://www.google.com/search?q=%27{i[1].replace(' ', '+')}%27+by+%27{i[2].replace(' ', '+')}%27+lyrics")
                element_present = EC.presence_of_element_located((By.CSS_SELECTOR, "#kp-wp-tab-default_tab\\:kc\\:\\/music\\/recording_cluster\\:lyrics > div.TzHB6b.cLjAic.LMRCfc > div > div > div:nth-child(2) > div > div > div > div > div:nth-child(3) > div:nth-child(2)"))
                WebDriverWait(driver, 10).until(element_present)
                sleep(3)
                text = driver.find_element(By.CSS_SELECTOR, "#kp-wp-tab-default_tab\\:kc\\:\\/music\\/recording_cluster\\:lyrics > div.TzHB6b.cLjAic.LMRCfc > div > div > div:nth-child(2) > div > div > div > div > div.xaAUmb > div:nth-child(2)")
                cut_text = text.text.strip()
                # with open(f"output/{i[1]}.txt", "w") as f: f.write(cut_text)
                lyrics = True
                print(" - Lyrics download successful")
                break
            except:
                if x > 10:
                    failed += 1
                    failed_list.append([i[0], i[1], i[2], url.replace('https://www.youtube.com/watch?v=', '')])
                    __download_error("ChromeDriverError", os.path.join("./output",  f"{num}-{title}"), i[1], "has failed in lyrics downloading. Try it again or disable lyrics downloading.", url, False)
                    del driver
                    driver = webdriver.Chrome(options=options)
                    lyrics = False
                    break
    else:
        print(" - Lyrics download skipped")
        lyrics = False

    x = 0
    while True:
        x += 1
        try:
            audio = music_tag.load_file(os.path.join("./output",  f"{num}-{title}.mp3"))
            audio.append_tag("tracktitle", i[1])
            audio.append_tag("artist", i[2])
            audio.append_tag("comment", "Downloaded with YouShazam")
            if cover:
                with open(os.path.join("./output",  f"{num}-{title}.jpg"), 'rb') as f:
                    audio.append_tag("artwork", f.read())
                os.remove(os.path.join("./output",  f"{num}-{title}.jpg"))
            if lyrics:
                audio.append_tag("lyrics", cut_text)
            audio.save()
            print(" - Tagging successful")
            break
        except:
            if x > 10:
                failed += 1
                failed_list.append([i[0], i[1], i[2], url.replace('https://www.youtube.com/watch?v=', '')])
                __download_error("AudioFileTaggingError", os.path.join("./output",  f"{num}-{title}"), i[1], "has failed in MP3 tag creation.", url, False)
                os.remove(os.path.join("./output",  f"{num}-{title}.jpg"))
                break
# MAIN LOOP END

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