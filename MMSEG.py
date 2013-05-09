#!/usr/bin/env python
# -*- coding:utf-8 -*-
# MMSEG: A Word Identification System for Mandarin Chinese Text Based on Two Variants of the Maximum Matching Algorithm
# Theory refered: http://technology.chtsai.org/mmseg/
# code refered: 
#

from Trie import *

class MMSEG(object):
    def __init__(self, lexicon):
        self.lexicon = lexicon
        self.max_word_len = lexicon.max_word_length()
        pass

    # Simple maximum matching
    def word_seg_simple(self, corpus):
        corpus_seg = ''
        i, j, corpus_len = 0, 0, len(corpus)
        while i < corpus_len:
            s = corpus[i:min(i + self.max_word_len, corpus_len)]
            find, match = self.lexicon.search(s)
            j = (i + 1) if len(match)==0 and find==False else ( i + len(match) )
            corpus_seg += corpus[i:j] + '/'
            i = j
            pass
        print corpus_seg


if __name__ == '__main__':
    words_list = [line.split()[0].decode('utf-8') for line in open('./lexicon/open-gram-m7.u8.lexicon').readlines()]
    words_list = [line.split()[0].decode('utf-8') for line in open('./lexicon/simpleNLP.lexicon').readlines()]
    tree = Trie()
    [tree.insert(word) for word in words_list]

    mmseg = MMSEG(tree)
    #corpus = "让我们荡起双桨一起来吐槽编程珠玑"
    corpus = "吃葡萄不吐葡萄皮，不吃葡萄到吐葡萄皮"
    mmseg.word_seg_simple(corpus.decode('utf-8'))
    pass