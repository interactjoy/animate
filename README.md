# Install

#!/bin/bash

# Clone the repository
git clone https://github.com/interactjoy/animate.git

# Change to the project directory
cd /notebooks/animate || { echo "Failed to change directory"; exit 1; }

# Make the install script executable
chmod +x install.sh

# Run the install script
./install.sh || { echo "Installation failed"; exit 1; }

# Run

chmod +x run.sh

/notebooks/animate/run.sh
