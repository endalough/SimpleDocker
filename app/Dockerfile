# Use an official python runtume as a parent image
FROM python:3.10.12

# Set the working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app code
COPY . .

# Run the FastAPI app with Uvicorn
CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]



