# Authentication Guide

This guide provides detailed setup instructions for authenticating the OSDU MCP Server with your OSDU platform instance across different cloud providers.

## Overview

The OSDU MCP Server supports **multi-cloud authentication** with automatic provider detection. The server automatically detects your authentication provider and uses the appropriate credential chain without requiring explicit configuration.

### Authentication Priority

The server automatically detects your authentication provider in this priority order:

1. **Manual Token** (highest priority) - `OSDU_MCP_USER_TOKEN`
2. **Azure** - `AZURE_CLIENT_ID` or `AZURE_TENANT_ID`
3. **AWS** (explicit) - `AWS_ACCESS_KEY_ID` or `AWS_PROFILE`
4. **GCP** (explicit) - `GOOGLE_APPLICATION_CREDENTIALS`
5. **AWS** (auto-discovery) - IAM roles, SSO
6. **GCP** (auto-discovery) - gcloud, metadata service

This priority system ensures zero-configuration for most scenarios while allowing explicit control when needed.

## Azure Authentication

Azure authentication uses `DefaultAzureCredential` which automatically tries multiple authentication methods in a predefined order.

### Method 1: Azure CLI (Development)

**Best for:** Local development on developer workstations

**Setup:**
1. Install [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli)
2. Run `az login` to authenticate

**Environment Variables:**
```bash
export OSDU_MCP_SERVER_URL="https://your-osdu.com"
export OSDU_MCP_SERVER_DATA_PARTITION="opendes"
export AZURE_CLIENT_ID="your-osdu-app-id"
export AZURE_TENANT_ID="your-tenant-id"
# No AZURE_CLIENT_SECRET needed - uses your az login credentials
```

**Example Installation:**
```bash
az login
mcp add osdu-mcp-server -- uvx osdu-mcp-server \
  -e OSDU_MCP_SERVER_URL=https://your-osdu.com \
  -e OSDU_MCP_SERVER_DATA_PARTITION=opendes \
  -e AZURE_CLIENT_ID=your-osdu-app-id \
  -e AZURE_TENANT_ID=your-tenant-id
```

**Authorization Setup Required:**

For Azure CLI authentication, you must authorize the Azure CLI application to access your OSDU app:

1. Navigate to your OSDU application in **Azure Portal** → **App registrations**
2. Go to **Expose an API** → **Authorized client applications**
3. Click **Add a client application**
4. Enter the Azure CLI client ID: `04b07795-8ddb-461a-bbee-02f9e1bf7b46`
5. Select the `user_impersonation` scope
6. Click **Add**

**Verify Authentication:**
```bash
az account get-access-token --resource YOUR_AZURE_CLIENT_ID
```

### Method 2: Service Principal (Production)

**Best for:** CI/CD pipelines, automated processes, production deployments

**Setup:**
1. Create a service principal:
   ```bash
   az ad sp create-for-rbac --name osdu-mcp-server-sp
   ```
2. Note the `appId` (client ID), `password` (client secret), and `tenant`

**Environment Variables:**
```bash
export OSDU_MCP_SERVER_URL="https://your-osdu.com"
export OSDU_MCP_SERVER_DATA_PARTITION="opendes"
export AZURE_CLIENT_ID="service-principal-app-id"
export AZURE_CLIENT_SECRET="service-principal-secret"
export AZURE_TENANT_ID="your-tenant-id"
```

**Example Installation:**
```bash
mcp add osdu-mcp-server -- uvx osdu-mcp-server \
  -e OSDU_MCP_SERVER_URL=https://your-osdu.com \
  -e OSDU_MCP_SERVER_DATA_PARTITION=opendes \
  -e AZURE_CLIENT_ID=your-service-principal-id \
  -e AZURE_CLIENT_SECRET=your-service-principal-secret \
  -e AZURE_TENANT_ID=your-tenant-id
```

**Authorization Setup:**

