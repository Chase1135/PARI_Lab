HOW TO RUN WITHIN DOCKER DESKTOP:
1. open docker terminal
2. pull docker image ('docker pull chasea1135/pari-lab-server:latest')
3. run container ('docker run -p 5000:5000 chasea1135/pari-lab-server:latest')
4. enter host machine's IP as environment variable

1. clone repository, install necessary dependencies (pydadntic, fastapi, uvicorn)
2. open docker terminal, navigate to project folder
3. type 'docker-compose up' in terminal

TO TEST:
Invoke-RestMethod -Uri "http://'insertiphere':5000/textual" -Method Post -Headers @{ "Content-Type" = "application/json" } -Body '{"sample": "textual data"}'
