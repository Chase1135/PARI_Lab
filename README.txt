HOW TO RUN WITHIN DOCKER DESKTOP:
1. open docker terminal
2. pull docker image ('docker pull chasea1135/pari_lab_server:latest')
3. run container ('docker run -p 5000:5000 chasea1135/pari_lab_server:latest') OR click run on downloaded image
4. if run from images tab, enter port # (5000)

RUNNING LOCALLY:
1. clone repository, install necessary dependencies (pydantic, fastapi, uvicorn, websockets, ollama)
2. open docker terminal, navigate to project folder
3. type 'docker-compose up --build' in terminal

TO TEST:
1. run test_connection.py (type exit to close connection)