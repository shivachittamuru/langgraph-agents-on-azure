import os
import requests
import uuid
import json

from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(), override=True)

api_url = "http://localhost:8000"   # FastAPI uvicorn URL with port 8000
# api_url = "http://localhost:80"     # Docker container URL since we exposed the port 80
# api_url = "https://chinook-backend-api.azurewebsites.net"  # Azure Web App URL
# api_url = "http://20.118.71.68:80"  # AKS URL

model_config = {
    "azure_endpoint": os.environ.get("AZURE_OPENAI_ENDPOINT"),
    "api_key": os.environ.get("AZURE_OPENAI_API_KEY"),
    "azure_deployment": os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME"),
}

def invoke_sql_query(message, thread_id):
    try:        
        res = requests.post(f"{api_url}/sql-invoke",
            json={
                "message": message,
                "thread_id": thread_id
            }
        )
        print(res.json()["content"])
        return res.json()["content"]
    except Exception as e:
        print(e)

def check_text(client, text):
    try:
        result = client.analyze_text(
            input_text=text,
            categories=["Hate", "SelfHarm", "Sexual", "Violence"]
        )
        return result
    except Exception as e:
        return {"error": str(e)}

# Define the input and output file paths
file_path_input = './data/evaluation_input.json'
file_path_output = './data/evaluation_output.json'

# Read input JSON file
with open(file_path_input, 'r', encoding='utf-8') as file:
    dataset = json.load(file)

# Prepare output structure
output_data = {"Results": []}

# Declare client
client = ContentSafetyClient(
    endpoint=model_config["azure_endpoint"],
    credential=AzureKeyCredential(model_config["api_key"])
)

# Process each question
for item in dataset:
    thread_id = str(uuid.uuid4())  # Generate unique thread ID

    # Extract question and ground truth
    question = item["Question"]

    # Call the function to get a response 
    results = invoke_sql_query(question, thread_id)

    # Compute relevance and similarity scores 
    safety_score = check_text(client=client, text=results)

    # Store results
    output_data["Results"].append({
        "Question": question,
        "Answer": results,
        "SafetyScores": safety_score
    })

    # Print scores for debugging
    print(f"Question: {question}")
    print(f"Answer: {results}")
    print(f"SafetyScores: {safety_score}")
    print("-" * 50)

# Write results to the output JSON file
with open(file_path_output, 'w', encoding='utf-8') as file_output:
    json.dump(output_data, file_output, indent=4, ensure_ascii=False)

print(f"Results saved to {file_path_output}")