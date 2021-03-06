#!/usr/bin/env python
# -*- coding:utf-8 -*-
# * trie, prefix tree. Build with O(n*len), len is average of n strings' length. Search with O(len).
# * Algorithm refered : http://blog.csdn.net/v_july_v/article/details/6897097
# * Codes Refered : http://blog.csdn.net/psrincsdn/article/details/8158182
# * TODO: Node definition could be just 'val' and 'children', then define 'val' outside this algorithm, 
# *       also Trie algorithm should just provide basic operations and expand operations by users

class Node(object):
    def __init__(self):
        self.word = None
        self.tf = 0
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

    def insert_tf(self, word, tf):
        node = self.root
        for c in word:
            if c not in node.children:
                node.children[c] = Node()
            node = node.children[c]
        node.word = word
        node.tf = tf

    def search(self, word):
        partial_match = []
        node = self.root
        for c in word:
            if c not in node.children:
                return (False, partial_match)
            node = node.children[c]
            if node.word:
                partial_match.append(node.word)
        return (True, partial_match) if node.word else (False, partial_match)

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
    tree.insert('abcd')
    tree.insert('ab')
    tree.insert('better')
    height = tree.height()
    tree.insert('best')
    a = tree.search('ab')
    a = tree.search('be')
    b = tree.search('best')
    f = tree.search('better')
    pass