# Use Python 3.11 base image (stable)
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Copy all project files
COPY . .

# Upgrade pip and install dependencies
RUN pip install --upgrade pip wheel setuptools
RUN pip install -r requirements.txt

# Expose Render port
ENV PORT=10000
EXPOSE 10000

# Start your bot
CMD ["python", "bot.py"]
