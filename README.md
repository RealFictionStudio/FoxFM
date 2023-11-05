# FoxFM 📻
## Simple python application for modifing audio files

`Made by RealFictionStudio`<br><br>
This project was created to make music files being able to be played with equal volume in public (like in a local radio). At the begining, the only feature that it had was sound volume normalization however in a later stage there were added other like adding fade-in and fade-out or silient breaks between each file. To sum it the app contain for now these features:

* Unify volume levels of given files
* Join audio files into one
* Add fade-in and fade-out to each file
* Separate files with silient part
* Download videos and playlists from YouTube

## Installation 🛠️

### 1. Download the newest release for your system

1. Unzip the downloading
2. Run the `foxfm` executable from the extracted folder

### 2. Clone the repository

1. Paste this command to your command line<br>
```git clone https://github.com/RealFictionStudio/FoxFM.git```
<br>(make sure you have GIT CLI installed) `or` download the zip
2. Open downloaded folder and go to `mini_src` directory
3. Run the `main.py` file from current dir

## How to use it 💡

When you run the app you will encounter two tabs `Download` and `Edit`

### Download

In the Download tab you will see the entry for YouTube URL of the video or playlist you want to download. Just paste it in here and click `Download` button adn choose download location.

### Edit

In the Edit tab you will see two scroll frames. Left one is for audio files you will load and the right one is for ordering exported files. To load a file, click `Load file` button and select the wanted one's. To add to the queue click `+` on choosed file tile. It will appear on the right scroll frame. To delete it from queue, click `-` on the tile on the right frame. If you are satisfied with current file order, click `Export` button.

### Exporting

You will be prompted with export form window. There you can type:

* How long silience should be between each sound (in seconds)
* How long should take to fade-in from silience to each file volume at the begining (in seconds)
* How long should take to fade-out from each file volume to silience at the end (in seconds)
* Value of volume that exported file should have. It will join files from queue and equalize their volumes to a given value, note that: 
  * The value should be in dBFS (decibells in full scale) which means that the closer to `0` the value is the lauder it will be;
  * Value can be both positive or negative;
  * Silience starts from `42` or `-42`;
  * If you type number between `5` and `-5` (including 0) file will be as laud as if you typed `5` or `-5`. You can't get higher volume values;
  * If you leave the entry blank the resault will be as if you typed 30

If all values are typed in as you wished, click `Export` button and wait until it finishes. It shouldn't take longer than your selected audio length summarised.

Enjoy:)