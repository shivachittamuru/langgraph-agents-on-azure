# Generating Client SDKs for the SQL Agent API

This guide explains how to generate client SDKs for the SQL Agent API using OpenAPI Generator. Follow the steps below to generate SDKs in Python or other programming languages.

---

## Prerequisites

1. Ensure you have the OpenAPI spec file (`openapi-spec.yaml`) available.
2. Install **OpenAPI Generator**:
    - Using npm:
      ```cli
      npm install @openapitools/openapi-generator-cli -g
      ```
    - Or download the JAR file from [OpenAPI Generator](https://openapi-generator.tech/).

---

## Steps to Generate a Python Client SDK

1. **Run the OpenAPI Generator Command**:
    ```cli
    openapi-generator-cli generate -i c:\Users\shchitt\OneDrive - Microsoft\Desktop\langchain-ai\langgraph-agents-on-azure\backend\api\openapi-spec.yaml -g python -o ./python-client
    ```
    - `-i`: Path to the OpenAPI spec file.
    - `-g`: Target language (`python` in this case).
    - `-o`: Output directory for the generated SDK (`./python-client`).

2. **Install the Generated SDK**:
    - Navigate to the output directory:
      ```cli
      cd ./python-client
      ```
    - Install the SDK locally:
      ```cli
      pip install .
      ```

3. **Use the SDK in Your Python Code**:
    - Import the generated client and use it:
      ```python
      from python_client import ApiClient, DefaultApi

      # Initialize the client
      api_client = ApiClient()
      api_instance = DefaultApi(api_client)

      # Example usage
      response = api_instance.invoke_sql_agent({"message": "Find albums released by artists with more than 5 albums."})
      print(response)
      ```

---

## Generating SDKs for Other Languages

To generate SDKs for other languages, replace `python` in the `-g` option with the desired language. For example:

- **JavaScript/TypeScript**:
  ```cli
  openapi-generator-cli generate -i c:\Users\shchitt\OneDrive - Microsoft\Desktop\langchain-ai\langgraph-agents-on-azure\backend\api\openapi-spec.yaml -g typescript-axios -o ./js-client
  ```

- **Java**:
  ```cli
  openapi-generator-cli generate -i c:\Users\shchitt\OneDrive - Microsoft\Desktop\langchain-ai\langgraph-agents-on-azure\backend\api\openapi-spec.yaml -g java -o ./java-client
  ```

Refer to the [OpenAPI Generator Documentation](https://openapi-generator.tech/docs/generators) for a full list of supported languages.

---

## Notes

- Ensure the OpenAPI spec file is valid and up-to-date.
- You can customize the generated SDK using configuration options. Refer to the OpenAPI Generator documentation for advanced usage.
