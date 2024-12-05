#!/bin/bash
# Step 3.3: Create the Anaconda environment if it doesn't exist
if ! conda info --envs | grep -q 'datasnake-test-env'; then
echo 'Creating Anaconda environment...'
conda create --n datasnake-test-env python=3.8 -y
else
echo 'Environment already exists.'
fi

# Step 3.4: Activate the environment
conda activate datasnake-test-env
# conda install pip
pip3 install cassandra-driver
cd /home/dev/testing-cassandra-remote
# Step 3.5: Install the required dependencies (from requirements.txt)
if [ -f "testing-cassandra-remote/requirements.txt" ]; then
pip3 install -r testing-cassandra-remote/requirements.txt
fi
cassandra -e "source db-script.cql"

# Step 3.6: Run your Python script or entry point (e.g., main.py)
python3 /home/dev/testing-cassandra-remote/main.py