If using an external service principal (not the OSDU app's own service principal):

1. Navigate to your OSDU application in **Azure Portal** → **App registrations**
2. Go to **Expose an API** → **Authorized client applications**
3. Click **Add a client application**
4. Enter your external service principal's client ID
5. Select the `user_impersonation` scope
6. Click **Add**

**Note:** If the service principal IS the OSDU application itself, no additional authorization is needed.

### Method 3: Managed Identity (Azure Hosting)

**Best for:** Applications running in Azure (VM, App Service, Container Apps, AKS)

**Setup:**
1. Enable managed identity on your Azure resource
2. Grant the managed identity access to your OSDU platform

**Environment Variables:**
```bash
export OSDU_MCP_SERVER_URL="https://your-osdu.com"
export OSDU_MCP_SERVER_DATA_PARTITION="opendes"
export AZURE_CLIENT_ID="your-osdu-app-id"
export AZURE_TENANT_ID="your-tenant-id"
# No credentials needed - automatically discovered from Azure
```

**Example Configuration:**
```json
{
  "mcpServers": {
    "osdu-mcp-server": {
      "command": "uvx",
      "args": ["osdu-mcp-server"],
      "env": {
        "OSDU_MCP_SERVER_URL": "https://your-osdu.com",
        "OSDU_MCP_SERVER_DATA_PARTITION": "opendes",
        "AZURE_CLIENT_ID": "your-osdu-app-id",
        "AZURE_TENANT_ID": "your-tenant-id"
      }
    }
  }
}
```

### OAuth Scope Configuration

By default, the server uses `{AZURE_CLIENT_ID}/.default` as the OAuth scope. For v1.0 token environments, you may need to customize the scope:

```bash
export OSDU_MCP_AUTH_SCOPE="api://your-custom-scope/.default"
```

### Common Azure Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| "Application not found" | Azure CLI app doesn't exist in tenant | Use service principal instead |
| "Invalid resource" | Client hasn't been authorized | Follow authorization setup above |
| "Authentication failed" | Wrong client ID | Verify client ID matches OSDU application |
| "Token audience mismatch" | Wrong OAuth scope | Set `OSDU_MCP_AUTH_SCOPE` environment variable |

## AWS Authentication

AWS authentication uses boto3's credential chain which automatically tries multiple authentication methods.

### Method 1: AWS SSO (Development)

**Best for:** Local development with AWS SSO configured

**Setup:**
1. Configure AWS SSO: `aws configure sso`
2. Log in: `aws sso login --profile your-profile`

**Environment Variables:**
```bash
export OSDU_MCP_SERVER_URL="https://your-osdu.com"
export OSDU_MCP_SERVER_DATA_PARTITION="opendes"
export AWS_PROFILE="your-sso-profile"
```

**Example Installation:**
```bash
aws sso login --profile dev-profile
mcp add osdu-mcp-server -- uvx osdu-mcp-server \
  -e OSDU_MCP_SERVER_URL=https://your-osdu.com \
  -e OSDU_MCP_SERVER_DATA_PARTITION=opendes \
  -e AWS_PROFILE=dev-profile
```

### Method 2: AWS Access Keys (Production)

**Best for:** CI/CD pipelines, automated processes

**Setup:**
1. Create an IAM user or obtain access keys
2. Grant necessary permissions for OSDU access

**Environment Variables:**
```bash
export OSDU_MCP_SERVER_URL="https://your-osdu.com"
export OSDU_MCP_SERVER_DATA_PARTITION="opendes"
export AWS_ACCESS_KEY_ID="AKIAIOSFODNN7EXAMPLE"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
export AWS_REGION="us-east-1"
```

**Example Installation:**
```bash
mcp add osdu-mcp-server -- uvx osdu-mcp-server \
  -e OSDU_MCP_SERVER_URL=https://your-osdu.com \
  -e OSDU_MCP_SERVER_DATA_PARTITION=opendes \
  -e AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE \
  -e AWS_SECRET_ACCESS_KEY=your-secret-key \
  -e AWS_REGION=us-east-1
```

**Security Note:** Never commit access keys to version control. Use environment variables or AWS Secrets Manager.

### Method 3: IAM Roles (AWS Hosting)

**Best for:** Applications running in AWS (EC2, ECS/Fargate, Lambda)

**Setup:**
1. Create an IAM role with necessary OSDU permissions
2. Attach the role to your compute resource

**Environment Variables:**
```bash
export OSDU_MCP_SERVER_URL="https://your-osdu.com"
export OSDU_MCP_SERVER_DATA_PARTITION="opendes"
export AWS_REGION="us-east-1"
# No credentials needed - automatically discovered from IAM role
```

**Example Configuration:**
```json
{
  "mcpServers": {
    "osdu-mcp-server": {
      "command": "uvx",
      "args": ["osdu-mcp-server"],
      "env": {
        "OSDU_MCP_SERVER_URL": "https://your-osdu.com",
        "OSDU_MCP_SERVER_DATA_PARTITION": "opendes",
        "AWS_REGION": "us-east-1"
      }
    }
  }
}
```

### Common AWS Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| "Invalid credentials" | Wrong access keys or expired SSO session | Verify keys or re-run `aws sso login` |
| "Access denied" | IAM permissions insufficient | Grant necessary permissions in IAM policy |
| "Region not specified" | Missing AWS_REGION | Set `AWS_REGION` environment variable |
| "Token expired" | SSO session expired | Re-authenticate with `aws sso login` |

## GCP Authentication

GCP authentication uses Application Default Credentials (ADC) which automatically discovers credentials from multiple sources.

### Method 1: gcloud CLI (Development)

**Best for:** Local development with gcloud installed

**Setup:**
1. Install [gcloud CLI](https://cloud.google.com/sdk/docs/install)
2. Run `gcloud auth application-default login`

**Environment Variables:**
```bash
export OSDU_MCP_SERVER_URL="https://your-osdu.com"
export OSDU_MCP_SERVER_DATA_PARTITION="opendes"
# No additional credentials needed
```

**Example Installation:**
```bash
gcloud auth application-default login
mcp add osdu-mcp-server -- uvx osdu-mcp-server \
  -e OSDU_MCP_SERVER_URL=https://your-osdu.com \
  -e OSDU_MCP_SERVER_DATA_PARTITION=opendes
```

### Method 2: Service Account Key (Production)

**Best for:** CI/CD pipelines, automated processes

**Setup:**
1. Create a service account in Google Cloud Console
2. Grant necessary permissions for OSDU access
3. Create and download a JSON key file

**Environment Variables:**
```bash
export OSDU_MCP_SERVER_URL="https://your-osdu.com"
export OSDU_MCP_SERVER_DATA_PARTITION="opendes"
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account.json"
```

**Example Installation:**
```bash
mcp add osdu-mcp-server -- uvx osdu-mcp-server \
  -e OSDU_MCP_SERVER_URL=https://your-osdu.com \
  -e OSDU_MCP_SERVER_DATA_PARTITION=opendes \
  -e GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
```

**Security Note:** Protect service account keys like passwords. Consider using Workload Identity instead.

### Method 3: Workload Identity (GKE)

**Best for:** Applications running in Google Kubernetes Engine (GKE)

**Setup:**
1. Configure Workload Identity on your GKE cluster
2. Create a Kubernetes service account
3. Bind it to a GCP service account with OSDU permissions

**Environment Variables:**
```bash
export OSDU_MCP_SERVER_URL="https://your-osdu.com"
export OSDU_MCP_SERVER_DATA_PARTITION="opendes"
# No credentials needed - automatically discovered from Workload Identity
```

**Example Configuration:**
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: osdu-mcp-server
spec:
  serviceAccountName: osdu-mcp-sa  # Bound to GCP service account
  containers:
  - name: mcp-server
    image: your-registry/osdu-mcp-server
    env:
    - name: OSDU_MCP_SERVER_URL
      value: "https://your-osdu.com"
    - name: OSDU_MCP_SERVER_DATA_PARTITION
      value: "opendes"
```

### Common GCP Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| "Could not load credentials" | No authentication configured | Run `gcloud auth application-default login` |
| "Permission denied" | Service account lacks permissions | Grant necessary roles in IAM |
| "Invalid key file" | Corrupted or wrong JSON key | Re-download service account key |
| "ADC not found" | No default credentials set | Set `GOOGLE_APPLICATION_CREDENTIALS` |

## Manual OAuth Token

For custom OAuth providers, testing, or unsupported cloud platforms, you can provide a bearer token directly.

### Setup

**Use Case:** Custom OAuth providers, testing, direct token control

**Environment Variables:**
```bash
export OSDU_MCP_SERVER_URL="https://your-osdu.com"
export OSDU_MCP_SERVER_DATA_PARTITION="opendes"
export OSDU_MCP_USER_TOKEN="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**Example Installation:**
```bash
# Obtain token from your OAuth provider
TOKEN=$(your-oauth-command)

mcp add osdu-mcp-server -- uvx osdu-mcp-server \
  -e OSDU_MCP_SERVER_URL=https://your-osdu.com \
  -e OSDU_MCP_SERVER_DATA_PARTITION=opendes \
  -e OSDU_MCP_USER_TOKEN=$TOKEN
```

### Token Requirements

- **Format:** Valid JWT (header.payload.signature)
- **Expiration:** Must not be expired
- **Warning:** Server warns if token expires within 5 minutes
- **Refresh:** Must be manually refreshed when expired

### Security Notes

- ✅ Tokens are validated for format and expiration
- ✅ Tokens are never logged
- ✅ This method takes highest priority (overrides all auto-discovery)
- ⚠️ Tokens must be refreshed manually when they expire
- ⚠️ Store tokens securely, never commit to version control

## Testing Authentication

### Quick Health Check

After configuring authentication, verify it works:

```bash
# Using the MCP server directly (if installed locally)
# Or through your MCP client:
# "Check the health of my OSDU platform"
```

The health check tool will:
1. Validate your authentication credentials
2. Test connectivity to OSDU services
3. Report any authentication issues

### Troubleshooting

#### Authentication Failing

1. **Check environment variables are set:**
   ```bash
   env | grep OSDU_MCP
   env | grep AZURE_   # or AWS_ or GOOGLE_
   ```

2. **Verify credentials work outside MCP:**
   ```bash
   # Azure
   az account get-access-token --resource YOUR_AZURE_CLIENT_ID

   # AWS
   aws sts get-caller-identity --profile your-profile

   # GCP
   gcloud auth application-default print-access-token
   ```

3. **Enable debug logging:**
   ```bash
   export OSDU_MCP_LOGGING_ENABLED="true"
   export OSDU_MCP_LOGGING_LEVEL="DEBUG"
   ```

#### Token Issues

| Symptom | Likely Cause | Solution |
|---------|--------------|----------|
| "Token expired" | Token past expiration | Refresh authentication (re-run login command) |
| "Invalid audience" | Wrong OAuth scope | Set `OSDU_MCP_AUTH_SCOPE` (Azure only) |
| "Unauthorized (401)" | Wrong credentials | Verify client ID and credentials |
| "Forbidden (403)" | Insufficient permissions | Grant necessary roles/permissions |

## Environment-Specific Recommendations

### Local Development
- **Azure:** Use `az login` (Method 1)
- **AWS:** Use AWS SSO (Method 1)
- **GCP:** Use `gcloud auth` (Method 1)

### CI/CD Pipelines
- **Azure:** Use Service Principal (Method 2) with secrets
- **AWS:** Use Access Keys (Method 2) or IAM roles in CI environment
- **GCP:** Use Service Account Key (Method 2)

### Production Hosting
- **Azure:** Use Managed Identity (Method 3)
- **AWS:** Use IAM Roles (Method 3)
- **GCP:** Use Workload Identity (Method 3)

### Testing/Custom
- **All platforms:** Use Manual OAuth Token

## Security Best Practices

1. **Never commit credentials to version control**
   - Use environment variables
   - Use secret management systems
   - Add credential files to `.gitignore`

2. **Use least-privilege access**
   - Grant only necessary permissions
   - Use separate credentials for dev/prod
   - Regularly rotate credentials

3. **Prefer temporary credentials**
   - Use CLI login for development
   - Use managed identities in production
   - Avoid long-lived access keys

4. **Monitor authentication**
   - Enable audit logging
   - Review access logs regularly
   - Set up alerts for failed authentication

5. **Rotate credentials regularly**
   - Service principal secrets: Every 90 days
   - Access keys: Every 90 days
   - Service account keys: Every 180 days

## Additional Resources

- **[Architecture Overview](project-architect.md)** - System design and auth architecture
- **[ADR-029: Multi-Cloud Authentication](adr/029-multi-cloud-authentication.md)** - Authentication design decisions
- **[ADR-002: Authentication Strategy](adr/002-authentication-strategy.md)** - Azure authentication details
- **[Contributing Guide](../CONTRIBUTING.md)** - Development workflow

## Support

If you encounter authentication issues not covered in this guide:

1. Check the [Architecture Decisions](adr/README.md) for implementation details
2. Review the [health_check tool](project-architect.md#health-check) documentation
3. Enable debug logging to diagnose issues
4. Open an issue on [GitHub](https://github.com/danielscholl/osdu-mcp-server/issues)
