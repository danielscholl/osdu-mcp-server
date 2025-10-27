"""OSDU Legal service client."""

import os
import re
from typing import Any

from ..exceptions import OSMCPAPIError
from ..osdu_client import OsduClient
from ..service_urls import OSMCPService, get_service_base_url


class LegalClient(OsduClient):
    """Client for OSDU Legal service operations."""

    def __init__(self, *args, **kwargs):
        """Initialize LegalClient with service-specific configuration."""
        super().__init__(*args, **kwargs)
        self._base_path = get_service_base_url(OSMCPService.LEGAL)

    async def get(self, path: str, **kwargs: Any) -> dict[str, Any]:
        """Override get to include service base path."""
        full_path = f"{self._base_path}{path}"
        return await super().get(full_path, **kwargs)

    async def post(self, path: str, data: Any = None, **kwargs: Any) -> dict[str, Any]:
        """Override post to include service base path."""
        full_path = f"{self._base_path}{path}"
        if data is None and "json" in kwargs:
            data = kwargs.pop("json")
        return await super().post(full_path, data, **kwargs)

    async def put(self, path: str, data: Any = None, **kwargs: Any) -> dict[str, Any]:
        """Override put to include service base path."""
        full_path = f"{self._base_path}{path}"
        if data is None and "json" in kwargs:
            data = kwargs.pop("json")
        return await super().put(full_path, data, **kwargs)

    async def delete(self, path: str, **kwargs: Any) -> dict[str, Any]:
        """Override delete to include service base path."""
        full_path = f"{self._base_path}{path}"
        return await super().delete(full_path, **kwargs)

    def ensure_full_tag_name(self, name: str) -> str:
        """Ensure legal tag name includes partition prefix.

        Args:
            name: Tag name with or without partition prefix

        Returns:
            Tag name with partition prefix
        """
        # If it already has the partition prefix, return as-is
        if name.startswith(f"{self._data_partition}-"):
            return name

        # Add partition prefix
        return f"{self._data_partition}-{name}"

    def simplify_tag_name(self, name: str) -> str:
        """Remove partition prefix from legal tag name if present.

        Args:
            name: Full tag name with partition prefix

        Returns:
            Simplified tag name without partition prefix
        """
        pattern = f"^{self._data_partition}-"
        return re.sub(pattern, "", name)

    def check_delete_permission(self) -> None:
        """Check if delete operations are enabled.

        Raises:
            OSMCPAPIError: If delete operations are disabled
        """
        if not os.environ.get("OSDU_MCP_ENABLE_DELETE_MODE", "false").lower() == "true":
            raise OSMCPAPIError(
                "Delete operations are disabled. Set OSDU_MCP_ENABLE_DELETE_MODE=true to enable legal tag deletion",
                status_code=403,
            )

    async def list_legal_tags(self, valid: bool | None = None) -> dict[str, Any]:
        """List all legal tags.

        Args:
            valid: Optional filter for valid/invalid tags

        Returns:
            List of legal tags
        """
        params = {}
        if valid is not None:
            params["valid"] = str(valid).lower()

        return await self.get("/legaltags", params=params)

    async def get_legal_tag(self, name: str) -> dict[str, Any]:
        """Get a specific legal tag.

        Args:
            name: Legal tag name

        Returns:
            Legal tag details
        """
        full_name = self.ensure_full_tag_name(name)
        return await self.get(f"/legaltags/{full_name}")

    async def get_legal_tag_properties(self) -> dict[str, Any]:
        """Get allowed property values for legal tags.

        Returns:
            Allowed property values
        """
        return await self.get("/legaltags:properties")

    async def search_legal_tags(
        self,
        query: list[str] | None = None,
        sort_by: str | None = None,
        sort_order: str | None = None,
        limit: int | None = None,
    ) -> dict[str, Any]:
        """Search legal tags with filter conditions.

        Args:
            query: Filter conditions
            sort_by: Field to sort by
            sort_order: ASC or DESC
            limit: Maximum results

        Returns:
            Filtered legal tags
        """
        body = {}
        if query:
            body["queryList"] = query
        if sort_by:
            body["sortBy"] = sort_by
        if sort_order:
            body["sortOrder"] = sort_order
        if limit:
            body["limit"] = limit

        return await self.post("/legaltags:query", json=body)

    async def batch_retrieve_legal_tags(self, names: list[str]) -> dict[str, Any]:
        """Retrieve multiple legal tags by name.

        Args:
            names: List of legal tag names (max 25)

        Returns:
            List of legal tags
        """
        if len(names) > 25:
            raise OSMCPAPIError(
                "Too many legal tags requested. Maximum 25 legal tags can be retrieved at once",
                status_code=400,
            )

        # Ensure all names have partition prefix
        full_names = [self.ensure_full_tag_name(name) for name in names]

        return await self.post("/legaltags:batchRetrieve", json={"names": full_names})

    async def create_legal_tag(
        self, name: str, description: str, properties: dict[str, Any]
    ) -> dict[str, Any]:
        """Create a new legal tag.

        Args:
            name: Legal tag name (without partition prefix)
            description: Tag description
            properties: Tag properties

        Returns:
            Created legal tag
        """
        body = {
            "name": name,  # API expects name without partition prefix
            "description": description,
            "properties": properties,
        }

        return await self.post("/legaltags", json=body)

    async def update_legal_tag(
        self,
        name: str,
        description: str | None = None,
        contract_id: str | None = None,
        expiration_date: str | None = None,
        extension_properties: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Update an existing legal tag.

        Args:
            name: Legal tag name
            description: New description
            contract_id: New contract ID
            expiration_date: New expiration date
            extension_properties: New extension properties

        Returns:
            Updated legal tag
        """
        full_name = self.ensure_full_tag_name(name)
        body = {"name": full_name}

        if description is not None:
            body["description"] = description
        if contract_id is not None:
            body["contractId"] = contract_id
        if expiration_date is not None:
            body["expirationDate"] = expiration_date
        if extension_properties is not None:
            body["extensionProperties"] = extension_properties

        return await self.put("/legaltags", json=body)

    async def delete_legal_tag(self, name: str) -> None:
        """Delete a legal tag.

        Args:
            name: Legal tag name
        """
        # Check delete permission for delete operations
        self.check_delete_permission()

        full_name = self.ensure_full_tag_name(name)
        await self.delete(f"/legaltags/{full_name}")
