#!/bin/bash

# Restart Miniconda
cd /notebooks/miniconda3
source /notebooks/miniconda3/etc/profile.d/conda.sh
echo "Conda version:"
conda --version

# Navigate to ToonCrafter and activate environment
cd /notebooks/ToonCrafter
conda activate tooncrafter
echo "Activated environment: tooncrafter"

# Run the Gradio app
echo "Running gradio_app.py..."
python gradio_app.py
