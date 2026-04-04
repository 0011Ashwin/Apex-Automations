#!/bin/bash

# --- Function for error handling ---
handle_error() {
  echo -e "\n\n*******************************************************"
  echo "Error: $1"
  echo "*******************************************************"
}

# --- Part 2: Install Dependencies and Run Billing Setup ---
# This part runs for both existing and newly created projects.
echo -e "\n--- Installing Python dependencies ---"
pip install --upgrade --user google-cloud-billing || handle_error "Failed to install Python libraries."

echo -e "\n--- Running the Billing Enablement Script ---"
python3 billing-enablement.py || handle_error "The billing enablement script failed. See the output above for details."

echo -e "\n--- Full Setup Complete ---"
