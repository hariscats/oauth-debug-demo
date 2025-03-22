# oauth-debug-demo

A demo repo for visualizing and debugging OAuth flows.

## Overview

This repo demonstrates how to:

- Visualize the OAuth flow using Mermaid sequence diagram
- Obtain an access token from Entra ID using the client credentials flow.
- Decode the access token to inspect its claims.
- Use the token to call APIs behind APIM.

It includes:

- A **REST Client demo** for VS Code.
- A **Python script** that programmatically demonstrates the OAuth flow.
- **Documentation** with an OAuth flow diagram provided as both an PNG (for visual reference) and its Mermaid source code (provided as plain text) for sample diagram as code.

## Setup

1. **Clone the Repo:**
   ```bash
   git clone https://github.com/yourusername/oauth-debug-demo.git
   cd oauth-debug-demo
   ```

2. **Configure Environment:**
   - Copy `http-client.env.json.example` to `http-client.env.json` and fill in your values.
   - Create or use existing `.env` file in the repo root for the Python script.
   - **Update `.vscode/settings.json`:**  
     Fill out the settings (e.g., REST Client environment variables) with your specific values.

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### REST Client Demo (VS Code)
- Open `oauth-demo.http` in VS Code.
- Use the REST Client extension to send the token request and subsequent API call.
- The workflow will:
  1. Obtain an access token from Azure AD.
  2. Decode and display the token claims.
  3. Use the token to call the pet store API behind APIM.

### Python Demo
- Run the Python script (adjust the HTTP method and payload as needed):
   ```bash
   python scripts/python-oauth-demo.py --method POST --payload '{"id":10,"name":"doggie","category":{"id":1,"name":"Dogs"},"photoUrls":["string"],"tags":[{"id":0,"name":"string"}],"status":"available"}'
   ```

## Documentation

- **OAuth Flow Diagram:**
  - **Visual Diagram:**  
    View the scalable diagram at `docs/oauth-flow-diagram.svg`.
  - **Mermaid Source Code:**  
    The Mermaid code is provided in `docs/oauth-flow-diagram.mmd`. (Note: To prevent GitHub from rendering the Mermaid diagram automatically, the code is fenced as plain text using a language identifier like `text` instead of `mermaid`.)
  
## Additional Info

This demo repository is intended for educational and debugging purposes. In production environments, avoid committing sensitive credentials and ensure proper security practices.