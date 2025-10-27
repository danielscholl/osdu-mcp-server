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

- **Natural Language Interface** - Complex API calls and Elasticsearch queries through conversation
- **Multi-Cloud Authentication** - Azure, AWS, and GCP with zero-config credential discovery
- **31 MCP Tools** - Complete OSDU API coverage (storage, search, schema, legal, partition)
- **Template-Driven** - Pre-built templates eliminate format-guessing errors
- **Safety Controls** - Write/delete protection, confirmation requirements, audit logging
- **MCP Resources & Prompts** - Guided workflows and interactive examples

## Quick Start

### Installation

```bash
# Using Claude Code CLI (recommended)
mcp add osdu-mcp-server -- uvx osdu-mcp-server \
  -e OSDU_MCP_SERVER_URL=https://your-osdu.com \
  -e OSDU_MCP_SERVER_DATA_PARTITION=opendes

# Or add to your MCP configuration
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

**Authentication** is auto-discovered from your environment (Azure CLI, AWS profiles, GCP gcloud).

See [Getting Started Guide](docs/getting-started.md) for detailed setup and configuration.

### Try It

> "Check the health of my OSDU platform"

> "List all schemas available in the system"

> "Find wells in the North Sea region"

> "Show me the legal tag template"

## What's Included

**31 Tools** across 6 OSDU services:
- Core: `health_check`, `entitlements_mine`
- Partition: List, get, create, update, delete
- Legal: CRUD operations, search, batch retrieval
- Schema: Discovery, validation, CRUD
- Search: Query, find by ID/kind
- Storage: CRUD, versioning, batch operations

**3 Prompts** for guided workflows:
- `list_mcp_assets` - Capability overview
- `guide_search_patterns` - Search best practices
- `guide_record_lifecycle` - Complete workflows

**4 Resources** with working templates:
- Legal tag templates
- Record examples
- ACL format patterns
- Search query examples

## Configuration

### Required
- `OSDU_MCP_SERVER_URL` - Your OSDU platform URL
- `OSDU_MCP_SERVER_DATA_PARTITION` - Data partition ID

### Optional
- `OSDU_MCP_SERVER_DOMAIN` - Data domain for ACLs (default: `contoso.com`)
- `OSDU_MCP_ENABLE_WRITE_MODE` - Enable create/update (default: `false`)
- `OSDU_MCP_ENABLE_DELETE_MODE` - Enable delete/purge (default: `false`)

See [Getting Started Guide](docs/getting-started.md#configuration) for complete configuration reference.


## License

Apache License 2.0 - see [LICENSE](LICENSE) for details.

---

<div align="center">

**[Getting Started](docs/getting-started.md)** • **[Authentication](docs/authentication.md)** • **[Architecture](docs/project-architect.md)** • **[Contributing](CONTRIBUTING.md)**

</div>
