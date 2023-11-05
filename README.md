# FoxFM 📻
## Simple python application for modifing audio files

`Made by RealFictionStudio`<br><br>
This project was created to adapt music files to be played with equal volume in public (eg. for a local radio). At the begining, the only feature that it had was sound volume normalization however in a later stage there were other features added like fade-in and fade-out or silient breaks between each file. To sum up, with this app you are able to:

* Unify volume levels of given files
* Join audio files into one
* Add fade-in and fade-out to each file
* Separate files with silient part
* Download videos and playlists from YouTube

## Installation 🛠️

### 1. Download the newest release for your system

1. Unzip the file
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

In the Download tab you will see the input field for a YouTube URL of the video or playlist that you want to download. Just paste it in here, click the `Download` button and choose download location.

### Edit

In the Edit tab you will see two scroll frames. The left one is for audio files that you will be loading and the right one is for ordering exported files. To load a file, click the `Load file` button and select the ones you want. To add to the queue click `+` on the choosen file tile. It will appear on the right scroll frame. To delete it from the queue, click `-` on the tile on the right frame. If you are satisfied with the current file order, click the `Export` button.

### Exporting

You will be prompted with an export form window. There you can type:

* How long a silience should be between each sound (in seconds)
* How long should it take to fade-in from silience to each file volume at the begining (in seconds)
* How long should it take to fade-out from each file volume to silience at the end (in seconds)
* Value of volume that the exported file should have. It will join files from the queue and equalize their volumes to a given value, note that: 
  * The value should be in dBFS (decibells in full scale) which means that the closer the value is to `0` the louder it will be;
  * The value can be both positive and negative;
  * Silience starts from `42` or from `-42`;
  * If you type a number between `5` and `-5` (including 0) the file will be as loud as if you typed `5` or `-5`. You can't get a higher volume;
  * If you leave the entry blank the resault will be as if you typed 30

If all values are typed in as you wish, click the `Export` button and wait until it finishes. It shouldn't take longer than your selected audio length summarised.

Enjoy :)