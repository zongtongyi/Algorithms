#!/usr/bin/env python
# -*- coding:utf-8 -*-
# * Suffix Array
# * Algorithm refered : 'Programming Pearls(Second Edition)' Chapter 15
# * demo without effective build process. Build: O(n) + O(nlogn)


def build_suffix_array(suffix_array, text_string):
    for i in range(len(text_string)):
        suffix_array.append(text_string[i:])

    suffix_array.sort()


def comlen(str_i, str_i_next):
    max_len = 0
    for i in range(1, len(str_i)+1):
        max_len = i if str_i[:i]==str_i_next[:i] else max_len

    return max_len


if __name__ == '__main__':
    suffix_array = []
    text_string = "Ask not what your country can do for you, but what you can do for your country"

    build_suffix_array(suffix_array, text_string)
 
    # Use Suffix Array to solve LRS   
    # The Longest Repeated Substring
    max_len = 0
    max_idx = 0
    for i in range(len(text_string)-1):
        com_len = comlen(suffix_array[i], suffix_array[i+1])
        [max_len, max_idx] = [com_len, i] if com_len > max_len else [max_len, max_idx]

    max_str = suffix_array[max_idx][:max_len]
    pass