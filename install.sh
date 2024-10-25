#!/bin/bash

# Enable error handling
set -e

# Function to display error message and exit
error_exit() {
    echo "Error on line $1: $2"
    exit 1
}

# Trap any command that exits with a non-zero status
trap 'error_exit $LINENO "$BASH_COMMAND"' ERR

# Step 1: Clone the Github Repo
echo "Cloning the GitHub repository..."
if [ ! -d "animate" ]; then
    git clone https://github.com/interactjoy/animate.git
else
    echo "Repository already cloned, skipping..."
fi

# Step 2: Install MiniConda
echo "Downloading and installing Miniconda..."
if [ ! -d "/notebooks/Miniconda" ]; then
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
    bash Miniconda3-latest-Linux-x86_64.sh -b -p /notebooks/Miniconda
    export PATH="/notebooks/Miniconda/bin:$PATH"
    source ~/.bashrc
else
    echo "Miniconda already installed, skipping..."
fi

# Step 3: Create Conda environment
echo "Creating Conda environment..."
if conda info --envs | grep -q "animate"; then
    echo "Conda environment 'animate' already exists, skipping..."
else
    conda create -n animate python=3.8.5 -y
fi

# Step 4: Initialize and activate Conda environment
echo "Initializing and activating Conda environment..."
conda init
source ~/.bashrc
conda activate animate

# Step 5: Navigate to the project folder
echo "Navigating to the project folder..."
cd /notebooks/animate

# Step 6: Make a Folder in checkpoints
echo "Creating checkpoint folder..."
mkdir -p checkpoints/tooncrafter_512_interp_v1

# Step 7: Download the Model to the Checkpoint folder
echo "Downloading model..."
wget -P checkpoints/tooncrafter_512_interp_v1/ https://huggingface.co/Doubiiu/ToonCrafter/resolve/main/model.ckpt

# Step 8: Install requirements
echo "Installing requirements..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    echo "requirements.txt not found, skipping requirements installation."
fi

# Step 9: Run the configuration script
echo "Running the configuration script..."
if [ -f "scripts/run.sh" ]; then
    sh scripts/run.sh
else
    echo "Configuration script not found, skipping."
fi

# Step 10: Launch the program
echo "Launching the program..."
if [ -f "gradio_app.py" ]; then
    python gradio_app.py
else
    echo "Program script gradio_app.py not found. Please check the installation."
fi

echo "Installation and setup complete!"