# OSDU MCP Server

[![CI](https://github.com/danielscholl/osdu-mcp-server/actions/workflows/ci.yml/badge.svg)](https://github.com/danielscholl/osdu-mcp-server/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/danielscholl/osdu-mcp-server)](https://github.com/danielscholl/osdu-mcp-server/releases)
[![Python](https://img.shields.io/badge/python-3.12%20|%203.13-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![MCP](https://img.shields.io/badge/MCP-Model%20Context%20Protocol-green)](https://modelcontextprotocol.io)

**AI-powered access to OSDU subsurface data through natural language.**

Enable AI assistants to interact with the OSDU (Open Subsurface Data Universe) platform through conversational interfaces. Search data, manage schemas, handle records, and maintain compliance—all through natural language.

## Why OSDU MCP Server?

Transform complex OSDU API workflows into simple conversations:

**Before:**
```bash
curl -X POST https://osdu.com/api/search/v2/query \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"kind":"osdu:wks:master-data--Well:*"}'
# ... parse JSON, check schemas, format records, handle ACLs ...
```

**After:**
```
You: "Find all wells in the North Sea and show their schemas"
AI: ✅ Found 247 wells
    📋 Retrieved schema requirements
    🎯 Ready to work with the data
```

## Key Features

| Feature | Description |
|---------|-------------|
| **Natural Language** | Complex API calls and Elasticsearch queries through conversation |
| **Multi-Cloud Auth** | Azure, AWS, and GCP with zero-config credential discovery |
| **31 MCP Tools** | Complete OSDU API coverage (storage, search, schema, legal, partition) |
| **Template-Driven** | Pre-built templates eliminate format-guessing errors |
| **Safety Controls** | Write/delete protection, confirmation requirements, audit logging |
| **Resources & Prompts** | Guided workflows and interactive examples |

## Quick Start

### Setup

[![Install with UV in VS Code](https://img.shields.io/badge/VS_Code-UV-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect?url=vscode:mcp/install?%7B%22name%22%3A%22osdu-mcp-server%22%2C%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22osdu-mcp-server%22%5D%2C%22env%22%3A%7B%22OSDU_MCP_SERVER_URL%22%3A%22%24%7Binput%3Aosdu_url%7D%22%2C%22OSDU_MCP_SERVER_DATA_PARTITION%22%3A%22%24%7Binput%3Adata_partition%7D%22%7D%2C%22inputs%22%3A%5B%7B%22id%22%3A%22osdu_url%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22OSDU%20Server%20URL%22%7D%2C%7B%22id%22%3A%22data_partition%22%2C%22type%22%3A%22promptString%22%2C%22description%22%3A%22Data%20Partition%20ID%22%7D%5D%7D)

```bash
mcp add osdu-mcp-server -- uvx osdu-mcp-server \
  -e OSDU_MCP_SERVER_URL=https://your-osdu.com \
  -e OSDU_MCP_SERVER_DATA_PARTITION=opendes \
  -e AZURE_CLIENT_ID=your-client-id \
  -e AZURE_TENANT_ID=your-tenant-id
```

Or add manually to your MCP configuration:

```json
{
  "mcpServers": {
    "osdu-mcp-server": {
      "command": "uvx",
      "args": ["osdu-mcp-server"],
      "env": {
        "OSDU_MCP_SERVER_URL": "https://your-osdu.com",
        "OSDU_MCP_SERVER_DATA_PARTITION": "opendes",
        "AZURE_CLIENT_ID": "your-client-id",
        "AZURE_TENANT_ID": "your-tenant-id"
      }
    }
  }
}
```

**Note:** Authentication credentials (Azure/AWS/GCP) are auto-discovered from your environment. See [Getting Started](docs/getting-started.md) for all auth methods.

### Try It

> "Check the health of my OSDU platform"

> "List all schemas available in the system"

> "Find wells in the North Sea region"

> "Show me the legal tag template"

## What's Included

**31 Tools** across 6 OSDU services:
- **Core**: `health_check`, `entitlements_mine`
- **Partition**: `list`, `get`, `create`, `update`, `delete`
- **Legal**: `list`, `get`, `search`, `batch_retrieve`, `create`, `update`, `delete`, `get_properties`
- **Schema**: `list`, `get`, `search`, `create`, `update`
- **Search**: `query`, `by_id`, `by_kind`
- **Storage**: `get_record`, `create_update_records`, `delete_record`, `purge_record`, `fetch_records`, `list_versions`, `get_version`, `query_by_kind`

**3 Prompts** for guided workflows:
- `list_mcp_assets` - Capability overview
- `guide_search_patterns` - Search best practices
- `guide_record_lifecycle` - Complete workflows

**4 Resources** with working templates:
- `legal-tag-template` - Ready-to-use legal tag structure
- `processing-parameter-record` - Sample OSDU record
- `acl-format-examples` - ACL patterns for different deployments
- `search-query-patterns` - Common Elasticsearch queries

## Configuration

### Required
- `OSDU_MCP_SERVER_URL` - Your OSDU platform URL
- `OSDU_MCP_SERVER_DATA_PARTITION` - Data partition ID

### Optional
- `OSDU_MCP_SERVER_DOMAIN` - Data domain for ACLs (default: `contoso.com`)
- `OSDU_MCP_ENABLE_WRITE_MODE` - Enable create/update (default: `false`)
- `OSDU_MCP_ENABLE_DELETE_MODE` - Enable delete/purge (default: `false`)


## License

Apache License 2.0 - see [LICENSE](LICENSE) for details.

---

<div align="center">

**[Getting Started](docs/getting-started.md)** • **[Authentication](docs/authentication.md)** • **[Architecture](docs/project-architect.md)** • **[Contributing](CONTRIBUTING.md)**

</div>
