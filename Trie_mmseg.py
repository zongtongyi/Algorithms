#!/usr/bin/env python
# -*- coding:utf-8 -*-
# * trie, prefix tree. Build with O(n*len), len is average of n strings' length. Search with O(len).
# * Algorithm refered : http://blog.csdn.net/v_july_v/article/details/6897097
# * Codes Refered : http://blog.csdn.net/psrincsdn/article/details/8158182

class Node(object):
    def __init__(self):
        self.word = None
        self.tf = 0
        self.children = {}

class Trie(object):
    def __init__(self):
        self.root = Node()

    '''def insert(self, word):
        node = self.root
        for c in word:
            if c not in node.children:
                node.children[c] = Node()
            node = node.children[c]
        node.word = word'''
    
    '''def search(self, word):
        partial_match = []
        node = self.root
        for c in word:
            if c not in node.children:
                return (False, partial_match)
            node = node.children[c]
            if node.word:
                partial_match.append(node.word)
        return (True, partial_match) if node.word else (False, partial_match)'''

    def insert_tf(self, word, tf):
        node = self.root
        for c in word:
            if c not in node.children:
                node.children[c] = Node()
            node = node.children[c]
        node.word = word
        node.tf = tf

    def search_tf(self,word):
        node = self.root
        for c in word:
            if c not in node.children:
                return (False, 0)
            node = node.children[c]
        return (True, node.tf) if node.word else (False, 0)
    
    def max_word_length(self):
        return self.height()

    def __node_height(self, node_list):
        if len(node_list) == 0:
            return 0
        else:
            children_node_list = []
            [children_node_list.extend( [v for v in node.children.itervalues()] ) for node in node_list]
            return 1 + self.__node_height(children_node_list)

    def height(self):
        return 0 if not self.root.children else self.__node_height([v for v in self.root.children.itervalues()])

if __name__ == '__main__':
    tree = Trie()
    tree.insert_tf('abcd', 44)
    tree.insert_tf('ab', 3542)
    tree.insert_tf('better',52907)
    height = tree.height()
    a = tree.search_tf('ab')
    a = tree.search_tf('be')
    b = tree.search_tf('best')
    f = tree.search_tf('better')
    pass