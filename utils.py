#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import collections
import random

import numpy as np
import json


def read_data(filename):
    with open(filename, encoding="utf-8") as f:
        data = f.read()
    data = list(data)
    return data


def index_data(sentences, dictionary):
    shape = sentences.shape
    sentences = sentences.reshape([-1])
    index = np.zeros_like(sentences, dtype=np.int32)
    for i in range(len(sentences)):
        try:
            index[i] = dictionary[sentences[i]]
        except KeyError:
            index[i] = dictionary['UNK']

    return index.reshape(shape)

with open('dictionary.json', encoding='utf-8') as inf:
    dictionary = json.load(inf, encoding='utf-8')

def get_index(ch, dictionary):
    try:
        index = dictionary[ch]
    except KeyError:
        index = dictionary['UNK']
    return index

def get_train_data(vocabulary, batch_size, num_steps):
    # your code here
    raw_x = [get_index(ch,dictionary) for ch in vocabulary]
    raw_y = [get_index(ch,dictionary) for ch in vocabulary[1:]]
    data_length = len(vocabulary)
    batch_partition_length = data_length // batch_size
    
    data_x = np.zeros([batch_size, batch_partition_length], dtype=np.int32)
    data_y = np.zeros([batch_size, batch_partition_length], dtype=np.int32)
    
    for i in range(batch_size):
        data_x[i] = raw_x[batch_partition_length * i:batch_partition_length * (i+1)]
        data_y[i] = raw_y[batch_partition_length * i:batch_partition_length * (i+1)]
        
    epoch_size = batch_partition_length // num_steps
    
    for i in range(epoch_size):
        x = data_x[:, i * num_steps:(i + 1) * num_steps]
        y = data_y[:, i * num_steps:(i + 1) * num_steps]
        yield (x, y)



def build_dataset(words, n_words):
    """Process raw inputs into a dataset."""
    count = [['UNK', -1]]
    count.extend(collections.Counter(words).most_common(n_words - 1))
    dictionary = dict()
    for word, _ in count:
        dictionary[word] = len(dictionary)
    data = list()
    unk_count = 0
    for word in words:
        index = dictionary.get(word, 0)
        if index == 0:  # dictionary['UNK']
            unk_count += 1
        data.append(index)
    count[0][1] = unk_count
    reversed_dictionary = dict(zip(dictionary.values(), dictionary.keys()))
    return data, count, dictionary, reversed_dictionary
