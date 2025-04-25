import os
import wave
import asyncio
import httpx 
from buffers import INBOUND_BUFFERS

from config import FRAMERATE, SAMPWIDTH, NCHANNELS

API_KEY_ID = "s1XyepwyxRdijzuf"
API_KEY_SECRET = "3ht6liNE015yjdiZ"
LANG = "en"
FILE_PATH = "STT/user_speech.wav"
RESULT_TYPE = 4

headers = {"keyId": API_KEY_ID, "keySecret": API_KEY_SECRET}


def write_wav_from_frames(frames: bytes, path: str, sample_rate=FRAMERATE, channels=NCHANNELS, sample_width=SAMPWIDTH):
    with wave.open(path, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(sample_rate)
        wf.writeframes(frames)

    print(f"Audio frames transcribed to .wav at: {path}", flush=True)


async def create():
    create_url = "https://api.speechflow.io/asr/file/v1/create"
    create_data = {"lang": LANG}
    files = {}

    abs_path = os.path.abspath(FILE_PATH)

    if not os.path.exists(abs_path):
        print(f"[ERROR] File not found: {abs_path}", flush=True)
        return ""

    print(f"[INFO] Submitting local file: {abs_path}", flush=True)
    create_url += f"?lang={LANG}"

    async with httpx.AsyncClient() as client:
        with open(abs_path, "rb") as audio_file:
            files = {"file": (os.path.basename(abs_path), audio_file, "audio/wav")}
            response = await client.post(create_url, headers=headers, files=files)

    if response.status_code == 200:
        result = response.json()
        if result.get("code") == 10000:
            task_id = result["taskId"]
            print(f"[INFO] Task created. ID: {task_id}")
            return task_id
        else:
            print("[ERROR] Create error:", result.get("msg"), flush=True)
    else:
        print(f"[ERROR] Create request failed: HTTP {response.status_code}")

    return ""


async def query(task_id):
    query_url = (
        f"https://api.speechflow.io/asr/file/v1/query?taskId={task_id}&resultType={RESULT_TYPE}"
    )

    print("[INFO] Querying transcription result...", flush=True)

    async with httpx.AsyncClient() as client:
        while True:
            try:
                response = await client.get(query_url, headers=headers)
            except Exception as e:
                print(f"[ERROR] Exception during query: {e}", flush=True)
                return ""

            if response.status_code == 200:
                result = response.json()
                code = result.get("code")

                if code == 11000:
                    print("[SUCCESS] Transcription complete:", flush=True)
                    print(result, flush=True)
                    return result["result"]
                elif code == 11001:
                    print("[INFO] Transcription in progress... waiting.", flush=True)
                    await asyncio.sleep(3)
                    continue
                else:
                    print("[ERROR] Transcription failed:", result.get("msg"), flush=True)
                    break
            else:
                print(f"[ERROR] Query failed: HTTP {response.status_code}", flush=True)
                break

    return ""


async def convert_speech_to_text():
    audio_bytes = b"".join(INBOUND_BUFFERS["audio"])
    write_wav_from_frames(audio_bytes, os.path.abspath(FILE_PATH))
    INBOUND_BUFFERS["audio"].clear()

    task_id = await create()
    if task_id:
        converted_text = await query(task_id)
        return converted_text

    return ""


if __name__ == "__main__":
    asyncio.run(convert_speech_to_text())
