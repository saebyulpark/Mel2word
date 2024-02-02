# -*- coding: utf-8 -*-
"""Mel2Words_Demo_script_231204

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1rR8x-THpaTudBCGkz-X-XwQwp57Kl0dS

# Mel2Word: Melody to Text Representation

This Colab notebook shows the demonstration of the Mel2Word (M2W) method, which converts monophonic melodic sequences into text-based representations for symbolic music analysis through natural language processing. Mel2Word is an innovative approach in music analysis, transforming melodic sequences into meaningful linguistic-like units, enabling a unique tokenization that captures the essence of musical phrases.


 <img src='https://drive.google.com/uc?export=download&id=1Xs9GrKwV6tyube8N2gzkom_a-mVXyTsd' width="600" height ="" /><br>


The notable aspect of this approach is its ability to tokenize melodies in MIDI format using a data-driven approach, making it possible to apply them directly to NLP algorithms, as depicted in the following figure (which is a result of the data analysis of our study):

<img src='https://drive.google.com/uc?export=download&id=1tegxqCjHGwCkzCgMu648jIzmvUy45beY' width="600" height ="" /><br>

Detailed information is available in the following journal article:

"Mel2Word: A Text-based Melody Representation for Symbolic Music Analysis" by Saebyul Park, Eunjin Choi, Jeounghoon Kim, and Juhan Nam, accepted for publication in Music and Science, 2023."

Also, you can download the relevant files from the following link: [https://github.com/saebyulpark/Mel2word](https://github.com/saebyulpark/Mel2word)

## MIDI melodies to Mel2Word

To begin, transform your MIDI melodies into the Mel2Word format.

**Symbols Explained:**

1. **Pitch:**
   - E, U, D: Indicate 'equal', 'up', 'down'.
   - Numerical Values: Represent the pitch interval using two digits.
   - Example: "U02" signifies a pitch interval increase of 2.

2. **Rhythm:**
   - Numerical Values: Show the Inter-Onset Interval (IOI) in beats, multiplied by 100, quantized to sixteenth notes.
   - Example: "100" indicates a rhythm of 1 beat.

3. **Combined (Pitch + Rhythm):**
   - Merges Pitch and Rhythm elements.
   - Example: "U02100" combines a +2 pitch interval with a rhythm of 1 beat.

For further details, please consult the associated paper.
"""

# @title Codes For Mel2Word

from music21 import *
import numpy as np
from os import listdir
from os.path import isfile, join
from collections import Counter
import pickle
import mel2word


def get_midi(midi_name, melody_program=0):
    """
    Extracts the melody from a MIDI file using music21.

    Parameters:
    - midi_name (str): The name of the MIDI file.
    - melody_program (int, optional): The instrument index in the MIDI file. Defaults to 0.

    Returns:
    - list: The extracted melody notes.
    """
    mf = midi.MidiFile()
    mf.open(midi_name)
    mf.read()
    mf.close()
    s = midi.translate.midiFileToStream(mf)
    melody = s.getElementsByClass('Part')[melody_program].flatten().notes
    return melody

def get_pitch_interval(melody):
    """
    Calculates pitch intervals from a given melody using music21.

    Parameters:
    - melody (list): The melody notes (music21 notes and chords).

    Returns:
    - ndarray: Array of pitch intervals.
    """
    pitches = []
    for nt in melody:
        if isinstance(nt, chord.Chord):
            # Use the highest note in the chord
            pitches.append(nt.sortAscending().pitches[-1].midi)
            print("Ensure the file is a valid monophonic MIDI file. Extracting the melody using top notes...")
        elif hasattr(nt, 'pitch'):
            pitches.append(nt.pitch.midi)
    pitch_interval = np.diff(pitches)
    pitchi = np.clip(pitch_interval, -12, 12)
    return pitchi

def get_IOI(melody, notequantize=0.25):
    """
    Calculates Inter-Onset Intervals (IOIs) from a melody using music21.

    Parameters:
    - melody (list): The melody notes (music21 notes).
    - notequantize (float, optional): The quantization value for note intervals. Defaults to 0.25.

    Returns:
    - ndarray: Array of IOIs.
    """

    beat = [nt.offset for nt in melody]  # Using offset as the start time
    beat_interval = np.diff(beat).astype(float)

    if notequantize is not None and beat_interval.size > 0:
        beat_interval = notequantize * np.round(beat_interval / notequantize)

    beati = np.clip(beat_interval, 0, 4)

    return beati, notequantize


