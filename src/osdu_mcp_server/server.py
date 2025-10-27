"""MCP server instance for OSDU platform integration."""

from mcp.server.fastmcp import FastMCP

from .tools.entitlements import (
    entitlements_mine,
)
from .tools.health_check import health_check
from .tools.legal import (
    legaltag_batch_retrieve,
    legaltag_create,
    legaltag_delete,
    legaltag_get,
    legaltag_get_properties,
    legaltag_list,
    legaltag_search,
    legaltag_update,
)
from .tools.partition import (
    partition_create,
    partition_delete,
    partition_get,
    partition_list,
    partition_update,
)
from .tools.schema import (
    schema_create,
    schema_get,
    schema_list,
    schema_search,
    schema_update,
)
from .tools.search import (
    search_query,
    search_by_id,
    search_by_kind,
)
from .tools.storage import (
    storage_create_update_records,
    storage_delete_record,
    storage_fetch_records,
    storage_get_record,
    storage_get_record_version,
    storage_list_record_versions,
    storage_purge_record,
    storage_query_records_by_kind,
)
from .prompts import list_mcp_assets, guide_search_patterns, guide_record_lifecycle
from .resources import get_workflow_resources

# Create FastMCP server instance
mcp = FastMCP("OSDU MCP Server")

# Register MCP resources
for resource in get_workflow_resources():
    mcp.add_resource(resource)

# Register prompts
mcp.prompt()(list_mcp_assets)  # type: ignore[arg-type]
mcp.prompt()(guide_search_patterns)  # type: ignore[arg-type]
mcp.prompt()(guide_record_lifecycle)  # type: ignore[arg-type]

# Register tools
mcp.tool()(health_check)  # type: ignore[arg-type]

# Register partition tools
mcp.tool()(partition_list)  # type: ignore[arg-type]
mcp.tool()(partition_get)  # type: ignore[arg-type]
mcp.tool()(partition_create)  # type: ignore[arg-type]
mcp.tool()(partition_update)  # type: ignore[arg-type]
mcp.tool()(partition_delete)  # type: ignore[arg-type]

# Register entitlements tools
mcp.tool()(entitlements_mine)  # type: ignore[arg-type]

# Register legal tools
mcp.tool()(legaltag_list)  # type: ignore[arg-type]
mcp.tool()(legaltag_get)  # type: ignore[arg-type]
mcp.tool()(legaltag_get_properties)  # type: ignore[arg-type]
mcp.tool()(legaltag_search)  # type: ignore[arg-type]
mcp.tool()(legaltag_batch_retrieve)  # type: ignore[arg-type]
mcp.tool()(legaltag_create)  # type: ignore[arg-type]
mcp.tool()(legaltag_update)  # type: ignore[arg-type]
mcp.tool()(legaltag_delete)  # type: ignore[arg-type]

# Register schema tools
mcp.tool()(schema_list)  # type: ignore[arg-type]
mcp.tool()(schema_get)  # type: ignore[arg-type]
mcp.tool()(schema_search)  # type: ignore[arg-type]
mcp.tool()(schema_create)  # type: ignore[arg-type]
mcp.tool()(schema_update)  # type: ignore[arg-type]

# Register search tools
mcp.tool()(search_query)  # type: ignore[arg-type]
mcp.tool()(search_by_id)  # type: ignore[arg-type]
mcp.tool()(search_by_kind)  # type: ignore[arg-type]

# Register storage tools
mcp.tool()(storage_create_update_records)  # type: ignore[arg-type]
mcp.tool()(storage_get_record)  # type: ignore[arg-type]
mcp.tool()(storage_get_record_version)  # type: ignore[arg-type]
mcp.tool()(storage_list_record_versions)  # type: ignore[arg-type]
mcp.tool()(storage_query_records_by_kind)  # type: ignore[arg-type]
mcp.tool()(storage_fetch_records)  # type: ignore[arg-type]
mcp.tool()(storage_delete_record)  # type: ignore[arg-type]
mcp.tool()(storage_purge_record)  # type: ignore[arg-type]

# This module can be imported by the main entry point
