#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import heapq
import random


def print_ascending_sums(A, B):

    # Сортируем оба массива
    A.sort()
    B.sort()

    # min-heap хранит выражения вида (сумма, индекс в A, индекс в B)
    heap = [(A[i] + B[0], i, 0) for i in range(len(A))]
    heapq.heapify(heap)

    # Вывод суммы в возрастающем порядке
    for _ in range(len(A)**2):
        sum, i, j = heapq.heappop(heap)
        print(sum, end=' ')
        if j + 1 < len(B):
            heapq.heappush(heap, (A[i] + B[j+1], i, j+1))


def fill_list(num_of_elements):
    a = [random.randint(1, 10) for _ in range(num_of_elements)]
    return a


if __name__ == "__main__":
    n = 5
    A = fill_list(n)
    B = fill_list(n)
    print(sorted(A), "\n", sorted(B))
    print_ascending_sums(A, B)