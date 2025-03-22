# oauth-debug-demo

A demo repo for learning how to debug OAuth flows that involve Entra ID and a sample API behind APIM.

## Overview

This repo demonstrates:
- Obtaining an access token from Entra ID using client credential flow.
- Decoding token claims for debugging.
- Using the token to call APIs behind APIM.

It includes a REST Client demo (VS Code) and a Python script.

## Setup

1. **Clone the Repo:**
   ```bash
   git clone https://github.com/yourusername/oauth-debug-demo.git
   cd oauth-debug-demo
   ```

2. **Configure Environment:**
   - Use `.env` file for the Python script.
   - **Update `.vscode/settings.json`:**  
     Fill out the settings (e.g., REST Client environment variables) with your specific values.

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### REST Client Demo (VS Code)
- Open `oauth-demo.http` in VS Code.
- Use the REST Client extension to send the token request and API call.

### Python Demo
- Run the script (adjust HTTP method and payload as needed):
   ```bash
   python scripts/python-oauth-demo.py --method POST --payload '{"id":10,"name":"doggie","category":{"id":1,"name":"Dogs"},"photoUrls":["string"],"tags":[{"id":0,"name":"string"}],"status":"available"}'
   ```

## Docs

Check out the docs for visual sequence diagram of the OAuth flow and jwt.io for another way to inspect claims in JWT.

