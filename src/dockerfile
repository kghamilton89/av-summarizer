# Use the official Python image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy only requirements first for better caching
COPY src/requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the rest of the application files
COPY src/ /app/

# Expose the Flask app's port
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=transcribe_summarize_api.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

# Ensure the uploads directory exists
RUN mkdir -p /app/uploads

# Run the application with Gunicorn for production
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "transcribe_summarize_api:app"]