# Function to convert pitch and IOI to Mel2Word representation
def get_M2W(melody, feat='all'):
    """
    Converts pitch and IOIs of a melody to Mel2Word representation.

    Parameters:
    - melody (list): The melody notes (pretty_midi).
    - feat (str, optional): Feature type to convert ('pitch', 'rhythm', or 'all'). Defaults to 'all'.

    Returns:
    - list: The Mel2Word representation.
    """
    try:
      pmidi = get_pitch_interval(melody)
      rtext, quant = get_IOI(melody)
      ptext = [f"U{int(com):02d}" if com > 0 else (f"D{int(-com):02d}" if com < 0 else 'E00') for com in pmidi]

      if quant == 0.25:
          rtext = [f'{int(com * 100):03d}' for com in rtext if com >= 0.25]
      elif quant == 0.125:
          rtext = [f'{int(com * 1000):04d}' for com in rtext]
      else:
          rtext = [f'{int(com * 10000):05d}' for com in rtext]

      alltext = [pt + rt for pt, rt in zip(ptext, rtext)]

      if feat == 'pitch':
          return ptext
      elif feat == 'rhythm':
          return rtext
      elif feat == 'all':
          return alltext
    except:
      print("ERROR!!:Verify if the file is a valid monophonic MIDI file.")


def get_M2W_from_midipath(midipath, feature_option=3):
    """
    Converts a MIDI file to Mel2Word representation based on specified feature options.

    Parameters:
    - midipath (str): The path of the MIDI file.
    - feature_option (int, optional): Option for the feature type to convert (1 for 'pitch', 2 for 'rhythm', 3 for 'all'). Defaults to 3.

    Returns:
    - list: The Mel2Word representation of the MIDI file.
    """
    melody = get_midi(midipath)

    if feature_option == 1:
        m2w_representation = get_M2W(melody, feat='pitch')
    elif feature_option == 2:
        m2w_representation = get_M2W(melody, feat='rhythm')
    elif feature_option == 3:
        m2w_representation = get_M2W(melody, feat='all')
    else:
        print("Invalid feature option. Defaulting to both features.")
        m2w_representation = get_M2W(melody, feat='all')

    return m2w_representation



def get_M2W_dataset(midi_path):
    """
    Generates a Mel2Word dataset from MIDI files in a specified directory.

    Parameters:
    - midi_path (str): The directory path containing MIDI files.

    Returns:
    - list: A list of dictionaries, each containing Mel2Word data for a MIDI file.
    """
    onlyfiles = sorted([f for f in listdir(midi_path) if isfile(join(midi_path, f))])
    M2W_dataset = []
    error_midi_files = []

    for idx, midi_name in enumerate(onlyfiles):
        midi_file_path = join(midi_path, midi_name)
        try:
            melody = get_midi(midi_file_path)
            midi = {'f_name': midi_name, 
                    'M2W_pitch': get_M2W(melody, feat='pitch'),
                    'M2W_rhythm': get_M2W(melody, feat='rhythm'),
                    'M2W_all': get_M2W(melody, feat='all')}
            M2W_dataset.append(midi)

            if (idx + 1) % 1 == 0:
                print(f"{idx + 1} of {len(onlyfiles)} files processed..")
        except Exception as e:
            print(f'ERROR ON {midi_name}: {e}..skipping the file..')
            error_midi_files.append(midi_name)

    print(f'Done. Processed {len(M2W_dataset)} files with {len(error_midi_files)} errors.')
    return M2W_dataset 


"""## Converting MIDI to Mel2Word Format

The `get_M2W_from_midipath()` function transforms a MIDI file into a Mel2Word representation. This includes options for pitch, rhythm, or both, based on the parameter: 1 (pitch), 2 (rhythm), or 3 (both - default).

###Transforming a Multiple MIDI Files to Mel2Word
You can use the `get_M2W_dataset()` function with the `midipath` of your file to convert your MIDI file into the Mel2Word format.

With `get_M2W_dataset()`, the data is stored as dictionaries with these keys: ['f_name', 'M2W_pitch', 'M2W_rhythm', 'M2W_all'], representing file names, transformed pitch, rhythm, and combined pitch-rhythm information.

##Mel2Word Dictionaries

To tokenize your melodies, you need a dictionary. Here are examples of either loading an existing word dictionary or creating new dictionary.

###Pre-generated dictionaries

If you want to use a pre-trained dictionary, you can easily load it using `load_dictionary()`. Additionally, customization is possible based on your needs, such as adjusting the existing dictionary size or maximum unit length using the `get_customed_dictionary()`. Here's the code and an example:
"""

