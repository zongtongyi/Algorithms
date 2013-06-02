#!/usr/bin/env python
# -*- coding:utf-8 -*-
# TF-IDF: 
# Theory refered: http://www.ruanyifeng.com/blog/2013/03/tf-idf.html
# code refered: 
#

import math
from MMSEG import *
from Trie.Trie_mmseg import *
from sougou_corpus import *


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
            self.TFxIDF_Trie.insert_tf( word, tf * math.log( float(self.corpus_doc_count) / float(doc_tf + 1) ) )

    def keyword_rank(self, rank_list):
        self.TFxIDF_Trie.item_list(rank_list)
        rank_list.sort(key=lambda x: -x[0])


if __name__ == '__main__':
    tree = Trie()
    [tree.insert_tf(word, tf) for word, tf in [(line.split()[0].decode('utf-8'), line.split()[1]) for line in open('./lexicon/open-gram-m7.u8.lexicon').readlines()]]
    mmseg = MMSEG(tree)
    corpus = Sougou_Corpus(mmseg, 'corpus/sougou_corpus/')

    target_doc = 'corpus/target_doc.txt'
    tfidf = TFxIDF(mmseg, target_doc, corpus.corpus_data())
    tfidf.TFxIDF_calculate()
    rank_list = []
    tfidf.keyword_rank(rank_list)
    for i in range(10):
        print rank_list[i][1]
    pass

