import asyncio
import random
from fastapi import FastAPI
from async_timer import AsyncTimer

app = FastAPI()


@app.get("/random-sleep")
async def random_sleep():
    sleep_time = random.uniform(0.5, 3.0)
    async with AsyncTimer("random sleep"):
        await asyncio.sleep(sleep_time)
    return {"message": f"Задержка {sleep_time:.2f} секунд"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)