# @title Codes for Pre-Generated Dictionaries

def load_dictionary(path):
    """
    Load a dictionary from a given file path.

    Parameters:
    - path (str): The file path to the dictionary.

    Returns:
    - dict: The loaded dictionary.
    """
    with open(path, 'rb') as handle:
        return pickle.load(handle)

def get_customed_dictionary(dictionary, dic_size, min_freq=10, max_length=10):
    """
    Build a custom dictionary.

    Parameters:
    - dictionary (dict): The input dictionary containing token occurrences.
    - dic_size (int or str): The desired size of the resulting dictionary; can be an integer or 'Full' for the full size.
    - min_freq (int): The minimum number of occurrences (frequency) for a token to be included in the dictionary.
    - max_length (int): The maximum length (number of tokens) a token can have to be included in the dictionary.

    Returns:
    - dict: The built custom dictionary.
    """

    sorted_vocs = sorted(dictionary.items(), key=lambda t: t[1], reverse=True)

    vocs = {}
    for idx, (word, count) in enumerate(sorted_vocs):
        if len(word.split('_')) <= max_length and len(word.split('_')) > 1 and count > min_freq:
            vocs[word] = count
            if len(vocs) == dic_size:
                break


    if dic_size > len(vocs):
        print('Dictionary size too large..Get full-size dictionary of..', len(vocs))
    else:
        print('Getting', len(vocs), 'sized dictionary')

    return vocs

"""###Generate new dictionary
You can create a new dictionary using your own dataset. The functions `BPE()` convert the dataset into the Mel2Word format and use Byte-Pair Encoding (BPE) to generate the dictionary. With `BPE()`, you obtain a dictionary in the form of a dictionary with the structure 'M2W: Frequency'.
"""

# @title Codes for generating new dictionary


def BPE(db, feat=3, dic_size=100, min_freq=10, max_length=11):
    """
    Builds a dictionary using Byte-Pair Encoding on a given dataset.

    Parameters:
    - db (list): The dataset containing M2W representations for each MIDI file.
    - feat (int, optional): The feature to consider for byte-pair encoding (1 for 'pitch', 2 for 'rhythm', 3 for 'all'). Defaults to 3.
    - dic_size (int, optional): The desired size of the resulting byte-pair dictionary. Defaults to 100.
    - min_freq (int, optional): The minimum frequency threshold for byte-pairs to be considered during dictionary construction. Defaults to 10.
    - max_length (int, optional): The maximum length of byte-pairs to be considered during dictionary construction. Defaults to 11.

    Returns:
    - dict: The generated dictionary.
    """
    words = []

    feat_mapping = {1: 'pitch', 2: 'rhythm', 3: 'all'}
    feat_str = feat_mapping.get(feat, 'all')

    # Concatenate M2W representations for the specified feature
    for mid in db:
        words += mid['M2W_' + feat_str]

    bpvocs = len(Counter(words).keys())
    print('starting byte-paring with iteration of..', dic_size, 'for', feat_str)

    db, bp_stat = prep_for_bytepair(db, feat_str)

    while True:
        # Get the most frequent byte-pair
        bpword, pre_freq = get_bped_word(db, 'bped', bp_stat, max_length)

        # Break the loop if the frequency is below the specified minimum
        if pre_freq <= min_freq:
            break

        tfreq = 0

        # Apply the byte-pair encoding to each MIDI in the dataset
        for midi in db:
            midi['bped'], freq = encode_bytepair(midi['bped'], bpword)
            tfreq += freq

        bp_stat[bpword] = tfreq
        vocsize = len(bp_stat)

        if vocsize % 100 == 0:
            print(vocsize, 'done...')

        if vocsize == dic_size:
            dictionary = {}
            dictionary.update(bp_stat)
            dictionary.update(dict(Counter(words)))
            break

    dictionary = {}
    dictionary.update(bp_stat)
    dictionary.update(dict(Counter(words)))
    dictionary = {k: v for k, v in sorted({**bp_stat, **Counter(words)}.items(), key=lambda item: item[1], reverse=True)}

    token_dictionary = {key: value for key, value in dictionary.items() if '_' in key}

    print('New BPE dictionary was built with', len(token_dictionary), 'of tokens')

    return token_dictionary


