#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import timeit
import random
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import heapq

amount_of_dots = 100  # Количество точек
aod = (amount_of_dots + 1) * 10
median_time = {}
graph_stuff = [i for i in range(10, aod, 10)]
xlabel = "Количество элементов в массиве"
ylabel = "Среднее время выполнения (секунды)"

def heapify(lis, n, i):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and lis[i] < lis[left]:
        largest = left

    if right < n and lis[largest] < lis[right]:
        largest = right

    if largest != i:
        lis[i], lis[largest] = lis[largest], lis[i]
        heapify(lis, n, largest)

def heap_sort(lis):
    n = len(lis)

    for i in range(n // 2 - 1, -1, -1):
        heapify(lis, n, i)

    for i in range(n - 1, 0, -1):
        lis[i], lis[0] = lis[0], lis[i]
        heapify(lis, i, 0)

    return lis

def heap_sort_fast(lis):
    heapq.heapify(lis)
    sorted_result = [heapq.heappop(lis) for _ in range(len(lis))]
    return sorted_result

def fill_list(num_of_elements):
    a = [random.randint(0, 100000) for _ in range(num_of_elements)]
    return a

def measure_sort_time(sort_func, unsorted_list):
    def func_to_measure():
        # Создаем копию, чтобы не влиять на оригинальный список
        copy_list = list(unsorted_list)
        sort_func(copy_list)
    return timeit.timeit(func_to_measure, number=100) / 100

def n_log_n_model(x, a, b):
    return a * x * np.log(x) + b

def lsm(name, time, graph_num):
    plt.figure(graph_num).set_figwidth(8)
    plt.title(
        f"Зависимость времени сортировки от размера массива\n({name})")
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()
    plt.grid(False)

    x_data = np.array(graph_stuff)
    y_data = np.array(list(time.values()))

    params, _ = curve_fit(n_log_n_model, x_data, y_data)

    a_fit, b_fit = params
    print(f"Коэффициенты уравнения ({name}): a = {a_fit}, b = {b_fit}")

    x_fit = np.linspace(min(x_data), max(x_data), 100)
    y_fit = n_log_n_model(x_fit, *params)

    plt.plot(x_fit, y_fit, "r-", label="n log n Fit")

    plt.scatter(graph_stuff, time.values(), s=5, c="blue")
    plt.tight_layout()

def results(name, func, graph_index):
    for i in range(10, aod, 10):
        a = fill_list(i)
        median_time[i] = timeit.timeit(lambda: func(a),
                                       number=100) / 100

    lsm(name, median_time, graph_index)

if __name__ == "__main__":
    unsorted_list = fill_list(200)

    sorted_slow = measure_sort_time(heap_sort, unsorted_list)
    print("Отсортирован обычным heapsort за:", sorted_slow, "сек")
    sorted_fast = measure_sort_time(heap_sort_fast, unsorted_list)
    print("Отсортирован heapsort с heapq за:", sorted_fast, "сек")
    print("Версия с heapq быстрее на", sorted_slow - sorted_fast, "сек")
    results("Неоптимизированный heapsort", heap_sort, 0)
    results("Oптимизированный heapsort", heap_sort_fast, 1)

    plt.show()