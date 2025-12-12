from datetime import datetime
import httpx
from bs4 import BeautifulSoup
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from urllib.parse import urljoin
from typing import Optional

app = FastAPI()


class Joke(BaseModel):
    text: str
    autor_profile: Optional[str] = None
    rating: int


def parse_date(date_str):
    # парсим дату формата 01-January-2025
    parts = date_str.split("-")
    if len(parts) != 3:
        raise HTTPException(status_code=400, detail="Неверный формат даты")
    
    day = int(parts[0])
    month_name = parts[1]
    year = int(parts[2])
    
    # находим номер месяца
    months = {
        "january": 1, "february": 2, "march": 3, "april": 4,
        "may": 5, "june": 6, "july": 7, "august": 8,
        "september": 9, "october": 10, "november": 11, "december": 12
    }
    
    month = months.get(month_name.lower())
    if month is None:
        raise HTTPException(status_code=400, detail="Неверное название месяца")
    
    return datetime(year, month, day)


async def get_html(url):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=20.0)
            response.raise_for_status()
            return response.text
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Ошибка при запросе: {e}")


def extract_jokes(html):
    soup = BeautifulSoup(html, "html.parser")
    jokes = []
    
    # ищем блоки с анекдотами
    topic_boxes = soup.find_all("div", class_="topicbox")
    
    for box in topic_boxes:
        text_div = box.find("div", class_="text")
        if not text_div:
            continue
        
        text = text_div.get_text(strip=True)
        
        # ищем автора
        author_link = None
        author_tags = box.find_all("a")
        for tag in author_tags:
            if "href" in tag.attrs:
                href = tag["href"]
                if "/users/" in href:
                    author_link = urljoin("https://www.anekdot.ru", href)
                    break
        
        # ищем рейтинг
        rating = 0
        rating_spans = box.find_all("span")
        for span in rating_spans:
            if "rating" in span.get("class", []):
                rating_text = span.get_text(strip=True)
                # пытаемся извлечь число
                try:
                    # убираем все кроме цифр и минуса
                    digits = ""
                    for char in rating_text:
                        if char.isdigit() or char == "-":
                            digits += char
                    if digits:
                        rating = int(digits)
                    break
                except:
                    rating = 0
                    break
        
        jokes.append(Joke(
            text=text,
            autor_profile=author_link,
            rating=rating
        ))
    
    return jokes


@app.get("/best")
async def best(day: str = Query(...)):
    date_obj = parse_date(day)
    date_str = date_obj.strftime("%Y-%m-%d")
    
    url = f"https://www.anekdot.ru/release/anekdot/day/{date_str}/"
    html = await get_html(url)
    jokes = extract_jokes(html)
    
    # сортируем по рейтингу
    jokes.sort(key=lambda x: x.rating, reverse=True)
    
    return jokes


@app.get("/random")
async def random_jokes():
    url = "https://www.anekdot.ru/random/anekdot/"
    html = await get_html(url)
    jokes = extract_jokes(html)
    return jokes


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)