def encode_bytepair(seq, target_pair):
    """
    Encodes a given sequence by replacing a specified byte-pair with a single token.

    Parameters:
    - seq (list): The sequence to be encoded.
    - target_pair (str): The byte-pair to be encoded.

    Returns:
    - tuple: A tuple containing the encoded sequence and the count of the encoded byte-pair.
    """
    # Encode a byte-pair in the sequence
    for idx in range(len(seq) - 1):
        bp_word = seq[idx] + '_' + seq[idx + 1]

        if target_pair == bp_word:
            bped = '.'.join(seq)
            bped = bped.replace('.' + seq[idx] + '.' + seq[idx + 1] + '.', '.' + target_pair + '.')
            bped = bped.replace('.' + seq[idx] + '.' + seq[idx + 1] + '.', '.' + target_pair + '.')  # to avoid consecutive bp

            # Handle exceptions for the beginning and end of the sequence
            if idx == 0:  # exception (begin)
                bped = bped.replace(seq[idx] + '.' + seq[idx + 1] + '.', target_pair + '.')
            elif idx == len(seq) - 1:  # exception (end)
                bped = bped.replace('.' + seq[idx] + '.' + seq[idx + 1], '.' + target_pair)

            return bped.split('.'), bped.split('.').count(target_pair)

    return seq, 0


def check_bped_word(freq, bp_list):
    """
    Checks if a byte-pair is in the provided list.

    Parameters:
    - freq (list): The frequency list of byte-pairs.
    - bp_list (dict): The list of byte-pairs to check against.

    Returns:
    - tuple: A tuple containing the byte-pair and its frequency.
    """
    for bp in freq:
        if bp[0] not in bp_list.keys():
            return bp[0], bp[1]
    assert 'CHECK ERROR IN BPED WORD'


def get_bped_word(db, mode, bp_list=None, max_bp_len=12):
    """
    Retrieves the most frequent byte-pair from a database.

    Parameters:
    - db (list): The dataset containing M2W representations for each MIDI file.
    - mode (str): The mode of the sequences in the database.
    - bp_list (dict, optional): An existing list of byte-pairs. Defaults to None.
    - max_bp_len (int, optional): The maximum length of a byte-pair. Defaults to 12.

    Returns:
    - tuple: The most frequent byte-pair and its frequency.
    """
    freq = {}

    # Count frequencies of byte-pairs
    for midi in db:
        seq = midi[mode]
        for idx in range(len(seq) - 1):
            bp_word = seq[idx] + '_' + seq[idx + 1]

            if len(bp_word.split('_')) <= max_bp_len:
                freq[bp_word] = freq.get(bp_word, 0) + 1

    # Sort frequencies
    sfreq = sorted(freq.items(), key=lambda t: t[1], reverse=True)

    if bp_list is not None:
        return check_bped_word(sfreq, bp_list)

    return sfreq[0][0], sfreq[0][1]


def prep_for_bytepair(db, feat):
    """
    Prepares a dataset for byte-pair encoding.

    Parameters:
    - db (list): The database to be prepared.
    - feat (str): The feature to be considered in the database.

    Returns:
    - tuple: A tuple containing the prepared database and byte-pair statistics.
    """
    bp_stat = {}

    # Get the initial byte-pair
    bpword, pre_freq = get_bped_word(db, 'M2W_' + feat)

    tfreq = 0

    # Apply the byte-pair encoding to each MIDI in the dataset
    for midi in db:
        midi['bped'], freq = encode_bytepair(midi['M2W_' + feat], bpword)
        tfreq += freq

    bp_stat[bpword] = tfreq
    return db, bp_stat

"""##Tokenization

Now that you have a dictionary for tokenization, you can tokenize your melodies based on that dictionary using the function `get_M2W_tokens()` and `get_M2W_token_for_dataset()`.
"""

# @title Code for Tokenization



