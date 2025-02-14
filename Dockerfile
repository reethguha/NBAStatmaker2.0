# Use an official Python image
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy project files
COPY nba_statmaker.py .
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the Flask port
EXPOSE 5000

# Run the Flask app using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "nba_statmaker:app"]