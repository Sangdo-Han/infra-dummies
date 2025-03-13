from fastapi import FastAPI

app = FastAPI()

@app.get("/interact")
async def get_interaction():
    return {"message": "Kub Inside! - 2"}

if "__main__" == __name__:
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

