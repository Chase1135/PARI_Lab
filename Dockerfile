# Use a base image with Python
FROM python:3.9

# Set the working directory
WORKDIR /app

# Netcat
RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt into the working directory
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Download and install Ollama for Linux
RUN if ! command -v ollama &> /dev/null; then curl -fsSL https://ollama.com/install.sh | sh; fi

# Copy the .env file into the container
COPY .env .env

# Copy the rest of the application code
COPY . .

# Copy the start_servers.sh script to the container
COPY start_servers.sh /start_servers.sh
RUN chmod +x /start_servers.sh

EXPOSE 5000

# Command to run the app and Ollama server
CMD ["/start_servers.sh"]