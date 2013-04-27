#!/usr/bin/env python
# -*- coding:utf-8 -*-
# * Calculate Term-Frequency Using Trie tree: Insert Term into Trie and increase the frequency number.

class Node(object):
    def __init__(self):
        self.word = None
        self.tf = 0
        self.children = {}

class Trie_TF(object):
    def __init__(self):
        self.root = Node()

    def insert(self, word):
        node = self.root
        for c in word:
            if c not in node.children:
                node.children[c] = Node()
            node = node.children[c]
        node.word = word
        node.tf += 1

    def search(self, word):
        node = self.root
        for c in word:
            if c not in node.children:
                return (False, None, 0)
            node = node.children[c]
        return (True, node.word, node.tf) if node.word else (False, None, 0)


if __name__ == '__main__':
    tree = Trie_TF()
    tree.insert('book')
    tree.insert('big')
    tree.insert('bigbang')
    tree.insert('hook')
    tree.insert('as')
    tree.insert('book')
    tree.insert('ass')
    tree.insert('book')
    tree.insert('bigbang')

    a = tree.search('book')
    b = tree.search('bigbang')
    c = tree.search('as')
    pass