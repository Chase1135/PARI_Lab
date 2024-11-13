from fastapi import FastAPI, HTTPException, Request

app = FastAPI()

@app.post("/textual")
async def get_textual_data(request: Request):
    data = await request.json()
    print("Received textual data:", data)
    return {"message": "Textual data received", "data": data}

@app.post("/visual")
async def get_visual_data(request: Request):
    data = await request.json()
    print("Received visual data:", data)
    return {"message": "Visual data received", "data": data}

@app.post("/physical")
async def get_physical_data(request: Request):
    data = await request.json()
    print("Received physical data:", data)
    return {"message": "Physical data received", "data": data}
