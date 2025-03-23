# Use an official Python image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy dependency files first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files
COPY . .

# Expose the port Django runs on
EXPOSE 8000

# Set the entrypoint script
ENTRYPOINT ["sh", "./entrypoint.sh"]
