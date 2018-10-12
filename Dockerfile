FROM python:3.6.6-slim-jessie

# Install OS dependencies
RUN \
  apt-get update && \
  apt-get install -y gcc openssh-client git iputils-ping make && \
  rm -rf /var/lib/apt/lists/*

# Copy the repo to the Container 
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Define default command.
CMD ["bash"]
