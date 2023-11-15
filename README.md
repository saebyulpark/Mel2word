# Mel2Word: Melody to Text Representation

This repository contains the implementation of Mel2Word, a pioneering method that leverages Natural Language Processing (NLP) techniques to transform melodies into word-like representations. The main goal is to improve symbolic music analysis by tokenization using Byte-Pair Encoding (BPE), a popular textual tokenization method.

For in-depth insights, please refer to the associated journal article:

**"Mel2Word: A Text-based Melody Representation for Symbolic Music Analysis"**

**Authors:** Saebyul Park, Eunjin Choi, Jeounghoon Kim, and Juhan Nam

**Journal:** Music and Science, 2023 (Accepted for publication)

## Colab Notebook

The code implementation, demo, and tutorial are available here: 

[**Mel2Word_Demo.ipynb**](https://colab.research.google.com/drive/1ZfnloqWUDe4yKqWS3ljde3YUxk5y14Xc?usp=sharing)

## Mel2Word Features

### Mel2Word Representation

Convert MIDI melodies into Mel2Word representations.

### Mel2Word Dictionaries

Tokenization requires a dictionary. Choose between pre-generated dictionaries or create a custom one based on your dataset.

### Tokenization

Tokenize your melody with the pre-trained or generated dictionary. 

## Environmental Setup

Ensure the following dependencies are installed to run Mel2Word:

- **PrettyMIDI:** A Python library for handling MIDI files. Install it using `pip install pretty_midi`.
- **Google Drive Mounting:** If using Google Colab, mount your Google Drive for file access. Follow the provided steps in the Colab notebook.

## Contact

For inquiries, issues, or collaboration opportunities, reach out to saebyul_park@kaist.ac.kr.

---