def get_dictionary_by_occurrence(dictionary, dic_size, min_freq=10, max_length=10):
    """
    Create a dictionary based on token occurrence.

    Parameters:
    - dictionary (dict): The input dictionary with token occurrences.
    - dic_size (int or str): Desired dictionary size (integer or 'Full' for full size).
    - min_freq (int): Minimum token occurrence frequency for inclusion.
    - max_length (int): Maximum token length for inclusion.

    Returns:
    - dict: The generated dictionary based on token occurrence.
    """

    sorted_vocs = sorted(dictionary.items(), key=lambda t: t[1], reverse=True)

    vocs = {}
    for idx, (word, count) in enumerate(sorted_vocs):
        if len(word.split('_')) <= max_length and len(word.split('_')) > 1 and count > min_freq:
            vocs[word] = count
            if len(vocs) == dic_size:
                break


    if dic_size > len(vocs):
        print('Dictionary size too large..Get full-size dictionary of..', len(vocs))
    else:
        print('Gettinng', len(vocs), 'sized dictionary')

    return vocs


    # sorted_vocs = sorted(dictionary.items(), key=lambda t: t[1], reverse=True)
    # dic_size = min(dic_size, 100000) if dic_size != 'Full' else 100000

    # vocs = {i: dictionary[i] for i, _ in sorted_vocs if len(i.split('_')) <= max_length and len(i.split('_')) > 1 and dictionary[i] > min_freq}

    # if dic_size > len(vocs):
    #     print('Dictionary size too large..Get full-size dictionary of..', len(vocs))
    # else:
    #     print('Getting', dic_size, 'sized dictionary')
    # return vocs


def get_dictionary_by_length(dictionary, dic_size, min_freq=10, max_length=11):
    """
    Build a dictionary based on length.

    Parameters:
    - dictionary (dict): The input dictionary containing token occurrences.
    - dic_size (int or str): The desired size of the resulting dictionary; can be an integer or 'Full' for the full size.
    - min_freq (int): The minimum number of occurrences (frequency) for a token to be included in the dictionary.
    - max_length (int): The maximum length (number of tokens) a token can have to be included in the dictionary.

    Returns:
    - dict: The built dictionary organized by length.
    """
    vocs = get_dictionary_by_occurrence(dictionary, dic_size, min_freq, max_length)
    maxlen = max(len(i.split('_')) for i in vocs)
    vocdic = {str(lth): [i for i in vocs if len(i.split('_')) == lth] for lth in range(maxlen, 1, -1)}
    return vocdic


def tokenize_single_M2W_seq(dic, M2W):
    """
    Tokenizes a list of M2W sequence(a single melody) based on a provided dictionary.

    Parameters:
    - dic (dict): A dictionary where each key represents the length of the token and each value is a list of tokens.
                  The dictionary is used to match and tokenize elements in the M2W list.
    - M2W (list): A list of M2W representations (strings) that are to be tokenized using the provided dictionary.

    Returns:
    - list: A list of tokenized M2W representations.
    """
    dic['1'] = []
    indices = []
    midi = M2W.copy()
    lths = list(dic.keys())
    lentmp = int(lths[0])
    cc = 0
    voc_dic = []

    for mlen in dic:
        for vocss in dic[mlen]:
            for idx, voctmp in enumerate(midi):
                vocstmp = midi[idx:idx + lentmp]
                mvocs = ('_').join(vocstmp)
                if vocss == mvocs:
                    vocstmp = [str(cc) + '.' + s + '.' + str(mlen) for s in vocstmp]
                    midi[idx:idx + lentmp] = vocstmp
                    cc = cc + 1
                    voc_dic.append(vocstmp)
        lentmp = lentmp - 1

    try:
        itr = int(voc_dic[-1][1].split('.')[0])
        for ct in range(0, itr + 1):
            for idx, voc in enumerate(midi):
                if not voc == 'none':
                    if len(voc.split('.')) == 3:
                        cnt = str(ct)
                        lth = int(voc.split('.')[-1])

                        if voc[0] == cnt:
                            voc_tmp = []
                            for i in range(lth):
                                voc_tmp.append((midi[idx + i].split('.')[1]))

                            del midi[idx:idx + lth]

                            for i in range(lth):
                                if i == 0:
                                    midi.insert(idx, ('_').join(voc_tmp))
                                else:
                                    midi.insert(idx + i, 'none')

    except:
        print('Nothing to tokenize..(Check the dictionary feature properties.)')

    assert len(midi) == len(M2W)
    midi = [i for i in midi if i != 'none']
    M2Wtoken = midi
    return M2Wtoken


