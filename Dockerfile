# Use a lightweight and stable Python image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy all files from the host to the container
COPY . .

# Install system dependencies (FFmpeg and other required tools)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python dependencies from the requirements file
RUN pip install --no-cache-dir -r requirements.txt

# Expose port (if your bot needs one for webhook or API)
EXPOSE 5000

# Define the command to run the bot
CMD ["python", "bot.py"]
