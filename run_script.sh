#!/bin/bash
# Step 3.4: Activate the environment
conda activate devenv
conda install pip
cd /home/dev/testing-cassandra-remote
# Step 3.5: Install the required dependencies (from requirements.txt)
if [ -f "testing-cassandra-remote/requirements.txt" ]; then
pip3 install -r testing-cassandra-remote/requirements.txt
fi

# Step 3.6: Run your Python script or entry point (e.g., main.py)
python3 /home/dev/testing-cassandra-remote/main.py
