# Mel2Word: Melody to Text Representation

This repository contains the implementation of Mel2Word, a method designed to convert melodic sequences into text-based representations, enhancing symbolic music analysis through the transformation of melodies into word-like units. The primary aim is to advance symbolic music analysis by introducing a novel segmentation method for tokenization, leveraging Byte-Pair Encoding (BPE) as a widely adopted method for text tokenization.

![Mel2Word Represenation](https://drive.google.com/uc?export=download&id=1Xs9GrKwV6tyube8N2gzkom_a-mVXyTsd)

For in-depth information, please refer to the associated journal article:

**"Mel2Word: A Text-based Melody Representation for Symbolic Music Analysis"**

**Authors:** Saebyul Park, Eunjin Choi, Jeounghoon Kim, and Juhan Nam

**Journal:** Music and Science, 2023 (Accepted for publication)

## Colab Notebook

The code implementation, demo, and tutorial are available here:

1. [**Mel2Word_Demo.ipynb**](https://colab.research.google.com/drive/1i-WC0kd1C_JtpRYMxECDQrLu3OCzegf8?usp=sharing): Main Mel2Word demo notebook. This Colab notebook provides a demonstration of Mel2Word with code and examples.




2. [**Mel2Word_Module_Demo.ipynb**](https://colab.research.google.com/drive/1WDq1uF2NzODHTgfCR4P0HSdMKU5Y-O0I?usp=sharing): Module demonstration using mel2word.py for Python module integration.


## Mel2Word Features

### Mel2Word Representation

Convert MIDI melodies into Mel2Word representations.

### Mel2Word Dictionaries

Tokenization requires a dictionary. Choose between pre-generated dictionaries or create a custom one based on your dataset.

### Tokenization
Tokenize your melodies with the pre-trained or generated dictionary.

### Application
Try out WordCloud and Word2Vec techniques for your melodies using the Mel2Word approach.

## Environmental Setup

Ensure the following dependencies are installed to run Mel2Word:

- **PrettyMIDI:** A Python library for handling MIDI files. Install it using `pip install pretty_midi`.
- **Google Drive Mounting:** If using Google Colab, mount your Google Drive for file access. Follow the provided steps in the Colab notebook.

## Attached Files

### Example Datasets and Pre-generated Dictionary

The datasets and pre-generated dictionaries used for creating examples in the demo code are available in this GitHub repository:


- **Dictionary Folder (/Dictionary)**: This folder contains dictionaries pre-generated using the Mel2Word method, as outlined in the associated journal. The dictionaries were constructed during the training phase, incorporating data from 8 monophonic datasets. In total, 3,007 monophonic melodies were included in the training set to build a comprehensive Mel2Word dictionary.

- **Data Example Folder (/Data-example)**: This folder contains an illustrative example sourced from the Meertens Tune Collection [(MTC-ANN)](https://www.liederenbank.nl/mtc/)., featuring Dutch folk melodies. It includes a tokenized version of MTC-ANN ('tokenized_MTC_ANN_Example.pkl') using a 100-word dictionary. This dataset is designed for users to experiment with WordCloud and Word2Vec techniques using the Mel2Word approach in the provided Colab demo, providing a practical hands-on experience.

- [**mel2word.py**](https://github.com/saebyulpark/Mel2word/blob/main/mel2word.py): Python module for Mel2Word.


## Data Analysis

Mel2Word enables the application of NLP algorithms to analyze music data. Check out the data analysis results depicted in the following figure:

![Mel2Word Data Analysis](https://drive.google.com/uc?export=download&id=1tegxqCjHGwCkzCgMu648jIzmvUy45beY)

## Citation

For more details, please refer to our journal article [here].


## Contact

For inquiries, issues, or collaboration, reach out to saebyul_park@kaist.ac.kr.
