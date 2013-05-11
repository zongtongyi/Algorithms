#!/usr/bin/env python
# -*- coding:utf-8 -*-
# MMSEG: A Word Identification System for Mandarin Chinese Text Based on Two Variants of the Maximum Matching Algorithm
# Theory refered: http://technology.chtsai.org/mmseg/
# code refered: 
#

import math
from Trie_mmseg import *

class Chunk(object):
    def __init__(self, tri_word_list, tf_list):
        self.w1, self.w2, self.w3 = tri_word_list
        # Rule1: Maximum Matching
        self.rule1 = self.length = len(self.w1) + len(self.w2) + len(self.w3)
        # Rule2: Largest average word length
        self.rule2 = self.avg_len = float(self.length) / 3
        # Rule3: Smallest variance of word lengths
        self.rule3 = self.variance = ( (len(self.w1)-self.avg_len)**2 + (len(self.w2)-self.avg_len)**2 + (len(self.w3)-self.avg_len)**2 ) / 3
        # Rule4: Largest sum of degree of morphemic freedom of one-character words
        self.sum_log_frequency = 0
        for tf in tf_list:
            log_single = 0 if tf==0 else math.log(tf)
            self.sum_log_frequency += log_single
        self.rule4 = self.sum_log_frequency

    def __lt__(self, obj):
        if [self.rule1, self.rule2, -(self.rule3), self.rule4] < [obj.rule1, obj.rule2, -(obj.rule3), obj.rule4]:
            return True
        else:
            return False

class MMSEG(object):
    def __init__(self, lexicon):
        self.lexicon = lexicon
        self.max_word_len = lexicon.max_word_length()

    def word_seg_simple(self, corpus):
        corpus_seg = ''
        i, j, corpus_len = 0, 0, len(corpus)
        while i < corpus_len:
            s = corpus[i:min(i + self.max_word_len, corpus_len)]
            find, match = self.lexicon.search(s) # prefix match
            j = (i + 1) if len(match)==0 and find==False else ( i + len(match[-1]) )
            corpus_seg += corpus[i:j] + '/'
            i = j
        print corpus_seg

    def word_seg_complex(self, corpus):
        i, i = 0, 0
        corpus_len, corpus_seg = len(corpus), ''
        chunk_list = []
        while i < corpus_len:
            s = corpus[i:min(i + self.max_word_len, corpus_len)]
            find, match = self.lexicon.search_tf(s) # prefix match
            tri_word_list, tf_list = [], []
            for word, tf in match:
                tri_word_list.append(word)
                tf_list.append(0 if len(word)!=0 else tf)
                i2 = i + len(word)
                s2 = corpus[i2:min(i2+self.max_word_len, corpus_len)]
                find2, match2 = self.lexicon.search_tf(s2)
                for word2, tf2 in match2:
                    tri_word_list.append(word2)
                    tf_list.append(0 if len(word2)!=0 else tf2)
                    i3 = i2 + len(word2)
                    s3 = corpus[i3:min(i3+self.max_word_len, corpus_len)]
                    find3, match3 = self.lexicon.search_tf(s3)
                    for word3, tf3 in match3:
                        tri_word_list.append(word3)
                        tf_list.append(0 if len(word3)!=0 else tf3)
                        chunk_list.append(Chunk(tri_word_list, tf_list))
                        tri_word_list.pop()
                    tri_word_list.pop()
                tri_word_list.pop()

            if len(chunk_list) == 0: # unknow word found (which not included in lexicon)
                j = i + 1
            else:
                best_seg = max(chunk_list)
                j = i + len(best_seg.w1)
            corpus_seg += corpus[i:j] + '/'
            i = j

        print corpus_seg


if __name__ == '__main__':
    words_list = [(line.split()[0].decode('utf-8'), line.split()[1]) for line in open('./lexicon/open-gram-m7.u8.lexicon').readlines()]
    tree = Trie()
    [tree.insert_tf(word, tf) for word, tf in words_list]

    mmseg = MMSEG(tree)
    corpus = "吃葡萄不吐葡萄皮，不吃葡萄到吐葡萄皮"
    mmseg.word_seg_simple(corpus.decode('utf-8'))

    corpus = "研究生命起源"
    mmseg.word_seg_complex(corpus.decode('utf-8'))

    pass
