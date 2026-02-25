# dataset-phi 2

# Spanish Historical Document Dataset (18th Century)

[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)

## Overview

This dataset contains handwritten Spanish historical documents from the 18th century, complete with word-level transcriptions. The collection serves as a valuable resource for researchers in historical document analysis, handwriting recognition, and digital humanities.

## Dataset Details

### Content
- Historical manuscripts from 18th century Spain
- Medium-resolution document images
- Word-level transcription annotations
- Diverse collection of writing styles and document types

### Statistics
| Split       | Size |
|-------------|------|
| Training    | 859  |
| Validation  | 97   |
| Test        | 8    |
| **Total**   | 964  

## install

```
pip install -r requeriments.txt
```


## Adornaciones

Este dataset puede mejorar agregandole palabras con adornaciones
tales como:

```
Id -- Text
96-p01l01-01 --  E|x|p|e|d|i|e|n|t|e| |s|o|b|r|e| |l|a| |r|e|a|l| |o|r|d|e|n| |d|e|c|l|a|r|a|n|d|o
96-p01l01-02 -- E|x|p|e|d|i|e|n|t|e| |s|o|b|r|e| |l|a| |r|e|a|l| |o|r|d|e|n
96-p01l02-03 -- q|u|e| |d|e|v|e| |d|a|r|s|e| |p|a|r|a| |t|o|d|o|s| |l|o|s| |c|u|e|r|p|o|s
```

dado que el modelo no fue entrenado con muchas de esta adornaciones que pendinente
mejorar el modelo para tratar estas particularidades de la escritura del siglo XVIII

esto son los test de linear pero de documento que fueron usados para el entrenamiento:

```
1-02 C|u|e|n|t|a|s| |d|e| |L|i|m|a| |e|n| |q|u|e| |a| |c|o|n|s|e|c|u|e|n|c|i|a
1-03 C|u|e|n|t|a|s| |d|e| |L|i|m|a| |e|n| |q|u|e| |a
91-01 y| |m|u|n|i|f|i|e|n|c|i|a| |s|o|b|e|r|a|n|a| |s|e| |h|a| |s|e|r|v|i|d|o
91-02 y| |m|u|n|i|f|i|e|n|c|i|a| |s|o|b|e|r|a|n|a| |s|e| |h|a
92-01 t|o|m|e| |l|a|s| |p|r|o|v|i|d|e|n|c|i|a|s| |c|o|r|r|e|s|p|o|n|d|i|e|n|t|e|s| |p|a|r|a| |l|a
92-02 t|o|m|e| |l|a|s| |p|r|o|v|i|d|e|n|c|i|a|s| |c|o|r|r|e|s|p|o|n|d|i|e|n|t|e|s
```

#### referencias

- https://memoriamanuscrita.bnp.gob.pe/