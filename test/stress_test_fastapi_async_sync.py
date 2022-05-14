from fastapi import APIRouter
import time
import asyncio

app = APIRouter()


@app.get("/a")
async def a():
    time.sleep(1)
    return {"message": "异步模式，但是同步执行sleep函数，执行过程是串行的"}


@app.get("/b")
async def b():
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, time.sleep, 1)
    return {"message": "线程池中运行sleep函数"}


@app.get("/c")
async def c():
    await asyncio.sleep(1)
    return {"message": "异步模式，且异步执行sleep函数"}


@app.get("/d")
def d():
    time.sleep(1)
    return {"message": "同步模式，但是FastAPI会放在线程池中运行，所以很快"}
