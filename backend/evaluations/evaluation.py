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
        return res.json()
    except Exception as e:

        if e.status_code == 400:
                print(f"400 Bad Request Error: {e.message}")
                try:
                    error_details = e.response.json()
                    print("error details json")
                    print(error_details)
                    if "error" in error_details:
                        inner_error = error_details.get("error", {}).get("innererror", {})
                        print(f"Inner Error: {inner_error}")
                        return inner_error
                except Exception:
                    print("Could not parse detailed error from response.")
        else:
            print(f"An unexpected API error occurred: {e.status_code} - {e.message}")

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

    # Extract question and safety score
    question = item["Question"]
    options = AnalyzeTextOptions(
        text=question,
        categories=["Hate", "SelfHarm", "Sexual", "Violence"]
    )
    analyze_text_result = client.analyze_text(options)
    input_safety_score = analyze_text_result.as_dict()

    # Call the function to get a response 
    results = invoke_sql_query(question, thread_id)

    # Get output safety scores 
    if results.get("content_filter_result"):
        output_safety_score = results["content_filter_result"]
    elif results.get("content"):
        results = results["content"]
        options = AnalyzeTextOptions(
            text=results,
            categories=["Hate", "SelfHarm", "Sexual", "Violence"]
        )
        analyze_text_result = client.analyze_text(options)
        output_safety_score = analyze_text_result.as_dict()
    else:
        output_safety_score = "undefined"

    # Store results
    output_data["Results"].append({
        "Question": question,
        "Answer": results,
        "InputSafetyScores": input_safety_score,
        "OutputSafetyScores": output_safety_score
    })

    # Print scores for debugging
    print(f"Question: {question}")
    print(f"Answer: {results}")
    print(f"InputSafetyScores: {input_safety_score}")
    print(f"OutputSafetyScores: {output_safety_score}")
    print("-" * 50)

# Write results to the output JSON file
with open(file_path_output, 'w', encoding='utf-8') as file_output:
    json.dump(output_data, file_output, indent=4, ensure_ascii=False)

print(f"Results saved to {file_path_output}")