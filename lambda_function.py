import json
import requests
from bs4 import BeautifulSoup

def lambda_handler(event, context):
    try:
        # Get the target URL from the request body
        body = json.loads(event.get("body", "{}"))
        target_url = body.get("url")

        if not target_url:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Please provide a 'url' in the request body."})
            }

        # Send a GET request to the target URL
        response = requests.get(target_url)
        
        if response.status_code != 200:
            return {
                "statusCode": 500,
                "body": json.dumps({"error": f"Failed to fetch the URL: {response.status_code}"})
            }

        # Parse the page content with BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # Example: Extract the title and all links
        page_title = soup.title.string if soup.title else "No title found"
        links = [a.get("href") for a in soup.find_all("a", href=True)]

        # Build the response
        result = {
            "url": target_url,
            "title": page_title,
            "links": links[:10]  # Limit to the first 10 links for brevity
        }

        return {
            "statusCode": 200,
            "body": json.dumps(result)
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
