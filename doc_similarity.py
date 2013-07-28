#!/usr/bin/env python
# -*- coding:utf-8 -*-
# TF-IDF: 
# Theory refered: http://www.ruanyifeng.com/blog/2013/03/tf-idf.html    calculate cosine
# code refered: 
#

import copy, codecs, sys
import math
from MMSEG import *
from Trie.Trie_mmseg import *


class TFxIDF_list(object):
    def __init__(self, mmseg, target_doc_list, idf_file):
        #self.target_doc_TFxIDF_maxtrie_dict = {}
        self.idf_trie = Trie()
        self.target_doc_TFxIDF_vector_dict = {}
        self.target_doc_TF_maxtrie_dict = {}
        self.keywords_trie = Trie()
        self.keywords_count = 0

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
                    target_doc_TFxIDF_trie.insert_tf(word, (tf / target_doc_TF_Trie.word_count()) * idf_value) # tf / target_doc_TF_Trie.word_count() calculate average term-frequency
                
                target_doc_TFxIDF_trie.fill_max_trie(target_doc_max5_trie, 5)
                TF_max5_trie = Trie()
                for k, _ in target_doc_max5_trie.iteritems():
                    TF_max5_trie.insert_tf(k, target_doc_TF_Trie.search_tf(k)[1][-1])
                self.target_doc_TF_maxtrie_dict[target_doc] = TF_max5_trie

        [self.keywords_trie.insert_tf(k, tf) for doc, tf_trie in self.target_doc_TF_maxtrie_dict.iteritems() for k, tf in tf_trie.traverse_BFS()]
        self.keywords_count = self.keywords_trie.word_count()

    def doc_vector(doc):
        v_list = []
        tf_trie = self.target_doc_TF_maxtrie_dict.search_tf(doc)[1][-1]
        for k, tf in self.keywords_trie.traverse_BFS():
            find, match_list = tf_trie.search_tf(k)
            if find:
                v_list.append(match_list[-1])
            else:
                v_list.append(0)
        return v_list

    def print_maxtrie_dict(self):
        print_word=lambda x:sys.stdout.write(x+' ')
        for k, v in self.target_doc_TF_maxtrie_dict.iteritems():
            print 'doc:', k
            [print_word(word) for word, _ in v.traverse_BFS()]
            print '\n'

    @property
    def TFxIDF_maxtrie_dict(self):
        return copy.deepcopy(self.target_doc_TF_maxtrie_dict)
 

'''
def fill_dimension_trie(TFxIDF_maxtrie_dict, dimension_trie):
    [[dimension_trie.insert_0tf(word) for word, _ in v.traverse_BFS()] for _, v in TFxIDF_maxtrie_dict.iteritems()]
'''

'''
def TFxIDF_vector_expand(TFxIDF_maxtrie_dict, dimension_trie):
    TFxIDF_vector_dict = {}
    for k, v in TFxIDF_maxtrie_dict.iteritems():
        vector_trie = copy.deepcopy(dimension_trie)
        vector_trie.merge_tf(v)
        vector_list = []
        vector_trie.item_list(vector_list)
        TFxIDF_vector_dict[k] = [vector for vector, _ in vector_list]
    pass
'''


if __name__ == '__main__':
    tree = Trie()
    [tree.insert_tf(word, int(tf)) for word, tf in [(line.split()[0].decode('utf-8'), line.split()[1]) for line in open('./lexicon/open-gram-m7.u8.lexicon').readlines()]]
    mmseg = MMSEG(tree)

    target_doc_list = ['corpus/target_doc.txt', 'corpus/target_doc2.txt']
    tfidf_list = TFxIDF_list(mmseg, target_doc_list, 'corpus/386194-idf_sougoug_news_allsites.utf8')
    tfidf_list.print_maxtrie_dict()
    #TFxIDF_maxtrie_dict = tfidf_list.TFxIDF_maxtrie_dict
    #dimension_trie = Trie()
    #fill_dimension_trie(TFxIDF_maxtrie_dict, dimension_trie)
    #TFxIDF_vector_expand(TFxIDF_maxtrie_dict, dimension_trie)

    key_tf_vector1 = tfidf_list.doc_vector('corpus/target_doc.txt')
    key_tf_vector2 = tfidf_list.doc_vector('corpus/target_doc2.txt')

    numerator = sum([x + y for x, y in zip(key_tf_vector1, key_tf_vector2)])
    dinomimator1 = sum(map(lambda x: x**2, key_tf_vector1))
    dinomimator2 = sum(map(lambda x: x**2, key_tf_vector2))

    cosine = numerator / ( math.sqrt(dinomimator1) * math.sqrt(dinomimator2) )

    pass



