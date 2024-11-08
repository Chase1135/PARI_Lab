from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/textual")
async def get_textual_data():
    return {"message": "This is the textual data endpoint"}

@app.get("/visual")
async def get_visual_data():
    return {"message": "This is the visual data endpoint"}

@app.get("/physical")
async def get_physical_data():
    return {"message": "This is the physical data endpoint"}
