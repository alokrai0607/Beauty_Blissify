# Use the official Python image as a base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app code
COPY . .

# Set environment variables
ENV PORT=8000
ENV HOST=0.0.0.0

# Expose the port FastAPI will run on
EXPOSE $PORT

# Run the application with Gunicorn and Uvicorn worker class
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "app.main:app", "--bind", "0.0.0.0:8000"]
