# Mel2Word: Melody to Text Representation

This repository contains the implementation of Mel2Word, a method designed to convert melodic sequences into text-based representations, enhancing symbolic music analysis through the transformation of melodies into word-like units. The primary aim is to advance symbolic music analysis by introducing a novel segmentation method for tokenization, leveraging Byte-Pair Encoding (BPE) as a widely adopted method for text tokenization.

For in-depth information, please refer to the associated journal article:

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

Certainly! Here's a brief addition to your README file:

---

## Attached Files

### Example Datasets and Pre-generated Dictionary

The datasets and pre-generated dictionaries used for creating examples in the demo code are available in this GitHub repository.

- **[Pre-generated-dictionary.zip](https://github.com/saebyulpark/Mel2word/blob/d17607cbd0f3e5755d4421e13b6801c19fed647a/Pre-generated-dictionary.zip)**: Contains pre-generated dictionaries used in the Mel2Word method. These dictionaries have been crafted for various features and sizes.

- **[Example_Datasets.zip](https://github.com/saebyulpark/Mel2word/blob/d17607cbd0f3e5755d4421e13b6801c19fed647a/Example_Dataset.zip)**: Includes melody datasets specifically curated for creating dictionaries in the Mel2Word method. These datasets exemplify the tokenization process using the MTC-ANN (Meertens Tune Collection), a valuable resource for symbolic music analysis. [Reference Link]([insert-reference-link](https://www.liederenbank.nl/mtc/))

Feel free to explore and utilize these resources for a deeper understanding of the Mel2Word method.

---

## Contact

For inquiries, issues, or collaboration opportunities, reach out to saebyul_park@kaist.ac.kr.

---
