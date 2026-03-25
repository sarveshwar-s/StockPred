FROM python:3.11-slim

# Set a non-root user to run the application
RUN adduser --disabled-password myuser
USER myuser

# Set work directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Command to run the application
CMD ["python", "app.py"]