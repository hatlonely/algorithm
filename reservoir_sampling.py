#!/usr/bin/env python3
# 蓄水池算法
# 更多的讨论: http://hatlonely.github.io/2018/01/26/蓄水池算法/

import unittest
import random


def reservior_sampling(sequence, k):
    n = len(sequence)
    if k > n:
        return sequence

    sample = list()
    for i in range(k):
        sample.append(sequence[i])

    for i in range(k, n):
        j = random.randint(0, i)
        if j >= k:
            continue
        sample[j] = sequence[i]

    return sample


def weighted_reservior_sampling_achao(sequence, k):
    n = len(sequence)
    if k > n:
        return sequence

    wsum = 0
    sample = list()
    for i in range(k):
        sample.append(sequence[i])
        wsum += sequence[i]['weight'] / k

    for i in range(k, n):
        wsum += sequence[i]['weight'] / k
        p = sequence[i]['weight'] / wsum
        j = random.random()
        if j <= p:
            sample[random.randint(0, k-1)] = sequence[i]

    return sample


class TestReserviorSampling(unittest.TestCase):
    def test_reservior_sampling(self):
        sequence = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        k = 4
        times = dict()
        for item in sequence:
            times[item] = 0
        for i in range(100000):
            sample = reservior_sampling(sequence, k)
            for item in sample:
                times[item] += 1
        print(times)

    def test_weighted_reservior_sampling_achao(self):
        sequence = [{
            'value': 0,
            'weight': 10,
        }, {
            'value': 1,
            'weight': 20,
        }, {
            'value': 2,
            'weight': 30,
        }, {
            'value': 3,
            'weight': 10,
        }, {
            'value': 4,
            'weight': 20,
        }, {
            'value': 5,
            'weight': 30,
        }, {
            'value': 6,
            'weight': 10,
        }, {
            'value': 7,
            'weight': 20,
        }, {
            'value': 8,
            'weight': 30,
        }, {
            'value': 9,
            'weight': 10,
        }]
        k = 4
        times = dict()
        for item in sequence:
            times[item['value']] = 0
        for i in range(100000):
            sample = weighted_reservior_sampling_achao(sequence, k)
            for item in sample:
                times[item['value']] += 1
        print(times)


if __name__ == '__main__':
    unittest.main()
