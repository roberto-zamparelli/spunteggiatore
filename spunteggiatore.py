#!/usr/bin/python3
# Program to generate variants of a sentence schema: A [ B1 B2 ] [ C1 C2 ] becomes A B1 C1, A B1 C2, A B2 C1, A B2 C2
# coding: utf-8
# In[ ]:
import argparse
import sys
import os.path
import re
import subprocess
import magic

"""A program to teach the subtle art of punctuation. It takes in input a text file or an image with text, and generates two
formatted files, one without puntuation marks, the other with highlighted punctuation.

Call on text with:

./spunteggiatore.py original-text.txt -o optional-output -t optional-file-title  

or on images:

./spunteggiatore.py original-text-image.jpg -o optional-output -t optional-file-title -l optional-OCR-language

"""


### Argument 

parser = argparse.ArgumentParser(description="Prende un file di testo e produce due versioni formattate in PDF."
                                 +" In una la punteggiatura è stata evidenziata. Nell'altra, è stata rimossa."+
                                 " Tutte le lettere maiuscole che seguono un segno di punteggiatura sono state"+
                                "trasposte in minuscolo.")

parser.add_argument('input', type=str,
                    help="File di input (solo testo).")
parser.add_argument("-t", '--titolo', type=str,
                    help="Titolo del documento")
parser.add_argument("-o", "--output", type=str,
                    help="Output file (default: input-file_con_punt.pdf, input-file_senza_punt.pdf)")
parser.add_argument("-l", "--language", type=str,
                    help="language file for OCR (default: italian)")


args = parser.parse_args()

if not os.path.isfile(args.input):
    print("The file %s does not exist" % args.input)
    sys.exit("Try again. Bye!")

if args.language == None:
  lang = 'ita'
else:
  lang = args.language

testofile = args.input.rsplit(".", 1)[0]

print(type(args.input))

#with open(args.input) as fobj:        # alternative: detect from content.
#  data = fobj.read()                  # broken at read()
content_detected = magic.detect_from_filename(args.input)

if 'text' in content_detected.mime_type:
  with open(args.input,"r") as f1:          # Text found
    testo = f1.read()
elif 'image' in content_detected.mime_type :
  from PIL import Image
  import pytesseract
  pytesseract.pytesseract.tesseract_cmd = r'/usr/local/bin/tesseract'  
  testo = (pytesseract.image_to_string(Image.open(args.input), lang='ita'))
  with open(testofile+".txt", "w") as ft:
    ft.write(testo)
    print("Printing the extracted text to %s" % (testofile+".txt"))
else:
  testo = ""
  sys.exit("Unrecognized input file type (it should be .txt or an image)")

if args.output != None:
    conp = args.output+"ConPunt.tex"
    nop = args.output+"SenzaPunt.tex"
    conpbase = args.output+"ConPunt."
    nopbase = args.output+"SenzaPunt."
else:
    conp = testofile+"ConPunt."+"tex"
    nop = testofile+"SenzaPunt."+"tex"
    conpbase = testofile+"ConPunt."
    nopbase = testofile+"SenzaPunt."
    
print(type(conp))
print(conp)
  
o1 = open(conp, "w")
o2 = open(nop, "w")

if args.titolo != None:
    tit = args.titolo
else:
  if lang == 'ita':
    tit = "Esercizio"
  else:
    tit = "Exercise"

    

LaTeXSkeleton = r'''
\documentclass[a4paper,12pt]{article}
\usepackage[italian]{babel} \usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage{lmodern}
\usepackage{xcolor}
\usepackage[margin=1.3in]{geometry}
\begin{document}
\begin{center}
\begin{Large}
%s
\end{Large}

\

\textsc{%s}
\end{center}

\

%s
\end{document}'''
        

testo = re.sub('-\s', '', testo)
punteggiatura = re.compile(r'([\.,:;\?!\(\)])')  
TestoLower = re.sub(r'([\.:;\?!\)\(])(\s*)([A-Z])', lambda match: match.group(1)+match.group(2)+match.group(3).lower(), testo)
TestoPunt = re.sub(punteggiatura, r"\colorbox{blue!30}{\1}", testo)
TestoNoPunt = re.sub(punteggiatura, "", TestoLower)

OutConPunt = LaTeXSkeleton % (tit, "Con Punteggiatura Evidenziata", TestoPunt)
OutNonPunt = LaTeXSkeleton % (tit, "Senza Punteggiatura", TestoNoPunt)

o1.write(OutConPunt)
o2.write(OutNonPunt)
o1.close()
o2.close()

### Running the latex formatting part

subprocess.run(["pdflatex", "-interaction=nonstopmode", conp])
subprocess.run(["pdflatex", "-interaction=nonstopmode", nop])
subprocess.run(["rm", "-f", nopbase+"aux", conpbase+"aux", nopbase+"log", conpbase+"log", nopbase+"tex", conpbase+"tex" ])

print("\n\n")
print(testo, "::::::::::::::::::::::::::: Testo Normale: %s :::::::::::::::::::::::::::\n" % (testofile))
print(testo)
print("::::::::::::::::::::::::::: Testo Lowercased :::::::::::::::::::::::::::\n" % ())
print(TestoLower)
print("::::::::::::::::::::::::::: Con punteggiatura evidenziata: %s :::::::::::::::::::::::::::\n" % (conp))
print(TestoPunt)
print("::::::::::::::::::::::::::: Con punteggiatura rimossa: %s :::::::::::::::::::::::::::\n" % (nop))
print(TestoNoPunt)


