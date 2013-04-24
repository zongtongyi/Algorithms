#!/usr/bin/env python
# -*- coding:utf-8 -*-
# * trie, prefix tree
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
                return False, None
            node = node.children[c]
        return True, node.word

    def __collect_words(self, node):
        results = []
        if node.word:
            results.append(node.word)
        for k,v in node.children.iteritems():
            results.extend(self.__collect_words(v))
        return results

    def auto_complete(self, prefix_word):
        node = self.root
        for c in prefix_word:
            if c not in node.children:
                return []
            node = node.children[c]

        return self.__collect_words(node)

if __name__ == '__main__':
    tree = Trie()
    tree.insert('abcd')
    tree.insert('ab')
    tree.insert('better')
    tree.insert('best')
    c = tree.auto_complete('ab')
    d = tree.auto_complete('be')
    pass