# Use an official Python runtime as the base image
FROM --platform=amd64 python:3.11

# Set the working directory in the container
# Both the utils and src folders will be mounted as volumes, please see docker-compose.yaml
WORKDIR /app

# Copy the requirements file to the working directory
COPY ./books_database_2/requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
# Install reloadium for hot reloading
# This allows us to make changes to the code without having to rebuild the container
RUN pip install reloadium

# Set the command to run the application
CMD reloadium run "books_database_2/src/app.py"
