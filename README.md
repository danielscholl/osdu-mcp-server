# OSDU MCP Server

[![CI](https://github.com/danielscholl/osdu-mcp-server/actions/workflows/ci.yml/badge.svg)](https://github.com/danielscholl/osdu-mcp-server/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/danielscholl/osdu-mcp-server)](https://github.com/danielscholl/osdu-mcp-server/releases)
[![Python](https://img.shields.io/badge/python-3.12%20|%203.13-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![MCP](https://img.shields.io/badge/MCP-Model%20Context%20Protocol-green)](https://modelcontextprotocol.io)

**AI-powered access to OSDU subsurface data through natural language.**

OSDU MCP Server enables AI assistants to interact with the OSDU (Open Subsurface Data Universe) platform, providing comprehensive tools for data discovery, schema management, and record operations—all through conversational interfaces.

## Why OSDU MCP Server?

**Traditional OSDU workflow:**
```bash
# Search for wells
curl -X POST https://osdu.com/api/search/v2/query -d '{"kind":"osdu:wks:master-data--Well:*"}'
# Parse JSON response manually
# Check schema requirements
# Format records correctly
# Handle ACLs and legal tags...
```

**With OSDU MCP Server:**
```
You: "Find all wells in the North Sea and show their schemas"
AI: ✅ Found 247 wells
    📋 Retrieved schema requirements
    🎯 Ready to work with the data
```

> **Key Benefits:**
> - Natural language instead of complex API calls and Elasticsearch queries
> - Multi-cloud authentication (Azure, AWS, GCP) with zero configuration
> - Template-driven workflows eliminate format-guessing errors
> - Built-in safety with write/delete protection
> - Complete audit trail for compliance requirements

## Features

| Category | Capabilities |
|----------|-------------|
| **Data Discovery** | Elasticsearch-powered search • Find records by ID or kind • Advanced filtering and aggregation • Search guidance prompts |
| **Schema Management** | List and search schemas • Retrieve schema definitions • Create and update schemas • Schema validation |
| **Data Operations** | CRUD operations on records • Version history tracking • Batch record operations • Record validation |
| **Compliance** | Legal tag management • ACL configuration • Partition administration • Entitlements checking |
| **Multi-Cloud** | Azure authentication (CLI, Service Principal, Managed Identity) • AWS (SSO, Access Keys, IAM Roles) • GCP (gcloud, Service Account, Workload Identity) • Manual OAuth tokens |
| **Safety Controls** | Write protection by default • Separate delete controls • Confirmation for destructive operations • Structured audit logging |

## Quick Start

**Prerequisites:**

- [Python 3.12+](https://www.python.org/downloads/)
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- Access to an OSDU platform instance
- Cloud credentials (Azure, AWS, or GCP)

### Setup

[![Install with UV in VS Code](https://img.shields.io/badge/VS_Code-UV-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect?url=vscode:mcp/install?%7B%22name%22%3A%22osdu-mcp-server%22%2C%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22osdu-mcp-server%22%5D%2C%22env%22%3A%7B%22OSDU_MCP_SERVER_URL%22%3A%22%24%7Binput%3Aosdu_url%7D%22%2C%22OSDU_MCP_SERVER_DATA_PARTITION%22%3A%22%24%7Binput%3Adata_partition%7D%22%7D%2C%22inputs%22%3A%5B%7B%22id%22%3A%22osdu_url%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22OSDU%20Server%20URL%22%7D%2C%7B%22id%22%3A%22data_partition%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Data%20Partition%20ID%22%7D%5D%7D)

#### Option 1: Using Claude Code CLI

```bash
# Azure (with az login)
az login
mcp add osdu-mcp-server -- uvx osdu-mcp-server \
  -e OSDU_MCP_SERVER_URL=https://your-osdu.com \
  -e OSDU_MCP_SERVER_DATA_PARTITION=opendes \
  -e AZURE_CLIENT_ID=your-client-id \
  -e AZURE_TENANT_ID=your-tenant-id

# AWS (with SSO)
aws sso login --profile dev
mcp add osdu-mcp-server -- uvx osdu-mcp-server \
  -e OSDU_MCP_SERVER_URL=https://your-osdu.com \
  -e OSDU_MCP_SERVER_DATA_PARTITION=opendes \
  -e AWS_PROFILE=dev

# GCP (with gcloud)
gcloud auth application-default login
mcp add osdu-mcp-server -- uvx osdu-mcp-server \
  -e OSDU_MCP_SERVER_URL=https://your-osdu.com \
  -e OSDU_MCP_SERVER_DATA_PARTITION=opendes
```

#### Option 2: Manual Configuration

Add to your MCP configuration (`.mcp.json` or `mcp_config.json`):

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

**Note:** Authentication credentials are discovered automatically from your environment (Azure CLI, AWS profiles, GCP gcloud, etc.).

### Try It

> "Check the health of my OSDU platform"

> "List all schemas available in the system"

> "Search for wells in the North Sea region"

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

### Authentication

The server automatically detects your cloud provider and uses native credential chains:

- **Azure**: `az login` or Service Principal
- **AWS**: SSO, profiles, IAM roles, or access keys
- **GCP**: `gcloud` auth, service accounts, or Workload Identity
- **Manual**: `OSDU_MCP_USER_TOKEN` for custom OAuth providers

For detailed authentication setup, see [Authentication Guide](docs/authentication.md).

### Data Domains

OSDU deployments use different data domains for ACL formatting. Set the correct domain to avoid validation errors:

| Deployment | Domain |
|------------|--------|
| Standard OSDU | `contoso.com` |
| Microsoft Energy Data Services | `dataservices.energy` |
| Microsoft Internal | `msft-osdu-test.org` |

Use `OSDU_MCP_SERVER_DOMAIN` environment variable or check your current domain with the `entitlements_mine` tool.

## Available Tools

### Core Operations

| Tool | Description |
|------|-------------|
| `health_check` | Check platform connectivity and service health |
| `entitlements_mine` | Get groups for the current authenticated user |

### Partition Management

| Tool | Description |
|------|-------------|
| `partition_list` | List all accessible partitions |
| `partition_get` | Get partition configuration |
| `partition_create` | Create new partition (write-protected) |
| `partition_update` | Update partition properties (write-protected) |
| `partition_delete` | Delete partition (delete-protected) |

### Legal & Compliance

| Tool | Description |
|------|-------------|
| `legaltag_list` | List all legal tags |
| `legaltag_get` | Get specific legal tag details |
| `legaltag_search` | Search legal tags with filters |
| `legaltag_batch_retrieve` | Retrieve multiple tags at once |
| `legaltag_get_properties` | Get allowed property values |
| `legaltag_create` | Create new legal tag (write-protected) |
| `legaltag_update` | Update legal tag (write-protected) |
| `legaltag_delete` | Delete legal tag (delete-protected) |

### Schema Operations

| Tool | Description |
|------|-------------|
| `schema_list` | List available schemas with filtering |
| `schema_get` | Retrieve complete schema definition |
| `schema_search` | Advanced schema discovery with text search |
| `schema_create` | Create new schema (write-protected) |
| `schema_update` | Update existing schema (write-protected) |

### Search & Discovery

| Tool | Description |
|------|-------------|
| `search_query` | Execute Elasticsearch queries |
| `search_by_id` | Find specific records by ID |
| `search_by_kind` | Find all records of a specific type |

### Data Storage

| Tool | Description |
|------|-------------|
| `storage_get_record` | Get latest version of a record |
| `storage_get_record_version` | Get specific version of a record |
| `storage_list_record_versions` | List all versions of a record |
| `storage_query_records_by_kind` | Get record IDs by kind |
| `storage_fetch_records` | Retrieve multiple records at once |
| `storage_create_update_records` | Create or update records (write-protected) |
| `storage_delete_record` | Logically delete a record (delete-protected) |
| `storage_purge_record` | Permanently delete a record (delete-protected) |

## Available Prompts

| Prompt | Description |
|--------|-------------|
| `list_mcp_assets` | Comprehensive overview of all capabilities with examples |
| `guide_search_patterns` | Elasticsearch query patterns and best practices |
| `guide_record_lifecycle` | Complete workflow from legal setup to data cleanup |

## Available Resources

Working templates and reference examples to eliminate format-guessing errors:

| Resource | Description |
|----------|-------------|
| `templates://legal-tag-template` | Ready-to-use legal tag template |
| `templates://processing-parameter-record` | Sample OSDU record template |
| `references://acl-format-examples` | ACL format examples for different deployments |
| `references://search-query-patterns` | Common Elasticsearch query patterns |

## Safety & Compliance

- **Write Protection**: All create/update operations disabled by default
- **Delete Protection**: Separate control for destructive operations
- **Confirmation Required**: Purge operations require explicit confirmation
- **Audit Logging**: Structured JSON logs with operation tracing
- **Sensitive Data**: Configurable handling for credentials and secrets

## Development

Built with AI-driven development practices using Claude Code and GitHub Copilot. See our [Contributing Guide](CONTRIBUTING.md) for details on the development workflow.

```bash
# Local development setup
uv sync
uv pip install -e '.[dev]'

# Run tests
pytest

# Code quality
black .
ruff check .
mypy src/
```

## Documentation

- **[Architecture Overview](docs/project-architect.md)** - System design and patterns
- **[Authentication Guide](docs/authentication.md)** - Detailed auth setup (to be created)
- **[Architecture Decisions](docs/adr/README.md)** - All ADRs (29 decisions documented)
- **[Contributing Guide](CONTRIBUTING.md)** - AI-driven development workflow
- **[Case Study](case-study.md)** - Insights on building with AI agents

## License

This project is licensed under the Apache License 2.0 - see [LICENSE](LICENSE) for details.

---

<div align="center">

**[Getting Started](docs/project-brief.md)** • **[Architecture](docs/project-architect.md)** • **[Contributing](CONTRIBUTING.md)**

</div>
