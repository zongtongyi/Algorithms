#!/usr/bin/env python
# -*- coding:utf-8 -*-
# TF-IDF: 
# Theory refered: http://www.ruanyifeng.com/blog/2013/03/automatic_summarization.html
# code refered: 
#

import sys, codecs
from Trie.Trie_mmseg import *
from MMSEG import *

class Summarizer(object):
    def __init__(self, mmseg, target_doc, idf_file):
        self.idf_trie = Trie()
        self.key_ranklist = []
        self.target_doc = target_doc

        with codecs.open(idf_file, 'r', 'utf-8') as f:
            for line in f.readlines():
                word, tf = line.split(' ')
                self.idf_trie.insert_tf(word, float(tf))

        with open(target_doc) as f:
            target_doc_TF_Trie, target_doc_TFxIDF_trie, target_doc_max5_trie = Trie(), Trie(), Trie()
            for line in f.readlines():
                [target_doc_TF_Trie.insert(word) for word in mmseg.word_seg_complex(line.decode('utf-8'))]

            for word, tf in target_doc_TF_Trie.traverse_BFS():
                result = self.idf_trie.search_tf(word)
                idf_value = 14.00000000000 if not result[0] else result[1][0][1]
                target_doc_TFxIDF_trie.insert_tf(word, tf * idf_value)
            
            target_doc_TFxIDF_trie.fill_max_trie(target_doc_max5_trie, 5)
            target_doc_max5_trie.item_list(self.key_ranklist)
            self.key_ranklist.sort(key=lambda x: -x[0])
            pass

    def simplify_summarizer(self):
        # sentence segment
        sentences = []
        juzi = ''
        with codecs.open(target_doc, 'r', 'utf-8') as f:
            for line in f.readlines:
                i, j = 0, 0
                for c in line:
                    if c=='，'.decode('utf-8') or c==',' or c=='。'.decode('utf-8') or c=='.':
                        sentences.append(line[i:j])
                        i = j + 1
                    else:
                        j += 1

        summary_sentences = set()
        summary_sentences_n, i = 4, 0
        for key in self.key_ranklist:
            for juzi in sentences:
                if key in juzi:
                    summary_sentences.add(juzi)
                    i += 1
                    if i == summary_sentences_n:
                        break

        return summary_sentences



if __name__ == '__main__':
    tree = Trie()
    [tree.insert_tf(word, int(tf)) for word, tf in [(line.split()[0].decode('utf-8'), line.split()[1]) for line in open('./lexicon/open-gram-m7.u8.lexicon').readlines()]]
    mmseg = MMSEG(tree)

    pass