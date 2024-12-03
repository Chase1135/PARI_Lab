from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import json, asyncio
from response_generator import generate_response

app = FastAPI()

#TEXTUAL ENDPOINT
@app.websocket("/ws/textual")
async def websocket_textual_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            try:
                #grab data, convert to json, print to confirm
                data = await asyncio.wait_for(websocket.receive_text(), timeout=30.0)
                print(f"Received raw data: {data}", flush=True)
                json_data = json.loads(data)
                print(f"Received textual data: {json_data}", flush=True)

                #GENERATE A RESPONSE
                async for token in generate_response(json_data["message"]):
                    print(f"Streaming token: {token}", flush=True)
                    await websocket.send_text(token["message"]["content"])

                #return OK to client
                #response = {"status": "received", "type": "textual", "content": json_data}
                await websocket.send_text("[END OF RESPONSE]")
            except asyncio.TimeoutError: 
                await websocket.send_text("Ping") 
                print("Ping sent",flush=True)
                
    except Exception as e:
        if type(e) is not WebSocketDisconnect:
            print(f"Error in textual endpoint: {e}", flush=True)

#VISUAL ENDPOINT
@app.websocket("/ws/visual")
async def websocket_visual_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            #grab data, convert to json, print to confirm
            data = await websocket.receive_text()
            print(f"Received raw data: {data}", flush=True)
            json_data = json.loads(data)
            print(f"Received visual data: {json_data}")

            #return OK to client
            response = {"status": "received", "type": "visual", "content": json_data}
            await websocket.send_text(json.dumps(response))
    except Exception as e:
        print(f"Error in visual endpoint: {e}")
    finally:
        try:
            await websocket.close()
        except Exception as e:
            print(f"Error closing WebSocket: {e}", flush=True)

#PHYSICAL ENDPOINT
@app.websocket("/ws/physical")
async def websocket_dynamic_endpoint(websocket: WebSocket, data_type: str):
    await websocket.accept()
    try:
        while True:
            #grab data, convert to json, print to confirm
            data = await websocket.receive_text()
            print(f"Received raw data: {data}", flush=True)
            json_data = json.loads(data)
            print(f"Received physical data: {json_data}")

            #return OK to client
            response = {"status": "received", "type": "physical", "content": json_data}
            await websocket.send_text(json.dumps(response))
    except Exception as e:
        print(f"Error in physical endpoint: {e}")
    finally:
        try:
            await websocket.close()
        except Exception as e:
            print(f"Error closing WebSocket: {e}", flush=True)
