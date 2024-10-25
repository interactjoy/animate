#!/bin/bash

# Restart Miniconda
cd /notebooks/Miniconda
source /notebooks/Miniconda/etc/profile.d/conda.sh
echo "Conda version:"
conda --version

# Navigate to ToonCrafter and activate environment
cd /notebooks/animate
conda activate animate
echo "Activated environment: animate"

# Run the Gradio app
echo "Welcome back. Running Animation Software..."
python gradio_app.py
