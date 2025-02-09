from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import json, asyncio, sys, os
from response_generator import generate_response

sys.path.append(os.path.abspath('Text-to-Speech'))
from PlayHD import generate_speech, wav_to_bytes

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
                if data.lower() == "pong": # Heartbeat technique, pong just keeps the socket alive
                    continue
 
                response_text = await generate_response(data) # Generate the response from LLM
                print(f"Generated response: {response_text}", flush=True)

                # Convert generated response to .wav and then to raw PCM data
                await generate_speech(response_text)
                params, frames = wav_to_bytes("Text-to-Speech/playhtTest.wav")

                if params and frames:
                    # Convert headers to JSON format
                    metadata = {
                        "nchannels": params.nchannels,
                        "sampwidth": params.sampwidth,
                        "framerate": params.framerate,
                        "nframes": params.nframes
                    }
                    await websocket.send_text(json.dumps(metadata)) # Send headers
                    print("Sent metadata", flush=True)

                    chunk_size = 4096 # Must chunk audio frames to reduce size of message
                    for i in range(0, len(frames), chunk_size):
                        await websocket.send_bytes(frames[i:i+chunk_size])

                    await websocket.send_text("END") # Indicate end of transmission
                    print("Sent audio frames",flush=True)

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
