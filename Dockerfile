# Use a base image with Python
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy requirements.txt into the working directory
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

EXPOSE 5000

# Command to run the app
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "5000"]
