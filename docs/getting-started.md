# Getting Started with OSDU MCP Server

This comprehensive guide will help you install, configure, and use the OSDU MCP Server to interact with OSDU platforms through AI assistants.

## Table of Contents

- [Installation](#installation)
- [Authentication](#authentication)
- [Configuration](#configuration)
- [Quick Start Examples](#quick-start-examples)
- [Available Capabilities](#available-capabilities)
- [Common Workflows](#common-workflows)
- [Troubleshooting](#troubleshooting)

## Installation

### Prerequisites

- **Python 3.12 or 3.13**
- **[uv](https://docs.astral.sh/uv/)** package manager
- **Access to an OSDU platform instance**
- **Cloud credentials** (Azure, AWS, or GCP)

### Installation Methods

#### Method 1: Using Claude Code CLI (Recommended)

```bash
mcp add osdu-mcp-server -- uvx osdu-mcp-server \
  -e OSDU_MCP_SERVER_URL=https://your-osdu.com \
  -e OSDU_MCP_SERVER_DATA_PARTITION=opendes
```

#### Method 2: Using uvx Directly

```bash
uvx osdu-mcp-server
```

Then configure environment variables in your shell or MCP client configuration.

#### Method 3: Manual MCP Configuration

Add to your MCP configuration file (`.mcp.json` or `mcp_config.json`):

```json
{
  "mcpServers": {
    "osdu-mcp-server": {
      "command": "uvx",
      "args": ["osdu-mcp-server"],
      "env": {
        "OSDU_MCP_SERVER_URL": "https://your-osdu.com",
        "OSDU_MCP_SERVER_DATA_PARTITION": "opendes"
      }
    }
  }
}
```

#### Method 4: Install from PyPI

```bash
pip install osdu-mcp-server
# or
uv pip install osdu-mcp-server
```

### VS Code Quick Install

[![Install with UV in VS Code](https://img.shields.io/badge/VS_Code-UV-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect?url=vscode:mcp/install?%7B%22name%22%3A%22osdu-mcp-server%22%2C%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22osdu-mcp-server%22%5D%2C%22env%22%3A%7B%22OSDU_MCP_SERVER_URL%22%3A%22%24%7Binput%3Aosdu_url%7D%22%2C%22OSDU_MCP_SERVER_DATA_PARTITION%22%3A%22%24%7Binput%3Adata_partition%7D%22%7D%2C%22inputs%22%3A%5B%7B%22id%22%3A%22osdu_url%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22OSDU%20Server%20URL%22%7D%2C%7B%22id%22%3A%22data_partition%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Data%20Partition%20ID%22%7D%5D%7D)

## Authentication

The OSDU MCP Server supports **multi-cloud authentication** with automatic provider detection.

### Authentication Priority

The server automatically detects your authentication provider in this order:

1. **Manual Token** (highest priority) - `OSDU_MCP_USER_TOKEN`
2. **Azure** - `AZURE_CLIENT_ID` or `AZURE_TENANT_ID`
3. **AWS** (explicit) - `AWS_ACCESS_KEY_ID` or `AWS_PROFILE`
4. **GCP** (explicit) - `GOOGLE_APPLICATION_CREDENTIALS`
5. **AWS** (auto-discovery) - IAM roles, SSO
6. **GCP** (auto-discovery) - gcloud, metadata service

### Azure Authentication

#### Azure CLI (Development)

**Best for:** Local development

```bash
# Login with Azure CLI
az login

# Configure MCP server
mcp add osdu-mcp-server -- uvx osdu-mcp-server \
  -e OSDU_MCP_SERVER_URL=https://your-osdu.com \
  -e OSDU_MCP_SERVER_DATA_PARTITION=opendes \
  -e AZURE_CLIENT_ID=your-osdu-app-id \
  -e AZURE_TENANT_ID=your-tenant-id
```

**Required Environment Variables:**
- `OSDU_MCP_SERVER_URL` - Your OSDU platform URL
- `OSDU_MCP_SERVER_DATA_PARTITION` - Data partition ID
- `AZURE_CLIENT_ID` - Your OSDU application ID
- `AZURE_TENANT_ID` - Your Azure tenant ID

**Authorization Required:** You must authorize the Azure CLI to access your OSDU app:
1. Go to Azure Portal → App registrations → Your OSDU app
2. Select **Expose an API** → **Authorized client applications**
3. Add client ID: `04b07795-8ddb-461a-bbee-02f9e1bf7b46` (Azure CLI)
4. Select `user_impersonation` scope

#### Service Principal (Production)

**Best for:** CI/CD, automated processes

```bash
mcp add osdu-mcp-server -- uvx osdu-mcp-server \
  -e OSDU_MCP_SERVER_URL=https://your-osdu.com \
  -e OSDU_MCP_SERVER_DATA_PARTITION=opendes \
  -e AZURE_CLIENT_ID=your-service-principal-id \
  -e AZURE_CLIENT_SECRET=your-service-principal-secret \
  -e AZURE_TENANT_ID=your-tenant-id
```

#### Managed Identity (Azure Hosting)

**Best for:** Azure VM, App Service, Container Apps, AKS

No credentials needed - automatically discovered from Azure environment.

```bash
# Just set OSDU config
export OSDU_MCP_SERVER_URL=https://your-osdu.com
export OSDU_MCP_SERVER_DATA_PARTITION=opendes
export AZURE_CLIENT_ID=your-osdu-app-id
export AZURE_TENANT_ID=your-tenant-id
```

### AWS Authentication

#### AWS SSO (Development)

```bash
aws sso login --profile dev

mcp add osdu-mcp-server -- uvx osdu-mcp-server \
  -e OSDU_MCP_SERVER_URL=https://your-osdu.com \
  -e OSDU_MCP_SERVER_DATA_PARTITION=opendes \
  -e AWS_PROFILE=dev
```

#### Access Keys (Production)

```bash
mcp add osdu-mcp-server -- uvx osdu-mcp-server \
  -e OSDU_MCP_SERVER_URL=https://your-osdu.com \
  -e OSDU_MCP_SERVER_DATA_PARTITION=opendes \
  -e AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE \
  -e AWS_SECRET_ACCESS_KEY=your-secret-key \
  -e AWS_REGION=us-east-1
```

#### IAM Roles (EC2/ECS/Lambda)

No credentials needed - automatically discovered from IAM role.

### GCP Authentication

#### gcloud CLI (Development)

```bash
gcloud auth application-default login

mcp add osdu-mcp-server -- uvx osdu-mcp-server \
  -e OSDU_MCP_SERVER_URL=https://your-osdu.com \
  -e OSDU_MCP_SERVER_DATA_PARTITION=opendes
```

#### Service Account (Production)

```bash
mcp add osdu-mcp-server -- uvx osdu-mcp-server \
  -e OSDU_MCP_SERVER_URL=https://your-osdu.com \
  -e OSDU_MCP_SERVER_DATA_PARTITION=opendes \
  -e GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
```

#### Workload Identity (GKE)

No credentials needed - automatically discovered from Workload Identity.

### Manual OAuth Token

For custom OAuth providers or manual token management:

```bash
export OSDU_MCP_USER_TOKEN="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**Token Requirements:**
- Valid JWT format
- Not expired
- Server warns if expires within 5 minutes

For detailed authentication troubleshooting, see [Authentication Guide](authentication.md).

## Configuration

### Required Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `OSDU_MCP_SERVER_URL` | OSDU platform URL | `https://your-osdu.com` |
| `OSDU_MCP_SERVER_DATA_PARTITION` | Data partition ID | `opendes` |

### Optional Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `OSDU_MCP_SERVER_DOMAIN` | Data domain for ACLs | `contoso.com` |
| `OSDU_MCP_ENABLE_WRITE_MODE` | Enable create/update operations | `false` |
| `OSDU_MCP_ENABLE_DELETE_MODE` | Enable delete/purge operations | `false` |
| `OSDU_MCP_LOGGING_ENABLED` | Enable structured logging | `false` |
| `OSDU_MCP_LOGGING_LEVEL` | Logging level | `INFO` |

### Data Domains

OSDU deployments use different data domains for ACL formatting:

| Deployment Type | Domain | Example ACL |
|----------------|--------|-------------|
| Standard OSDU | `contoso.com` | `data.default.viewers@contoso.com` |
| Microsoft Energy Data Services | `dataservices.energy` | `data.default.viewers@dataservices.energy` |
| Microsoft Internal | `msft-osdu-test.org` | `data.default.viewers@msft-osdu-test.org` |

**How to find your domain:**
1. Use the `entitlements_mine` tool to see your group format
2. Ask your OSDU administrator
3. Check the domain in existing ACLs

### Write Protection

**Safety by default** - all write operations are disabled unless explicitly enabled:

```json
{
  "env": {
    "OSDU_MCP_ENABLE_WRITE_MODE": "true",    // Enable create/update
    "OSDU_MCP_ENABLE_DELETE_MODE": "true"    // Enable delete/purge
  }
}
```

## Quick Start Examples

### Example 1: Check Platform Health

```
You: "Check the health of my OSDU platform"

AI: The OSDU platform is healthy:
    ✅ Authentication: valid
    ✅ Storage service: healthy
    ✅ Search service: healthy
    ✅ Legal service: healthy
```

### Example 2: Search for Data

```
You: "Find all wells in the North Sea"

AI: Found 247 wells matching "North Sea":
    - Well-123: coordinates [60.5, 2.3]
    - Well-456: coordinates [61.2, 3.1]
    ...
```

### Example 3: Get Schema Information

```
You: "What schema do I need for a well record?"

AI: For well records, use schema: osdu:wks:master-data--Well:1.0.0
    Required fields:
    - kind
    - acl
    - legal
    - data.WellName
    - data.WellID
```

### Example 4: List Available Resources

```
You: "What templates are available?"

AI: Available templates:
    📄 legal-tag-template.json - Ready-to-use legal tag
    📄 processing-parameter-record.json - Complete record example
    📚 acl-format-examples.json - ACL format reference
    📚 search-query-patterns.json - Search examples
```

## Available Capabilities

### Tools (31 total)

#### Core Operations
- `health_check` - Check platform connectivity and service health
- `entitlements_mine` - Get groups for the current authenticated user

#### Partition Management (5 tools)
- `partition_list` - List all accessible partitions
- `partition_get` - Get partition configuration
- `partition_create` - Create new partition (write-protected)
- `partition_update` - Update partition properties (write-protected)
- `partition_delete` - Delete partition (delete-protected)

#### Legal & Compliance (8 tools)
- `legaltag_list` - List all legal tags
- `legaltag_get` - Get specific legal tag details
- `legaltag_search` - Search legal tags with filters
- `legaltag_batch_retrieve` - Retrieve multiple tags at once
- `legaltag_get_properties` - Get allowed property values
- `legaltag_create` - Create new legal tag (write-protected)
- `legaltag_update` - Update legal tag (write-protected)
- `legaltag_delete` - Delete legal tag (delete-protected)

#### Schema Operations (5 tools)
- `schema_list` - List available schemas with filtering
- `schema_get` - Retrieve complete schema definition
- `schema_search` - Advanced schema discovery with text search
- `schema_create` - Create new schema (write-protected)
- `schema_update` - Update existing schema (write-protected)

#### Search & Discovery (3 tools)
- `search_query` - Execute Elasticsearch queries
- `search_by_id` - Find specific records by ID
- `search_by_kind` - Find all records of a specific type

#### Data Storage (8 tools)
- `storage_get_record` - Get latest version of a record
- `storage_get_record_version` - Get specific version of a record
- `storage_list_record_versions` - List all versions of a record
- `storage_query_records_by_kind` - Get record IDs by kind
- `storage_fetch_records` - Retrieve multiple records at once
- `storage_create_update_records` - Create or update records (write-protected)
- `storage_delete_record` - Logically delete a record (delete-protected)
- `storage_purge_record` - Permanently delete a record (delete-protected)

### Prompts (3 total)

- `list_mcp_assets` - Comprehensive overview of all capabilities with examples
- `guide_search_patterns` - Elasticsearch query patterns and best practices
- `guide_record_lifecycle` - Complete workflow from legal setup to data cleanup

### Resources (4 total)

**Templates** (working examples for direct use):
- `templates://legal-tag-template` - Ready-to-use legal tag template
- `templates://processing-parameter-record` - Sample OSDU record template

**References** (patterns and examples):
- `references://acl-format-examples` - ACL format examples for different deployments
- `references://search-query-patterns` - Common Elasticsearch query patterns

## Common Workflows

### Workflow 1: Complete Record Lifecycle

```
1. "Create a legal tag for my test data"
2. "Show me the legal tag template"
3. "Create a new well record using the template"
4. "Search for my well record"
5. "Update the well location"
6. "Delete the test record"
```

### Workflow 2: Data Discovery

```
1. "What schemas are available for seismic data?"
2. "Search for all seismic surveys in the Gulf of Mexico"
3. "Get the full details for survey XYZ-123"
4. "List all versions of this survey record"
```

### Workflow 3: Compliance Check

```
1. "List all legal tags in the system"
2. "Show me the properties of legal tag ABC"
3. "Search for all records using this legal tag"
4. "Validate that all records have proper ACLs"
```

## Safety & Compliance

### Write Protection

All write operations are **disabled by default**:

- Create/update operations require `OSDU_MCP_ENABLE_WRITE_MODE=true`
- Delete/purge operations require `OSDU_MCP_ENABLE_DELETE_MODE=true`
- Purge operations require explicit confirmation parameter

### Audit Logging

When enabled, the server provides structured JSON logs with:
- Operation type and timestamp
- User/service principal identity
- Resource IDs and operation results
- Success/failure indicators
- Security events (auth failures, permission denials)

Enable logging:
```bash
export OSDU_MCP_LOGGING_ENABLED=true
export OSDU_MCP_LOGGING_LEVEL=INFO
```

### Sensitive Data Handling

The server automatically:
- Redacts credentials from logs
- Masks API tokens in responses
- Excludes sensitive fields from audit trails

## Troubleshooting

### Common Issues

#### Authentication Failures

**Problem:** "Authentication failed"

**Solutions:**
1. Verify environment variables are set correctly
2. Check credentials work outside MCP:
   ```bash
   # Azure
   az account get-access-token --resource YOUR_CLIENT_ID

   # AWS
   aws sts get-caller-identity

   # GCP
   gcloud auth application-default print-access-token
   ```
3. Enable debug logging: `OSDU_MCP_LOGGING_LEVEL=DEBUG`

#### ACL Format Errors

**Problem:** "Invalid ACL format"

**Solutions:**
1. Check your data domain: Use `entitlements_mine` tool
2. Set correct domain: `OSDU_MCP_SERVER_DOMAIN=dataservices.energy`
3. Review `references://acl-format-examples` resource

#### Write Operations Disabled

**Problem:** "Write operations are disabled"

**Solution:** Enable write mode:
```bash
export OSDU_MCP_ENABLE_WRITE_MODE=true
```

#### Connection Errors

**Problem:** "Cannot connect to OSDU platform"

**Solutions:**
1. Verify `OSDU_MCP_SERVER_URL` is correct
2. Check network connectivity
3. Use `health_check` tool to diagnose

### Getting Help

- **Issues**: [GitHub Issues](https://github.com/danielscholl/osdu-mcp-server/issues)
- **Documentation**: [docs/](https://github.com/danielscholl/osdu-mcp-server/tree/main/docs)
- **Contributing**: [CONTRIBUTING.md](../CONTRIBUTING.md)

## Next Steps

- Review [Architecture Documentation](project-architect.md) to understand the system design
- Check [Architecture Decisions (ADRs)](adr/README.md) for design rationale
- Read [Contributing Guide](../CONTRIBUTING.md) to contribute to the project
- Explore [Authentication Guide](authentication.md) for advanced auth scenarios
