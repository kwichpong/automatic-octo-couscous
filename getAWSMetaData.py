import requests
import json

def get_instance_metadata(key=None):
    # Define the base URL for instance metadata
    base_url = "http://169.254.169.254/latest/meta-data/"
    # Define the URL to fetch the IMDSv2 token
    token_url = "http://169.254.169.254/latest/api/token"

    try:
        # Step 1: Request an IMDSv2 Token
        print("Requesting IMDSv2 token...")
        token_response = requests.put(token_url, headers={"X-aws-ec2-metadata-token-ttl-seconds": "21600"}, timeout=5)
        print("IMDSv2 token request status code:", token_response.status_code)

        if token_response.status_code != 200:
            print("Failed to retrieve IMDSv2 token. Status code:", token_response.status_code)
            return json.dumps({"error": "Failed to get IMDSv2 token"}, indent=4)

        # Extract the token from the response
        token = token_response.text
        print("IMDSv2 token retrieved successfully.")
        headers = {"X-aws-ec2-metadata-token": token}

        # Step 2: Retrieve Metadata
        metadata_url = base_url + (key if key else "")  # Construct URL based on the key
        print(f"Fetching metadata from: {metadata_url}")

        # Send a request to fetch the metadata
        response = requests.get(metadata_url, headers=headers, timeout=5)
        print("Response status code:", response.status_code)

        if response.status_code == 200:
            if key:
                # If a specific key was requested, return its value
                print(f"Metadata retrieved successfully for key: {key}")
                return json.dumps({key: response.text}, indent=4)
            else:
                # Otherwise, retrieve all available metadata keys
                metadata_keys = response.text.split('\n')
                metadata = {}
                print("Retrieved metadata keys:", metadata_keys)
                for meta_key in metadata_keys:
                    print(f"Fetching metadata for key: {meta_key}")
                    meta_response = requests.get(base_url + meta_key, headers=headers, timeout=5)
                    print(f"Response status code for key {meta_key}: {meta_response.status_code}")
                    if meta_response.status_code == 200:
                        metadata[meta_key] = meta_response.text  # Store key-value pairs in dictionary
                print("All metadata retrieved successfully.")
                return json.dumps(metadata, indent=4)
        else:
            print("Unable to retrieve metadata. Status code:", response.status_code)
            return json.dumps({"error": "Unable to retrieve metadata"}, indent=4)
    
    except requests.exceptions.RequestException as e:
        # Handle exceptions such as network errors
        print("Request exception occurred:", str(e))
        return json.dumps({"error": str(e)}, indent=4)

if __name__ == "__main__":
    import argparse
    print("Initializing AWS Metadata Retrieval Script...")
    parser = argparse.ArgumentParser(description="Retrieve AWS instance metadata.")
    parser.add_argument("--key", type=str, help="Metadata key to retrieve", required=False)
    args = parser.parse_args()
    print("Starting metadata retrieval...")
    result = get_instance_metadata(args.key)
    print("Metadata retrieval process completed.")
    print(result)