def get_M2W_tokens(M2W, dictionary, dic_size=100, feat=3):
    """
    Tokenizes Mel2Word data using a given dictionary.

    Parameters:
    - M2W (list): List of M2W representations to be tokenized.
    - dictionary (dict): The dictionary used for tokenization.
    - dic_size (int, optional): The size of the dictionary to be used. Defaults to 100.
    - feat (int, optional): The feature type (1 for 'pitch', 2 for 'rhythm', 3 for 'all'). Defaults to 3.

    Returns:
    - list: The tokenized Mel2Word data.
    """
    feat_str = None

    M2Wk = max(dictionary, key=dictionary.get).split('_')[0]

    print('M2W for Data Example:',M2W[0])
    print('M2W for Dictionary Example:',M2Wk)

    if feat == 1:
      feat_str = 'Pitch' if len(M2W[0]) == 3 and not M2W[0].isdigit() and not M2Wk.isdigit() and len(M2Wk) == 3 else None
    elif feat == 2:
      feat_str = 'Rhythm' if M2W[0].isdigit() and M2Wk.isdigit() else None
    elif feat == 3:
        feat_str = 'All' if len(M2Wk[0]) > 3 and not M2W.isdigit() else None
    else:
        print("Error!!: Please check the feat value.")
        return None

    if feat_str is not None:
        print(f"Processing Dictionary for {feat_str} Feature")

        if feat_str == 'pitch':
            print('Tokenization for Pitch Feature..')
        elif feat_str == 'rhythm':
            print('Tokenization for Rhythm Feature..')

        dic = get_dictionary_by_length(dictionary, dic_size)

        return tokenize_single_M2W_seq(dic, M2W)

    else:
        print("ERROR!!!!!!!!!!:Check if the features of the dictionary match the specified feature...")

        M2Wfeat = 'Pitch' if len(M2W[0]) == 3 and not M2W[0].isdigit() else 'Rhythm' if M2W[0].isdigit() else 'All'
        dicfeat = 'Pitch' if len(M2Wk[0]) == 3 and not M2Wk[0].isdigit() else 'Rhythm' if M2Wk[0].isdigit() else 'All'

        print("See examples - Mel2Word Example:", M2W[0], f'({M2Wfeat})', "Dictionary Example:", M2Wk[0], f'({dicfeat})')

        return None


def get_M2W_tokenized_dataset(data, dictionary, feat=3, dic_size=100, min_num=10, max_length=11):
    """
    Tokenize Mel2Word representations in a dataset using a custom dictionary.

    Parameters:
    - data (list of dicts): List of dictionaries containing Mel2Word representations.
    - dictionary (dict): Custom dictionary for tokenization.
    - feat (int): Feature option for tokenization (1 for pitch, 2 for rhythm, 3 for both).
    - dic_size (int): Desired dictionary size.
    - min_num (int): Minimum frequency threshold for tokenization.
    - max_length (int): Maximum length of tokens for tokenization.

    Returns:
    - list of dicts: Updated dataset with tokenized Mel2Word representations.
    """
    print('Processing M2W tokenization for dataset for feature:', ['M2W_pitch' if feat == 1 else 'M2W_rhythm' if feat == 2 else 'M2W_all'])


    # Generate a custom dictionary based on length
    dic = get_dictionary_by_length(dictionary, dic_size, min_num, max_length)
    M2Wk = max(dictionary, key=dictionary.get).split('_')[0]
    M2W = data[0]['M2W_pitch' if feat == 1 else 'M2W_rhythm' if feat == 2 else 'M2W_all']
    print('M2W for Data Example:',M2W[0])
    print('M2W for Dictionary Example:',M2Wk)
    if feat == 1:
      feat_str = 'Pitch' if len(M2W[0])==3 and not M2W[0].isdigit() and len(M2Wk)==3 and not M2Wk.isdigit()  else None
    elif feat == 2:
      feat_str = 'Rhythm' if M2W[0].isdigit() and M2Wk.isdigit() else None
    elif feat == 3:
        feat_str = 'All' if len(M2W[0]) > 3 and len(M2Wk) > 3  else None
    else:
        print("Error!!: Please check the feat value.")
        return None

    if feat_str is not None:

      # Iterate through each song in the dataset
      for sidx, song in enumerate(data):
          M2W = song['M2W_pitch' if feat == 1 else 'M2W_rhythm' if feat == 2 else 'M2W_all']

          M2W_tokenized = tokenize_single_M2W_seq(dic, M2W)

          song['token_pitch' if feat == 1 else 'token_rhythm' if feat == 2 else 'token_all'] = M2W_tokenized

          if sidx % 100 == 0:
              print('Tokenization done for', song['f_name'], sidx + 1, '/', len(data))
    else:
      print("ERROR!!!!!!!!!!:Check if the features of the dictionary match the specified feature...")

      M2Wfeat = 'Pitch' if len(M2W[0]) == 3 and not M2W[0].isdigit() else 'Rhythm' if M2W[0].isdigit() else 'All'
      dicfeat = 'Pitch' if len(M2Wk[0]) == 3 and not M2Wk[0].isdigit() else 'Rhythm' if M2Wk[0].isdigit() else 'All'

      print("See examples - Mel2Word Example:", M2W[0], f'({M2Wfeat})', "Dictionary Example:", M2Wk, f'({dicfeat})')


    return data

