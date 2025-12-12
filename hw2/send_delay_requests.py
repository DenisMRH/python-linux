import asyncio
import random
import aiohttp
import sys
from time import time


async def send_request(session, base_url, seconds):
    url = f"{base_url}/delay/{seconds}"
    async with session.get(url) as response:
        await response.text()
        return seconds


async def main(base_url, count):
    # генерируем случайные задержки от 1 до 60
    delays = [random.randint(1, 60) for _ in range(count)]
    
    start_time = time()
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        for delay in delays:
            task = asyncio.create_task(send_request(session, base_url, delay))
            tasks.append(task)
        
        results = await asyncio.gather(*tasks)
    
    end_time = time()
    total_time = end_time - start_time
    
    max_delay = max(delays)
    
    print(f"Отправлено запросов: {count}")
    print(f"Максимальная задержка: {max_delay} секунд")
    print(f"Общее время выполнения: {total_time:.2f} секунд")
    
    # наблюдаем что общее время примерно равно максимальной задержке
    # потому что все запросы идут параллельно
    print(f"\nНаблюдение: так как запросы идут асинхронно параллельно,")
    print(f"время выполнения примерно равно максимальной задержке, а не сумме всех задержек")


if __name__ == "__main__":
    # можно передать аргументы через командную строку: python script.py [base_url] [count]
    base_url = "http://127.0.0.1:8000"
    count = 100
    
    if len(sys.argv) >= 2:
        base_url = sys.argv[1]
    if len(sys.argv) >= 3:
        count = int(sys.argv[2])
    
    asyncio.run(main(base_url, count))

