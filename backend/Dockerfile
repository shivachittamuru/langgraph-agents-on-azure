# Use an official Python runtime as a base image
FROM python:3.12.3-slim

# Set the working directory in the container
WORKDIR /app

# Set PYTHONPATH environment variable
ENV PYTHONPATH=/app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
# RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 80 (optional, usually not needed unless you want to explicitly document the port in the Dockerfile)
EXPOSE 80

# Run the Uvicorn server to start FastAPI on port 80
# uvicorn main:app --host 0.0.0.0 --port 80
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"] 
CMD ["python", "main.py"]