"""### Tokenization for a Single MIDI File

You can tokenize individual melodies that have been converted to Mel2Word (M2W) representations into M2W vocabularies using the `get_M2W_tokens()` function. To extract M2W features from MIDI, you can refer to the `get_M2W_from_midipath()` function above.

### Tokenization for Multiple MIDI Data

You can tokenize the entire dataset using the `get_M2W_tokens_for_dataset` function. To do this, provide the M2W-processed dataset and the generated dictionary. To convert the entire dataset to M2W representations using a data folder path, you can refer to the `get_M2W_dataset()` function mentioned earlier.

Notice that the data is in list format, with tokenized melodies stored under keys like 'token_pitch,' 'token_rhythm,' or 'token_all' based on the feature (pitch, rhythm, or all).

##Usage

This approach offers the advantage of enabling the direct application of existing NLP algorithms to string-format melodies. To illustrate this, let's explore two examples:

1. Visualizing Word Importance with a WordCloud: We can utilize word frequency to visualize the importance of words in a WordCloud.

2. Creating Distribution Representations of Word Contexts using Word2Vec: We can employ the Word2Vec approach to generate distribution representations of word contexts.

When selecting features for these examples, you have the option to choose from morpheme-level features like:

- 'M2W_pitch'
- 'M2W_rhythm'
- 'M2W_all'

Alternatively, you can use tokenized features such as:

- 'token_pitch'
- 'token_rhythm'
- 'token_all'

Your choice will depend on your specific tokenization approach.

You can choose to use your own custom tokenized data or utilize the pre-tokenized MTC-ANN dataset that we have provided at [https://github.com/saebyulpark/Mel2word](https://github.com/saebyulpark/Mel2word).
"""

# @title Code for WordCloud

# Import necessary libraries
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def Get_WordCloud_for_M2W(data, feat):
    """
    Generate a Word Cloud for a specific feature (M2W_pitch, M2W_all, etc.) in the given dataset.

    Args:
        data (list): List of dictionaries containing song data.
        feat (str): The feature to visualize using a Word Cloud.

    Returns:
        None
    """
    # Check if the feature is 'M2W_rhythm'
    if feat == 'M2W_rhythm':
        print("Error!!: The current WordCloud implementation struggles to handle text consisting solely of numbers.")
        print("Please consider using a different feature for analysis.")
    else:
        # Extract the specified feature from the dataset
        feature_data = [song[feat] for song in data]
        filtered_data = [[element for element in sublist if len(element.split('_')) > 1] for sublist in feature_data] #removing morphemes

        # Flatten the list of feature data into a single string
        all_text = ' '.join([' '.join(song_text) for song_text in filtered_data])

        # Create a WordCloud object
        wordcloud = WordCloud(width=300, height=200, background_color='white').generate(all_text)

        # Display the Word Cloud
        plt.figure(figsize=(7, 4))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.title(f'Word Cloud for {feat.upper()}')
        plt.axis('off')
        plt.show()

# @title Code for Word2Vec
import gensim
from gensim.models import Word2Vec
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import numpy as np

