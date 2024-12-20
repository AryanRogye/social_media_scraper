FROM python:3.11-slim

WORKDIR /app

# Copy project files
COPY . /app

# Create a virtual environment and install dependencies
RUN python3 -m venv /venv && \
    /venv/bin/pip install --upgrade pip && \
    /venv/bin/pip install -r requirements.txt

# Ensure the bash scripts are executable
RUN chmod +x /app/rung /app/runp

# Set the Python virtual environment as the default Python
ENV PATH="/venv/bin:$PATH"

# Allow arguments to specify which script to run
ENTRYPOINT ["bash", "-c"]
CMD ["/app/rung"]
