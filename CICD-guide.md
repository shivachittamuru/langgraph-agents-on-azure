# CI/CD Goals, Success Criteria, and Best Practices for Text2SQL Agent Application

## Overview
This document outlines the goals and success criteria for implementing Continuous Integration (CI) and Continuous Deployment (CD) pipelines for the Text2SQL Agent application, which leverages the LangGraph agentic framework, FastAPI, and containerized deployments to Azure.

---


## Goals

### 1. Build & Evaluate (CI)
- **Automated Build:**
  - On every push to main or feature branches, build the backend Docker image and run the container locally in the CI runner.
- **Automated Evaluation:**
  - Run the agent evaluation suite against the running container to validate correctness and performance.
- **Feedback & Artifacts:**
  - Upload evaluation results and logs as workflow artifacts for review.
- **Fail Fast:**
  - CI fails if any build, test, or evaluation step fails. PRs cannot be merged unless CI passes.

### 2. Dev Deployment (CD)
- **Automated Container Build & Push:**
  - Build and push the backend Docker image to Azure Container Registry (ACR) after successful CI.
- **Azure App Service Deployment:**
  - Deploy the backend container to Azure App Service for development/staging, using secure environment variables from GitHub secrets.
- **Automated Provisioning:**
  - Ensure App Service Plan and Web App are created if they do not exist.

### 3. Prod Deployment (CD)
- **AKS Deployment:**
  - Build and push the backend Docker image to ACR, then deploy to Azure Kubernetes Service (AKS) for production.
- **Kubernetes Best Practices:**
  - Use secrets for ACR access, create namespace if needed, and expose the backend via a LoadBalancer service.
- **Traceability & Rollback:**
  - Maintain traceability from commit to deployment and enable rollback to previous versions.

---


## Success Criteria

### Build & Evaluate (CI)
- [ ] Every push/PR triggers the CI workflow automatically.
- [ ] The backend Docker image is built and runs successfully in the CI environment.
- [ ] The FastAPI backend container responds to health checks in CI.
- [ ] The evaluation suite runs against the running container and produces accurate pass/fail results.
- [ ] Evaluation results and logs are uploaded as workflow artifacts.
- [ ] CI fails if any build, test, or evaluation step fails.
- [ ] PRs cannot be merged unless CI passes.

### Dev Deployment (CD)
- [ ] Docker images are built and pushed to ACR after successful CI.
- [ ] The backend is deployed to Azure App Service (dev) with correct environment variables from secrets.
- [ ] App Service Plan and Web App are created if missing.
- [ ] The backend is accessible at the expected endpoint after deployment.
- [ ] Deployment is automated and does not require manual intervention.

### Prod Deployment (CD)
- [ ] Docker images are built and pushed to ACR after successful CI.
- [ ] The backend is deployed to AKS with correct configuration, secrets, and imagePullSecrets.
- [ ] The chinook namespace and ACR secret are created if missing.
- [ ] The backend is exposed via a LoadBalancer service and external IP is available.
- [ ] Rollback to previous deployments is possible and documented.
- [ ] Deployment status and logs are visible in GitHub Actions.

---


## Stretch Goals (Optional)
- Automated deployment of frontend container to App Service or AKS.
- Blue/green or canary deployments for production.
- Automated integration tests against deployed endpoints.
- Slack/Teams notifications for pipeline status.
- Infrastructure as Code (Bicep/Terraform) for Azure resources and environments.

---


---

## Important Steps and Best Practices

### 1. Use OIDC for Secure Azure Login
- Configure federated identity credentials for your GitHub Actions service principal to enable passwordless, secure authentication to Azure.
- Add required permissions in your workflow: `id-token: write` and `contents: read`.

### 2. Build and Test in Containers
- Build and run your backend as a Docker container in CI to ensure environment parity with production.
- Run evaluations inside the container for consistency and to avoid dependency mismatches.

### 3. Use Azure Container Registry (ACR)
- Push Docker images to ACR for both dev and prod deployments.
- Use ACR access tokens or service principal credentials for secure image pulls in AKS.

### 4. Automated Resource Provisioning
- Use CLI steps to create App Service Plans, Web Apps, AKS clusters, and Kubernetes namespaces if they do not exist.
- Make all infrastructure creation idempotent to support repeatable deployments.

### 5. Secure Secrets and Environment Variables
- Store all sensitive values (API keys, DB credentials, etc.) in GitHub secrets and inject them as environment variables at deploy time.
- Never hard-code secrets in code or workflow files.

### 6. Health Checks and Rollbacks
- Always check backend health after deployment.
- Ensure you can rollback to previous images or deployments in case of failure.

### 7. Artifact and Log Management
- Upload evaluation results and logs as workflow artifacts for traceability and debugging.

### 8. Modular and Separate Workflows
- Separate build, dev, and prod jobs for clarity and security.
- Use `needs:` to enforce job dependencies (e.g., prod deploy waits for CI to pass).

---

## Summary
A robust CI/CD pipeline with clear build, dev, and prod stages ensures the Text2SQL Agent application is always tested, reliable, and can be deployed to Azure environments with confidence, supporting rapid iteration and high code quality.
