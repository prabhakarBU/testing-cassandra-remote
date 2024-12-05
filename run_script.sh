#!/bin/bash
# Step 3.3: Create the Anaconda environment if it doesn't exist
if ! conda info --envs | grep -q 'datasnake-test-env'; then
echo 'Creating Anaconda environment...'
conda create --name datasnake-test-env python=3.8 -y
else
echo 'Environment already exists.'
fi

# Step 3.4: Activate the environment
conda init
conda activate datasnake-test-env
# conda install pip
pip3 install cassandra-driver
cd /home/dev/testing-cassandra-remote
# Step 3.5: Install the required dependencies (from requirements.txt)
if [ -f "/home/dev/testing-cassandra-remote/requirements.txt" ]; then
pip3 install -r /home/dev/testing-cassandra-remote/requirements.txt
fi

# Verify Polars installation
if ! python3 -c "import polars" &>/dev/null; then
    echo "Polars is not installed. Installing it explicitly..."
    pip3 install polars
fi

# Verify boto3 installation
if ! python3 -c "import boto3" &>/dev/null; then
    echo "boto3 is not installed. Installing it explicitly..."
    pip3 install boto3
fi

CASSANDRA_HOST="127.0.0.1"
USERNAME="cassandra"
PASSWORD="cassandra"
CQL_FILE="/home/dev/testing-cassandra-remote/db-script.cql"
cqlsh $CASSANDRA_HOST -u $USERNAME -p $PASSWORD -f $CQL_FILE


# Step 3.7: S3 Bucket Creation (Dynamic)
project_name="testing-cassandra-remote"
bucket_name="s3://$project_name-bucket"

# Check if the bucket exists
if ! s3cmd ls | grep -q "$bucket_name"; then
    echo "Bucket does not exist. Creating bucket: $bucket_name"
    s3cmd mb "$bucket_name"
else
    echo "Bucket $bucket_name already exists."
fi

# Step 3.6: Run your Python script or entry point (e.g., main.py)
python3 /home/dev/testing-cassandra-remote/test-insert-cassandra.py
