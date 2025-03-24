import os
import sys
import json
import requests
import logging
import argparse
import jwt  # PyJWT package: pip install pyjwt
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load configuration from environment variables
TENANT_ID = os.getenv("TENANT_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
SCOPE = os.getenv("SCOPE")
APIM_ENDPOINT = os.getenv("APIM_ENDPOINT")
SUBSCRIPTION_KEY = os.getenv("SUBSCRIPTION_KEY")  # Optional

# Construct the Azure AD token endpoint URL
TOKEN_ENDPOINT = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"

def get_access_token():
    """Retrieve an access token using the client credentials flow."""
    payload = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "scope": SCOPE,
    }
    logger.info("Requesting token from Azure AD...")
    token_response = requests.post(TOKEN_ENDPOINT, data=payload)
    if token_response.status_code != 200:
        logger.error("Token request failed: %s %s", token_response.status_code, token_response.text)
        sys.exit(1)
    token_data = token_response.json()
    access_token = token_data.get("access_token")
    if not access_token:
        logger.error("Access token not found in the response.")
        sys.exit(1)
    logger.info("Access token acquired.")
    
    # Decode the token to inspect claims (without verifying signature)
    try:
        claims = jwt.decode(access_token, options={"verify_signature": False})
        logger.info("Decoded token claims:\n%s", json.dumps(claims, indent=2))
        print("Decoded Token Claims:")
        print(json.dumps(claims, indent=2))
    except Exception as e:
        logger.error("Failed to decode token: %s", e)
    
    return access_token

def call_api(endpoint, method="GET", payload=None, access_token=None):
    """Call the specified API endpoint using the given HTTP method and payload."""
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    # Optionally include the subscription key header if provided
    if SUBSCRIPTION_KEY:
        headers["Ocp-Apim-Subscription-Key"] = SUBSCRIPTION_KEY

    logger.info("Calling API endpoint %s with method %s", endpoint, method.upper())
    
    if method.upper() == "GET":
        response = requests.get(endpoint, headers=headers)
    elif method.upper() == "POST":
        response = requests.post(endpoint, headers=headers, json=payload)
    elif method.upper() == "PUT":
        response = requests.put(endpoint, headers=headers, json=payload)
    elif method.upper() == "DELETE":
        response = requests.delete(endpoint, headers=headers)
    else:
        logger.error("HTTP method %s not supported.", method)
        sys.exit(1)
        
    return response

def main():
    parser = argparse.ArgumentParser(description="Test APIs behind APIM with OAuth authentication.")
    parser.add_argument("--method", type=str, default="GET", help="HTTP method to use (GET, POST, PUT, DELETE)")
    parser.add_argument("--payload", type=str, help="JSON payload as a string (for POST/PUT requests)")
    parser.add_argument("--payload-file", type=str, help="Path to JSON payload file (for POST/PUT requests)")
    parser.add_argument("--endpoint", type=str, default=APIM_ENDPOINT, help="API endpoint URL to test")
    args = parser.parse_args()

    # Get access token from Azure AD and decode it
    token = get_access_token()

    # Convert payload string to dictionary if provided
    json_payload = None
    
    # Check if payload file is provided
    if args.payload_file:
        try:
            logger.info(f"Loading payload from file: {args.payload_file}")
            with open(args.payload_file, 'r') as f:
                json_payload = json.load(f)
            logger.info(f"Payload loaded successfully from file")
        except Exception as e:
            logger.error(f"Failed to load JSON payload from file: {e}")
            sys.exit(1)
    # If no payload file but direct payload string is provided
    elif args.payload:
        try:
            json_payload = json.loads(args.payload)
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON payload: {e}")
            sys.exit(1)

    # Call the API and print response
    response = call_api(args.endpoint, method=args.method, payload=json_payload, access_token=token)
    logger.info(f"API response status: {response.status_code}")
    logger.info(f"Response body: {response.text}")
    print("Response Status:", response.status_code)
    print("Response Body:", response.text)

if __name__ == "__main__":
    main()
