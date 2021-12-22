FROM quay.io/centos/centos:stream9

# Install OS dependencies
RUN \
  yum update && \
  yum install python3-pip openssh-clients -y

# Copy the repo to the Container 
COPY . .

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Define default command.
CMD ["bash"]