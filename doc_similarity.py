#!/usr/bin/env python
# -*- coding:utf-8 -*-
# TF-IDF: 
# Theory refered: http://www.ruanyifeng.com/blog/2013/03/tf-idf.html
# code refered: 
#

import copy, codecs, sys
from MMSEG import *
from Trie.Trie_mmseg import *


class TFxIDF_list(object):
    def __init__(self, mmseg, target_doc_list, idf_file):
        self.target_doc_TFxIDF_maxtrie_dict = {}
        self.target_doc_TFxIDF_vector_dict = {}
        self.idf_trie = Trie()

        with codecs.open(idf_file, 'r', 'utf-8') as f:
            for line in f.readlines():
                word, tf = line.split(' ')
                self.idf_trie.insert_tf(word, float(tf))

        for target_doc in target_doc_list:
            with open(target_doc) as f:
                target_doc_TF_Trie, target_doc_TFxIDF_trie, target_doc_max5_trie = Trie(), Trie(), Trie()

                for line in f.readlines():
                    [target_doc_TF_Trie.insert(word) for word in mmseg.word_seg_complex(line.decode('utf-8'))]
                
                for word, tf in target_doc_TF_Trie.traverse_BFS():
                    result = self.idf_trie.search_tf(word)
                    idf_value = 14.00000000000 if not result[0] else result[1][0][1] # if a unknown word found(idf-file haven't include this word), then this word has a very high IDF value
                    target_doc_TFxIDF_trie.insert_tf(word, tf * idf_value)
                
                target_doc_TFxIDF_trie.fill_max_trie(target_doc_max5_trie, 5)
                self.target_doc_TFxIDF_maxtrie_dict[target_doc] = target_doc_max5_trie

    def print_maxtrie_dict(self):
        print_word=lambda x:sys.stdout.write(x+' ')
        for k, v in self.target_doc_TFxIDF_maxtrie_dict.iteritems():
            print 'doc:', k
            [print_word(word) for word, _ in v.traverse_BFS()]
            print '\n'

    @property
    def TFxIDF_maxtrie_dict(self):
        return copy.deepcopy(self.target_doc_TFxIDF_maxtrie_dict)
 

def fill_dimension_trie(TFxIDF_maxtrie_dict, dimension_trie):
    [[dimension_trie.insert_0tf(word) for word, _ in v.traverse_BFS()] for _, v in TFxIDF_maxtrie_dict.iteritems()]


def TFxIDF_vector_expand(TFxIDF_maxtrie_dict, dimension_trie):
    TFxIDF_vector_dict = {}
    for k, v in TFxIDF_maxtrie_dict.iteritems():
        vector_trie = copy.deepcopy(dimension_trie)
        vector_trie.merge_tf(v)
        vector_list = []
        vector_trie.item_list(vector_list)
        TFxIDF_vector_dict[k] = [vector for vector, _ in vector_list]

    pass



if __name__ == '__main__':
    tree = Trie()
    [tree.insert_tf(word, int(tf)) for word, tf in [(line.split()[0].decode('utf-8'), line.split()[1]) for line in open('./lexicon/open-gram-m7.u8.lexicon').readlines()]]
    mmseg = MMSEG(tree)

    target_doc_list = ['corpus/target_doc.txt', 'corpus/target_doc2.txt']
    tfidf_list = TFxIDF_list(mmseg, target_doc_list, 'corpus/386194-idf_sougoug_news_allsites.utf8')
    tfidf_list.print_maxtrie_dict()
    TFxIDF_maxtrie_dict = tfidf_list.TFxIDF_maxtrie_dict
    dimension_trie = Trie()
    fill_dimension_trie(TFxIDF_maxtrie_dict, dimension_trie)
    TFxIDF_vector_expand(TFxIDF_maxtrie_dict, dimension_trie)
    pass



