# Base image
FROM python:3.9

# Install necessary dependencies, including Java
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    openjdk-11-jre && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Copy the requirements file
COPY requirements.txt .

# Install numpy first to avoid binary incompatibility issues
RUN pip install --no-cache-dir numpy

# Install the rest of the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Download spaCy model
RUN python -m spacy download en_core_web_sm

# Copy the entire app directory
COPY . .

# Expose the default port for Streamlit
EXPOSE 8501

# Command to run the Streamlit app
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.enableCORS=false", "--server.enableXsrfProtection=false"]
