import asyncio
import aiohttp
import sys

try:
    from tqdm import tqdm
    HAS_TQDM = True
except ImportError:
    HAS_TQDM = False


async def check_url(session, semaphore, url, timeout=10):
    async with semaphore:
        try:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=timeout)) as response:
                status = response.status
                if status >= 200 and status < 300:
                    return url, "доступен"
                else:
                    return url, f"недоступен ({status})"
        except asyncio.TimeoutError:
            return url, "ошибка: timeout"
        except Exception as e:
            return url, f"ошибка: {str(e)}"


async def scan_urls(url_list, max_concurrent=10):
    semaphore = asyncio.Semaphore(max_concurrent)
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in url_list:
            task = asyncio.create_task(check_url(session, semaphore, url))
            tasks.append(task)
        
        if HAS_TQDM:
            # если есть tqdm, показываем прогресс
            results = []
            for task in tqdm(asyncio.as_completed(tasks), total=len(tasks), desc="Проверка"):
                result = await task
                results.append(result)
            return results
        else:
            # иначе просто ждем все задачи
            return await asyncio.gather(*tasks)


def read_urls(filename):
    urls = []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                url = line.strip()
                if url:
                    urls.append(url)
    except FileNotFoundError:
        print(f"Файл {filename} не найден!")
        sys.exit(1)
    return urls


def write_results(filename, results):
    with open(filename, "w", encoding="utf-8") as f:
        for url, status in results:
            f.write(f"{url} - {status}\n")


def main():
    # аргументы командной строки
    input_file = "urls.txt"
    output_file = "results.txt"
    max_concurrent = 10
    
    # парсим аргументы вручную
    i = 1
    while i < len(sys.argv):
        if sys.argv[i] == "--input" and i + 1 < len(sys.argv):
            input_file = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--output" and i + 1 < len(sys.argv):
            output_file = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--limit" and i + 1 < len(sys.argv):
            max_concurrent = int(sys.argv[i + 1])
            i += 2
        else:
            i += 1
    
    urls = read_urls(input_file)
    if not urls:
        print("Список URL пуст!")
        return
    
    print(f"Найдено {len(urls)} URL для проверки")
    print(f"Максимум одновременных запросов: {max_concurrent}")
    
    results = asyncio.run(scan_urls(urls, max_concurrent))
    write_results(output_file, results)
    
    print(f"\nПроверка завершена. Результаты записаны в {output_file}")


if __name__ == "__main__":
    main()

