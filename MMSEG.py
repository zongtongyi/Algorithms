#!/usr/bin/env python
# -*- coding:utf-8 -*-
# MMSEG: A Word Identification System for Mandarin Chinese Text Based on Two Variants of the Maximum Matching Algorithm
# Theory refered: http://technology.chtsai.org/mmseg/
# code refered: 
#

import math
#from Trie import Trie_mmseg as Trie_mmseg
from Trie.Trie_mmseg import *

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
        single_tf_list = [tf_list[i] for i in range(3) if len(tri_word_list[i])==1 and tf_list[i]!=0]
        self.rule4 = 0 if not single_tf_list else reduce(lambda x, y: math.log(x) + math.log(y), single_tf_list)

    def __lt__(self, obj):
        if [self.rule1, self.rule2, -(self.rule3), self.rule4] < [obj.rule1, obj.rule2, -(obj.rule3), obj.rule4]:
            return True
        else:
            return False

class MMSEG(object):
    def __init__(self, lexicon):
        self.lexicon = lexicon
        self.max_word_len = lexicon.max_word_length()
        self.corpus_seg_list = []

    def print_seg(self):
        str_print = reduce(lambda x,y: x + '/' + y, self.corpus_seg_list)
        print str_print

    def word_seg_simple(self, corpus):
        i, j, corpus_len, self.corpus_seg_list = 0, 0, len(corpus), []
        while i < corpus_len:
            s = corpus[i:min(i + self.max_word_len, corpus_len)]
            find, match = self.lexicon.search_tf(s) # prefix match
            j = (i + 1) if len(match)==0 else ( i + len(match[-1][0]) )
            self.corpus_seg_list.append(corpus[i:j])
            i = j
        return self.corpus_seg_list

    def word_seg_complex(self, corpus):
        i, corpus_len, self.corpus_seg_list = 0, len(corpus), []
        while i < corpus_len:
            s = corpus[i:min(i + self.max_word_len, corpus_len)]
            tri_word_list, tf_list, chunk_list = [], [], []
            find, match = self.lexicon.search_tf(s) # prefix match
            match = match if len(match)!=0 else [(s[0], '1')] # unknown word
            for word, tf in match:
                tri_word_list.append(word)
                tf_list.append(0 if len(word)!=0 else tf)
                i2 = i + len(word)
                s2 = corpus[i2:min(i2+self.max_word_len, corpus_len)]
                find2, match2 = self.lexicon.search_tf(s2)
                match2 = match2 if len(match2)!=0 else ([(s2[0], '1')] if len(s2)!=0 else [(' ', '1')]) # unknown word
                for word2, tf2 in match2:
                    tri_word_list.append(word2)
                    tf_list.append(0 if len(word2)!=0 else tf2)
                    i3 = i2 + len(word2)
                    s3 = corpus[i3:min(i3+self.max_word_len, corpus_len)]
                    find3, match3 = self.lexicon.search_tf(s3)
                    match3 = match3 if len(match3)!=0 else ([(s3[0], '1')] if len(s3)!=0 else [(' ', '1')]) # unknown word
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
            self.corpus_seg_list.append(corpus[i:j])
            i = j

        return self.corpus_seg_list


if __name__ == '__main__':
    words_list = [(line.split()[0].decode('utf-8'), line.split()[1]) for line in open('./lexicon/open-gram-m7.u8.lexicon').readlines()]
    #tree = Trie_mmseg.Trie()
    tree = Trie()
    [tree.insert_tf(word, tf) for word, tf in words_list]

    mmseg = MMSEG(tree)
    corpus = "吃葡萄不吐葡萄皮，不吃葡萄到吐葡萄皮"
    mmseg.word_seg_simple(corpus.decode('utf-8'))

    corpus = "研究生命起源"
    corpus = "据英国《每日邮报》１２月２６日报道，视频分享网站ＹｏｕＴｕｂｅ　上近日出现一段点击量约百万的搞笑影片。在短片里，一只６个月大的猫咪在小心翼翼地下楼梯，不料，一旁冷眼观看的同伴突然伸出“魔爪”，一把将其推了下去，所幸小猫没有受伤。　（来源：中国日报网）"
    mmseg.word_seg_complex(corpus.decode('utf-8'))
    mmseg.print_seg()

    pass
