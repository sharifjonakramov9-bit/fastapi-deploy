from fastapi import FastAPI

app = FastAPI(title="FastAPI deploy")


@app.get("/")
async def home_view():
    return {"message": "hello world"}


@app.get("/about")
async def about_view():
    return {"message": "about page"}
