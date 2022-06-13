# https://fastapi.tiangolo.com/tutorial/first-steps/
# How to run the code: uvicorn app.main:app --reload

from fastapi import FastAPI

from app.routers import auth, user, topic
# Import your routers here
# example: from app.routers import module1

app = FastAPI(
    title="Quiz API",
    description="API for the Quiz APP",
    version="0.1.0",
    contact={
        "name": "Kamal",
        "url": "https://github.com/KamalDGRT/quiz-app"
    }
)

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(topic.router)

# use the imported router in your project here:
# app.include_router(module1.router)


@app.get("/")
async def root_endpoint():
    return {
        "message": "API is running successfully!"
    }
