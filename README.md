# Chinese Menu Reader

## Description
Chinese Menu Reader is an iOS application that takes a picture of a dish name on a Chinese menu and gives you some information about the dish, including a translation, a description, user reviews and tags.

This repository contains the code for the Python server. For the iOS application, [check out this repository](https://github.com/ejanzer/menureader_ios).

## How to use it
![Screenshot 1: Open the app](https://raw.githubusercontent.com/ejanzer/menureader/master/screenshots/app1.jpg)

Take a photo of a menu or choose one from your photo library.

![Screenshot 2: Take a photo](https://raw.githubusercontent.com/ejanzer/menureader/master/screenshots/app2.jpg)

Crop the image around the dish you’d like to look up.

![Screenshot 3: Crop the image](https://raw.githubusercontent.com/ejanzer/menureader/master/screenshots/app3.jpg)

Tap “Search” to upload the image to the server.

![Screenshot 4: Dish information](https://raw.githubusercontent.com/ejanzer/menureader/master/screenshots/app4.jpg)

If the dish exists, the server will return some information about the dish. Tap on a tag to see other dishes with the same tag.

![Screenshot 5: Reviews and tags](https://raw.githubusercontent.com/ejanzer/menureader/master/screenshots/app5.jpg)

If the dish doesn’t exist, the server will try to translate the dish name using [CEDICT](http://cc-cedict.org/wiki/). Tap on a similar dish to go to that dish’s page.

## How it works

The iOS application takes the image, crops it, and uploads it to the Python server. The Python server does some basic image processing (smoothing, converting to grayscale, binarizing/thresholding) and then uses [Google Tesseract OCR](https://code.google.com/p/tesseract-ocr/) to get a string of Chinese characters from the image. If Tesseract fails to recognize any characters in the image, the server thins the image (using Stentiford's preprocessing steps and Scikit-Image's skeletonize() function) and runs it through Tesseract again. 

If Tesseract returns characters, the server looks them up first in a dishes table. If a dish is found, it returns a JSON object representing that dish. If not, it attempts to translate the characters relying first on a list of common food words and finally on [CEDICT](http://cc-cedict.org/wiki/), an open source Chinese dictionary maintained by [MDBG](http://www.mdbg.net/).



