# Use a base image with Python
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy requirements.txt into the working directory
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Download and install Ollama for Linux
RUN if ! command -v ollama &> /dev/null; then curl -fsSL https://ollama.com/install.sh | sh; fi

# Copy the rest of the application code
COPY . .

# Copy the start_servers.sh script to the container
COPY start_servers.sh /start_servers.sh

EXPOSE 5000

RUN chmod +x /start_servers.sh

# Command to run the app and Ollama server
CMD ["/start_servers.sh"]