#!/usr/bin/env python
# -*- coding:utf-8 -*-
# * trie, prefix tree. Build with O(n*len), len is average of n strings' length. Search with O(len).
# * Algorithm refered : http://blog.csdn.net/v_july_v/article/details/6897097
# * Codes Refered : http://blog.csdn.net/psrincsdn/article/details/8158182

class Node(object):
    def __init__(self):
        self.word = None
        self.children = {}

class Trie(object):
    def __init__(self):
        self.root = Node()

    def insert(self, word):
        node = self.root
        for c in word:
            if c not in node.children:
                node.children[c] = Node()
            node = node.children[c]
        node.word = word

    def search(self, word):
        node = self.root
        for c in word:
            if c not in node.children:
                return (False, None)
            node = node.children[c]
        return (True, node.word) if node.word else (False, None)

if __name__ == '__main__':
    tree = Trie()
    tree.insert('abcd')
    tree.insert('ab')
    tree.insert('better')
    tree.insert('best')
    a = tree.search('ab')
    a = tree.search('be')
    b = tree.search('best')
    f = tree.search('better')
    pass