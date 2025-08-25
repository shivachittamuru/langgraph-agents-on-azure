import os
import requests
import uuid
import json
import ast

from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions
from azure.core.credentials import AzureKeyCredential

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(), override=True)

api_url = "http://localhost:8000"   # FastAPI uvicorn URL with port 8000
# api_url = "http://localhost:80"     # Docker container URL since we exposed the port 80
# api_url = "https://chinook-backend-api.azurewebsites.net"  # Azure Web App URL
# api_url = "http://20.118.71.68:80"  # AKS URL

endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

def invoke_sql_query(message, thread_id):
    try:        
        res = requests.post(f"{api_url}/sql-invoke",
            json={
                "message": message,
                "thread_id": thread_id
            }
        )
        # print(res.json())
        return res.json()["content"]
    except Exception as e:
        # print("Exception thrown")
        # print(e)
        error_str = str(e)

        if "content_filter_result" in error_str:
            # Convert the outer string into a Python dict
            outer = ast.literal_eval(error_str)

            # Extract the inner "Error code: 400 - {...}" part
            detail_str = outer["detail"].split("Error code: 400 - ", 1)[1]

            # Parse the inner dict
            inner = ast.literal_eval(detail_str)

            # Finally grab the content_filter_result
            content_filter_result = inner["error"]["innererror"]
            print(content_filter_result)
            return content_filter_result

client = ContentSafetyClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(key) 
)

# Define the input and output file paths
file_path_input = './data/evaluation_input.json'
file_path_output = './data/evaluation_output.json'

# Read input JSON file
with open(file_path_input, 'r', encoding='utf-8') as file:
    dataset = json.load(file)

# Prepare output structure
output_data = {"Results": []}

# Process each question
for item in dataset:
    thread_id = str(uuid.uuid4())  # Generate unique thread ID

    # Extract question and ground truth
    question = item["Question"]

    # Call the function to get a response 
    results = invoke_sql_query(question, thread_id)

    # Get safety scores 
    if results.get("content_filter_result"):
        safety_scores = results["content_filter_result"]
    else:
        options = AnalyzeTextOptions(
            text=results,
            categories=["Hate", "SelfHarm", "Sexual", "Violence"]
        )
        result = client.analyze_text(options)
        safety_scores = result.as_dict()

    # Store results
    output_data["Results"].append({
        "Question": question,
        "Answer": results,
        "SafetyScores": safety_scores
    })

    # Print scores for debugging
    print(f"Question: {question}")
    print(f"Answer: {results}")
    print(f"SafetyScores: {safety_scores}")
    print("-" * 50)

# Write results to the output JSON file
with open(file_path_output, 'w', encoding='utf-8') as file_output:
    json.dump(output_data, file_output, indent=4, ensure_ascii=False)

print(f"Results saved to {file_path_output}")