# https://fastapi.tiangolo.com/tutorial/first-steps/
# How to run the code: uvicorn app.main:app --reload

from fastapi import FastAPI

# Import your routers here
# example: from app.routers import module1

app = FastAPI(
    title="Your App Title",
    description="Add description on what the app is for.",
    version="0.1.0",
    contact={
        "name": "Your Name",
        "url": "http://you-own-url.com"
    }
)

# use the imported router in your project here:
# app.include_router(module1.router)


@app.get("/")
async def root_endpoint():
    return {
        "message": "API is running successfully!"
    }
