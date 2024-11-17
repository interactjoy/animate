# Install

#!/bin/bash

git clone https://github.com/interactjoy/animate.git

cd /notebooks/animate || { echo "Failed to change directory"; exit 1; }

chmod +x install.sh

./install.sh || { echo "Installation failed"; exit 1; }

# Run

chmod +x run.sh

/notebooks/animate/run.sh
