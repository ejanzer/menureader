# Chinese Menu Reader

Chinese Menu Reader is a mobile application that takes a picture of a dish name on a Chinese menu and gives you an English translation of the dish name, a description, reviews, photos and tags.

This repository contains the code for the Python server. For the iOS application, [check out this repository](https://github.com/ejanzer/menureader_ios).

### How it works

The iOS application takes the image, crops it, and uploads it to the Python server. The Python server does some basic image processing (smoothing, converting to grayscale, binarizing/thresholding) and then uses [Google Tesseract OCR](https://code.google.com/p/tesseract-ocr/) to get a string of Chinese characters from the image. If Tesseract fails to recognize any characters in the image, the server thins the image (using Stentiford's preprocessing steps and Scikit-Image's skeletonize() function) and runs it through Tesseract again. 

If Tesseract returns characters, the server looks them up first in a dishes table. If a dish is found, it returns a JSON object representing that dish. If not, it attempts to translate the characters relying first on a list of common food words and finally on [CEDICT](http://cc-cedict.org/wiki/), an open source Chinese dictionary maintained by [MDBG](http://www.mdbg.net/).

### Installation

1. Clone the repository:

    <code>$ git clone https://github.com/ejanzer/menureader.git</code>

2. Install [Google Tesseract OCR](https://code.google.com/p/tesseract-ocr/).

3. Add language training data to your tessdata directory (usually at /usr/local/share/tessdata - if not, just set your TESSDATA_PREFIX environment variable to the parent directory of the tessdata directory):

    * [Simplified characters](https://tesseract-ocr.googlecode.com/files/chi_sim.traineddata.gz)
    * [English](https://tesseract-ocr.googlecode.com/files/tesseract-ocr-3.02.eng.tar.gz) – for testing purposes
    * [Traditional characters](https://tesseract-ocr.googlecode.com/files/chi_tra.traineddata.gz) (Note: to use traditional characters, you'll need to also set LANG to 'chi_tra' in config.py.)

4. Make sure Tesseract is installed properly by running pytesser on the test images:

    <code>$ python tesseract/pytesser.py</code>

5. Install Python packages:

    <code>$ pip install -r requirements.txt</code>

6. Run the app:

    <code>$ python app.py</code>

7. Deploy the app or use [ngrok](https://ngrok.com/) to forward your port:

    <code>$ ./ngrok 5000</code>

8. In the [iOS Xcode project](https://github.com/ejanzer/menureader_ios), change the server URL to the server's address ([see instructions on iOS repo for details](https://github.com/ejanzer/menureader_ios)).

### How to use it

1. Take a photo of a menu or choose one from your photo library.

    ![Screenshot 1: Open the app](https://raw.githubusercontent.com/ejanzer/menureader/master/screenshots/app1.jpg)

    ![Screenshot 2: Take a photo](https://raw.githubusercontent.com/ejanzer/menureader/master/screenshots/app2.jpg)

2. Crop the image around the dish you’d like to look up.

    ![Screenshot 3: Crop the image](https://raw.githubusercontent.com/ejanzer/menureader/master/screenshots/app3.jpg)

3. Tap “Search” to upload the image to the server.

    ![Screenshot 4: Dish information](https://raw.githubusercontent.com/ejanzer/menureader/master/screenshots/app4.jpg)

4. If the dish exists, the server will return some information about the dish. Tap on a tag to see other dishes with the same tag.

    ![Screenshot 5: Reviews and tags](https://raw.githubusercontent.com/ejanzer/menureader/master/screenshots/app5.jpg)

5. If the dish doesn’t exist, the server will try to translate the dish name using [CEDICT](http://cc-cedict.org/wiki/). Tap on a similar dish to go to that dish’s page.

### Notes

For best results, take a picture with your camera about 6 inches away from the menu, then zoom and crop around the name of the dish you want to translate. Try to hold the menu straight and avoid blur if possible.

Tesseract has trouble recognizing some Chinese characters that have vertical space between two halves or radicals. I haven't yet figured out how to address this problem, so the app will have trouble recognizing dish names with these characters, especially if the font accentuates these spaces.


