#!/usr/bin/env python
# -*- coding:utf-8 -*-
# TF-IDF: 
# Theory refered: http://www.ruanyifeng.com/blog/2013/03/tf-idf.html
# code refered: 
#

import os, copy
import math
from MMSEG import *
from Trie.Trie_mmseg import *


class Sougou_Corpus(object):
    def __init__(self, mmseg, corpus_dir):
        self.mmseg, self.doc_count, self.corpus_file_list = mmseg, 0, []
        self.doc_tf_tree = Trie() # doc count that contain specific word
        for root, dirs, files in os.walk(corpus_dir):
            [self.corpus_file_list.append(os.path.join(root, filename)) for filename in files]

        for filename in self.corpus_file_list:
            with open(filename) as f:
                for line in f.readlines():
                    if '<doc>' in line: # one <doc> section as one document
                        self.doc_count += 1
                    elif '<content>' in line:
                        doc_word_trie = Trie()
                        [doc_word_trie.insert_0tf(word) for word in self.mmseg.word_seg_complex(line[9:-10].decode('utf-8'))]
                        self.doc_tf_tree.merge(doc_word_trie)

    def corpus_data(self):
        doc_tf_tree = copy.deepcopy(self.doc_tf_tree)
        return (self.doc_count, doc_tf_tree)


class TFxIDF(object):
    def __init__(self, mmseg, target_doc, corpus_data):
        self.mmseg, self.target_doc = mmseg, target_doc
        self.corpus_doc_count, self.corpus_doc_tf_tree = corpus_data
        self.target_doc_tf_tree = Trie()
        self.TFxIDF_Trie = Trie()

        # TF_calculate(self):
        with open(target_doc) as f:
            for line in f.readlines():
                [self.target_doc_tf_tree.insert(word) for word in self.mmseg.word_seg_complex(line.decode('utf-8'))]

    def TFxIDF_calculate(self):
        for word, tf in self.target_doc_tf_tree.traverse_BFS():
            result = self.corpus_doc_tf_tree.search_tf(word)
            doc_tf = 0 if not result[0] else result[1][0][1]
            self.TFxIDF_Trie.insert_tf( word, tf * math.log( self.corpus_doc_count / (doc_tf + 1) ) )

    def keyword_rank(self, rank_list):
        self.TFxIDF_Trie.item_list(rank_list)
        rank_list.sort()
        rank_list.reverse()


if __name__ == '__main__':
    tree = Trie()
    [tree.insert_tf(word, tf) for word, tf in [(line.split()[0].decode('utf-8'), line.split()[1]) for line in open('./lexicon/open-gram-m7.u8.lexicon').readlines()]]
    mmseg = MMSEG(tree)
    target_doc = 'corpus/target_doc.txt'
    corpus = Sougou_Corpus(mmseg, 'corpus/sougou_corpus/')

    tfidf = TFxIDF(mmseg, target_doc, corpus.corpus_data())
    tfidf.TFxIDF_calculate()
    rank_list = []
    tfidf.keyword_rank(rank_list)
    for i in range(10):
        print rank_list[i][1]
    pass

