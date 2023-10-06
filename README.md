# YouShazam
YouShazam is a simple-to-use tool that can download your whole Shazam library from YouTube to your local PC. I searched for a tool to do that for a while now, and after no success, I decided to code my own. It's not perfect, though; for example, the MP3s are not real MP3s. If you add any tags to them, they will corrupt.

## Installation
To start using this tool, simply download the ZIP file of this repository and place it in a new folder on your disk. That's all you need. Now continue in the usage chapter.

## Usage
- To start, visit your Shazam library by simply clicking [here](https://www.shazam.com/de/myshazam), then click on `Download CSV-File` to get your file. **If it's not named `shazamlibrary.csv` rename it to that!**
- After downloading the file, simply drag it into the YouShazam folder and replace the old `shazamlibrary.csv`, which is used as an example.
- Now simply start the `main.py` and wait a bit. It can take longer if you have many titles on your list, be warned!
  - If you get an error from a song, it can't be downloaded due to age restrictions. YouShazam tries to download it 10 times and uses a different video every time.

## License
```
Copyright 2023 JHubi1

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```