# Use the provided base image
FROM python:3.11-slim

# Set the working directory to /app
WORKDIR /app

# Create a non-root user
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

# Set the user for subsequent commands
USER appuser

# Copy the configuration file into the container at /app
COPY config.yaml .
COPY ../requirements.txt /usr/local//bin/requirements.txt
#COPY ../entrypoint.sh /usr/local/bin/entrypoint.sh
#RUN chmod +x /usr/local/bin/entrypoint.sh
#RUN pip install --upgrade pip
RUN python3 -m pip install --no-cache-dir -r requirements.txt

# Make sure your docker/entrypoint.sh is executable
#RUN chmod +x ./docker/entrypoint.sh

# Expose the necessary port
EXPOSE 50051
#/tcp
# Override the CMD instruction with your desired command and arguments
# WARNING: FOR PROD DO NOT USE `--detailed_debug` it slows down response times, instead use the following CMD
# CMD ["--port", "4000", "--config", "config.yaml"]

CMD ["python3", "server.py"]
