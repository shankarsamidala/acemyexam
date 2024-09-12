# Base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Download spaCy model
RUN python -m spacy download en_core_web_sm

# Copy the entire app directory
COPY . .

# Expose the default port for Streamlit
EXPOSE 8501


# Command to run the Streamlit app
CMD ["streamlit", "run", "app/main.py", "--server.port=8501", "--server.enableCORS=false", "--server.enableXsrfProtection=false"]
