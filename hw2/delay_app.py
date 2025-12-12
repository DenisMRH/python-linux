import asyncio
from fastapi import FastAPI

app = FastAPI()


@app.get("/delay/{seconds}")
async def delay(seconds: int):
    await asyncio.sleep(seconds)
    return {"message": f"Done waiting for {seconds} seconds"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

