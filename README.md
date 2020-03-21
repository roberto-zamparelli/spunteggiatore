# spunteggiatore
A program to teach the subtle art of punctuation.

A python3 script which takes in input a text file or an image with text, and generates two
formatted files, one without puntuation marks, the other with highlighted punctuation. The first can be 
used to try to guess the type and position of punctuation marks (,.!?"()); the second is then used to verify
if the guesses correspond to the original punctuation. 
Of course, punctuation is largely subjective, with very different styles. Guessing the original punctuation is
not a guarantee that we have guessed the "perfect" punctuation. 

Call on text from command prompt with:

./spunteggiatore.py original-text.txt -o optional-output -t optional-file-title  

or on images:

./spunteggiatore.py original-text-image.jpg -o optional-output -t optional-file-title -l optional-OCR-language

When called on images, the program generates a text file (original-text-image.txt) which can be useful to correct 
the text before treating punctuation.

The script requires a functioning pdflatex to generate its PDF output. For image conversion, it uses the 
pytessercat library and assumes that Tesseract OCR (https://github.com/tesseract-ocr/tesseract) has been installed.
When using the OCR function it is useful to pass the optional-OCR-language parameter (e.g. 'ita', 'eng'; default: 'ita')
When removing punctuation, the program lowercases initials that follow ".?)!".

Limits: 
- The OCR does not try to guess the bounding box for the main text.
- Proper names after sentence-ending punctuation are also lowercased, which can give a clue of the presence

Bugs:
- Uppercased accented characters after punctuation are for some reason NOT lowercased.
- Not tested on non UTF-8 encodings