def create_word2vec_model_for_M2W(data, feat, vector_size=100, window=5, min_count=1, epochs=300):
    """
    Create a Word2Vec model for a specific feature in the data.

    Parameters:
    data (list of dict): List of data points where each dict contains the specified feature.
    feat (str): The key of the feature to create Word2Vec embeddings for.
    vector_size (int): Dimensionality of the word vectors.
    window (int): Maximum distance between the current and predicted word within a sentence.
    min_count (int): Ignores all words with a total frequency lower than this.
    epochs (int): Number of iterations over the dataset.

    Returns:
    Word2Vec: Word2Vec model trained on the specified feature.
    """
    # Extract the feature data
    feature_data = [song[feat] for song in data]

    # Train a Word2Vec model
    model = Word2Vec(feature_data, vector_size=vector_size, window=window, min_count=min_count, epochs=epochs)

    return model


def get_word2vec_visualization(model, num_top_words):
    """
    Visualize word embeddings using t-SNE for the top N words in the model's vocabulary.

    Parameters:
    model (Word2Vec): The Word2Vec model.
    num_top_words (int): Number of top words to visualize.

    Returns:
    None (displays a plot).
    """
    # Get the top N words by frequency
    top_words = model.wv.index_to_key[:num_top_words]

    # Extract word vectors for the top words
    word_vectors = np.array([model.wv[word] for word in top_words])

    # Apply t-SNE for dimensionality reduction
    tsne = TSNE(n_components=2, perplexity=10, random_state=42)
    word_vectors_2d = tsne.fit_transform(word_vectors)

    # Visualize the word vectors
    plt.figure(figsize=(8, 6))
    for i, word in enumerate(top_words):
        x, y = word_vectors_2d[i]
        plt.scatter(x, y)
        plt.annotate(word, xy=(x, y), xytext=(5, 2), textcoords='offset points', ha='right', va='bottom', fontsize=8)

    plt.title(f"Word2Vec Word Embeddings Visualization (Top {num_top_words} Words)")
    plt.xlabel("t-SNE Dimension 1")
    plt.ylabel("t-SNE Dimension 2")
    plt.show()

"""Generate Word2Vec embeddings for your chosen feature by specifying the 'feat' key.

With this Word2Vec model, you can perform various tasks with your trained Word2Vec model. Here are some simple tasks you can do.

## Reconstructing Mel2Word to MIDI

You can use the `Mel2midi` function to convert Mel2Word-encoded melodies into MIDI files, allowing playback and editing in standard music software. Simply provide a list of melodies encoded as 'M2W_all' or 'token_all' feature, which includes both pitch and rhythm information, and specify the desired file name for saving the MIDI file.
"""

# @title Code for MIDI Generation from Mel2Word

def Mel2midi(song,file_path, first_pitch = 69, last_beat=4):
    """
    Converts a Mel2Word encoded melody into a MIDI file.

    Parameters:
    - song (list): List of Mel2Word encoded tokens.
    - file_path (str): Path to save the MIDI file.
    - first_pitch (int): The pitch value for the first note (default is MIDI note 69, middle A).
    - first_beat (int): The beat value for the first note (default is 1).
    - last_beat (int): The beat value for the last note (default is 4).

    Returns:
    None
    """

    formidi=[]
    for i, tok in enumerate(song):
        tmp=tok.split('_')
        formidi+=tmp

    get_pitch=[first_pitch]
    get_beat=[]


    #pitch
    for i,com in enumerate(formidi):
        if com[0] == 'U':
            note_pitch=get_pitch[-1]+int(com[1:3])
            get_pitch.append(note_pitch)
        elif com[0] == 'D':
            note_pitch=get_pitch[-1]-int(com[1:3])
            get_pitch.append(note_pitch)
        elif com[0] =='E':
            get_pitch.append(get_pitch[-1])


    for i,com in enumerate(formidi):
        note_beat=int(com[3:7])/100
        get_beat.append(note_beat)
    get_beat.append(last_beat)

    notes = []
    for i, pitch_tmp in enumerate(get_pitch):
        n = note.Note(pitch_tmp)
        n.quarterLength = get_beat[i]
        notes.append(n)
    s = stream.Stream()
    s.append(notes)
    mf = midi.translate.streamToMidiFile(s)
    mf.open(file_path, 'wb')
    mf.write()
    mf.close()
    print('midifile written to..', file_path)

"""NOTE: Keep in mind that the conversion process involves quantization and the use of relative values, which may result in imperfect restoration. Thus, manual adjustment of the values for the first and last notes may be necessary. Be aware that this function is substandard and may require adjustments to suit your specific research needs.

#Contact

If you have any issues, inquiries, or are interested in collaborative research, please feel free to contact us at saebyulsb@gmail.com
"""
