#!/bin/bash
# Install Asterisk and Python dependencies in Google Cloud Shell

sudo apt-get update
sudo apt-get install -y asterisk python3-pip

pip3 install python-telegram-bot flask
echo "Installation complete."
