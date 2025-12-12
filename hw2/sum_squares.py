from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import os
import sys
import io
from time import perf_counter

# Устанавливаем UTF-8 для вывода в консоль Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

LIMIT = 1_000_000


def chunk_sum(start, end):
    # считаем сумму квадратов от start до end
    result = 0
    for i in range(start, end):
        result += i * i
    return result


def chunk_sum_range(rng):
    # обертка чтобы передать в executor
    return chunk_sum(rng[0], rng[1])


def split_ranges(total, parts):
    # делим на части для параллельной обработки
    chunk_size = total // parts
    ranges = []
    start = 1
    for i in range(parts):
        end = start + chunk_size
        if i == parts - 1:  # последний кусок берет все что осталось
            end = total + 1
        ranges.append((start, end))
        start = end
    return ranges


def sum_sync():
    return chunk_sum(1, LIMIT + 1)


def sum_threaded(workers):
    ranges = split_ranges(LIMIT, workers)
    with ThreadPoolExecutor(max_workers=workers) as executor:
        results = list(executor.map(chunk_sum_range, ranges))
    return sum(results)


def sum_multiprocessing(workers):
    ranges = split_ranges(LIMIT, workers)
    with ProcessPoolExecutor(max_workers=workers) as executor:
        results = list(executor.map(chunk_sum_range, ranges))
    return sum(results)


def measure(name, func):
    start = perf_counter()
    value = func()
    duration = perf_counter() - start
    return (name, duration, value)


def main():
    workers = os.cpu_count() or 4
    
    result1 = measure("sync", sum_sync)
    result2 = measure("threads", lambda: sum_threaded(workers))
    result3 = measure("processes", lambda: sum_multiprocessing(workers))
    
    runs = [result1, result2, result3]
    
    # проверяем что результаты совпадают
    first_value = runs[0][2]
    for r in runs:
        if r[2] != first_value:
            print("ОШИБКА: разные суммы!")
            break
    
    for r in runs:
        print(f"{r[0]:10s} время={r[1]:.4f}с сумма={r[2]}")
    
    print(f"\nКоличество потоков/процессов: {workers}")


if __name__ == "__main__":
    main()

