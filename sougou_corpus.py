#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Corpus from Sougou.

import os, copy, math, codecs
import time
from MMSEG import *
from Trie.Trie_mmseg import *

class Sougou_Corpus(object):
    def __init__(self, mmseg, corpus_dir=''):
        self.mmseg, self.doc_count, self.corpus_file_list = mmseg, 0, []
        self.doc_tf_tree = Trie() # doc count that contain specific word
        for root, dirs, files in os.walk(corpus_dir):
            [self.corpus_file_list.append(os.path.join(root, filename)) for filename in files]

        # 2317164 / 6 = 386194 / 100 = 3861.94
        i, start_time = 0, time.clock()

        for filename in self.corpus_file_list:
            with open(filename) as f:
                for line in f.readlines():
                    if '<doc>' in line: # one <doc> section as one document
                        self.doc_count += 1
                        i += 1
                        if i%100 == 0:
                            print "Finished ", i
                    elif '<content>' in line:
                        doc_word_trie = Trie()
                        [doc_word_trie.insert_0tf(word) for word in self.mmseg.word_seg_complex(line[9:-10].decode('utf-8'))]
                        self.doc_tf_tree.merge(doc_word_trie)

        elapsed = time.clock() - start_time
        print "time spend:", elapsed

    def corpus_data(self):
        doc_tf_tree = copy.deepcopy(self.doc_tf_tree)
        return (self.doc_count, doc_tf_tree)

    def IDF_trie_2_file(self, IDF_trie_file=None):
        if not IDF_trie_file:
            IDF_trie_file = str(self.doc_count) + '-idf.utf8'
        with codecs.open(IDF_trie_file, 'w', 'utf-8') as f:
            idf_list = []
            for word, doc_tf in self.doc_tf_tree.traverse_BFS():
                idf = math.log( float(self.doc_count) / float(doc_tf + 1) )
                idf_list.append(word)
                idf_list.append(' ')
                idf_list.append(str(idf))
                idf_list.append('\n')
            f.write(''.join(idf_list))
            f.flush()

if __name__ == '__main__':
    tree = Trie()
    [tree.insert_tf(word, tf) for word, tf in [(line.split()[0].decode('utf-8'), line.split()[1]) for line in open('./lexicon/open-gram-m7.u8.lexicon').readlines()]]
    mmseg = MMSEG(tree)

    corpus = Sougou_Corpus(mmseg, 'corpus/sougou_corpus/')
    corpus_doc_count, corpus_doc_tf_tree = corpus.corpus_data()
    corpus.IDF_trie_2_file()
