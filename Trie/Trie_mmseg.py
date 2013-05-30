#!/usr/bin/env python
# -*- coding:utf-8 -*-
# * trie, prefix tree. Build with O(n*len), len is average of n strings' length. Search with O(len).
# * Algorithm refered : http://blog.csdn.net/v_july_v/article/details/6897097
# * Codes Refered : http://blog.csdn.net/psrincsdn/article/details/8158182

class MergeTypeError(Exception): pass

class Node(object):
    def __init__(self):
        self.word = None
        self.tf = 0
        self.children = {}

class Trie(object):
    def __init__(self):
        self.root = Node()

    def insert(self, word):    # Accumlate TF while insert word
        node = self.root
        for c in word:
            if c not in node.children:
                node.children[c] = Node()
            node = node.children[c]
        node.word, node.tf = word, (node.tf + 1)
    
    def insert_0tf(self, word):    # ignore TF(keep as 1) while insert word
        node = self.root
        for c in word:
            if c not in node.children:
                node.children[c] = Node()
            node = node.children[c]
        node.word = word

    def insert_tf(self, word, tf):    # SET TF while insert word
        node = self.root
        for c in word:
            if c not in node.children:
                node.children[c] = Node()
            node = node.children[c]
        node.word, node.tf = word, tf
    
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

    def search_tf(self, word):
        partial_match = []
        node = self.root
        for c in word:
            if c not in node.children:
                return (False, partial_match)
            node = node.children[c]
            if node.word:
                partial_match.append((node.word, node.tf))
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

    def traverse_BFS(self): # Breadth-First Search
        import Queue
        node_queue = Queue.Queue()
        node_queue.put(self.root)
        while not node_queue.empty():
            node = node_queue.get()
            if node.word:
                yield (node.word, node.tf)
            if len(node.children) != 0:
                [node_queue.put(node) for node in node.children.itervalues()]

    def merge(self, Node_trie): # this incoming trie's node must be Node type
        if not isinstance(Node_trie, Trie):
            raise MergeTypeError('Incoming trie is not type(Trie)')
        [self.insert(word) for word in Nodetrie.traverse_BFS()]


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
    for word, tf in tree.traverse_BFS():
        print word, tf
    pass