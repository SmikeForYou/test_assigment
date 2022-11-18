# Fedex API Test Assigment
## Requirements
    Python 3.6+
## Getting started
### Setup virtual environment
```bash
  python3.6 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
```
### Fill and apply environment variables
```bash
    cp .env.example .env
    # Put required variables to .env file
    export $(grep -v '^#' .env | xargs) # Apply vars from .env to your environment
```
## Usage
### Run server
```bash
   python3.6 main.py
```
### Track you shipment

After server started follow [tracking page url](http://127.0.0.1:8000/) and use your tracking number for get info