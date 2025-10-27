# Contributing to OSDU MCP Server

Thank you for your interest in contributing to the OSDU MCP Server! This guide will help you get started.

## Getting Started

### Prerequisites

- Python 3.12 or 3.13
- [uv](https://docs.astral.sh/uv/) package manager
- Git
- Access to an OSDU platform instance (for testing)

### Development Setup

1. **Fork and clone the repository:**
   ```bash
   git clone https://github.com/your-username/osdu-mcp-server.git
   cd osdu-mcp-server
   ```

2. **Install dependencies:**
   ```bash
   uv sync
   uv pip install -e '.[dev]'
   ```

3. **Verify installation:**
   ```bash
   uv run pytest --version
   uv run black --version
   uv run ruff --version
   uv run mypy --version
   ```

## Development Workflow

### 1. Create an Issue

Before starting work, create an issue describing:
- The problem you're solving or feature you're adding
- Proposed approach
- Expected behavior

```bash
gh issue create -t "Title" -b "Description" -l "enhancement"
```

### 2. Create a Feature Branch

```bash
git checkout -b feature/issue-number-short-description
```

Branch naming conventions:
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring

### 3. Make Your Changes

Follow these guidelines:

- **Code Style**: Code is automatically formatted with `black` and linted with `ruff`
- **Type Hints**: Add type hints for all function signatures
- **Documentation**: Update docstrings and relevant docs
- **Tests**: Add tests for new functionality (see Testing section)

### 4. Run Quality Checks

Before committing, run all quality checks:

```bash
# Format code
uv run black src/ tests/

# Lint code
uv run ruff check src/ tests/

# Type check
uv run mypy src/

# Run tests with coverage
uv run pytest --cov=src/osdu_mcp_server --cov-report=term-missing --cov-fail-under=70
```

All checks must pass before submitting a PR.

### 5. Commit Your Changes

We use [Conventional Commits](https://www.conventionalcommits.org/) for automatic versioning:

```bash
# Format: <type>(<scope>): <description>

git commit -m "feat(storage): add record versioning support"
git commit -m "fix(auth): resolve token expiration handling"
git commit -m "docs: update authentication guide"
```

**Commit Types:**
- `feat:` - New features (minor version bump)
- `fix:` - Bug fixes (patch version bump)
- `feat!:` or `BREAKING CHANGE:` - Breaking changes (major version bump)
- `docs:` - Documentation only
- `test:` - Test additions or updates
- `refactor:` - Code refactoring
- `chore:` - Maintenance tasks

### 6. Create a Pull Request

```bash
git push origin feature/issue-number-short-description
gh pr create --title "feat: Add new feature" --body "Closes #123"
```

**PR Checklist:**
- [ ] Tests pass locally
- [ ] Code coverage meets 70% threshold
- [ ] Type checking passes
- [ ] Code formatted with black
- [ ] Commit messages follow Conventional Commits
- [ ] Documentation updated (if needed)
- [ ] CHANGELOG.md updated (automatic via release-please)

## Testing

### Writing Tests

We use behavior-driven testing (see [ADR-010](docs/adr/010-testing-philosophy-and-strategy.md)):

```python
# tests/tools/storage/test_my_feature.py
import pytest
from aioresponses import aioresponses

@pytest.mark.asyncio
async def test_feature_handles_error_gracefully():
    """Test that the feature gracefully handles API errors."""

    with aioresponses() as mocked:
        # Mock external service behavior
        mocked.get("https://osdu.com/api/storage/v2/records/123", status=404)

        result = await my_feature("123")

        # Verify behavior - what the user sees
        assert result["status"] == "not_found"
        assert "does not exist" in result["message"]
```

**Testing Guidelines:**
- Test behaviors, not implementation details
- Mock at service boundaries only (HTTP, auth providers)
- Each test should be self-documenting
- Aim for 70%+ coverage, 90%+ for new features

### Running Tests

```bash
# Run all tests
uv run pytest

# Run specific test file
uv run pytest tests/tools/storage/test_get_record.py

# Run with coverage
uv run pytest --cov=src/osdu_mcp_server --cov-report=html

# Run tests matching a pattern
uv run pytest -k "test_auth"
```

## Architecture and Design

### Architecture Decision Records (ADRs)

This project uses ADRs to document architectural decisions. See [docs/adr/](docs/adr/) for all decisions.

**Before making significant changes:**
1. Review relevant ADRs to understand design rationale
2. If your change conflicts with an ADR, discuss in an issue first
3. Major architectural changes may require a new ADR

Key ADRs to review:
- [ADR-007: Tool Implementation Pattern](docs/adr/007-tool-implementation-pattern.md)
- [ADR-010: Testing Philosophy](docs/adr/010-testing-philosophy-and-strategy.md)
- [ADR-020: Write Protection](docs/adr/020-unified-write-protection.md)

### Project Structure

```
src/osdu_mcp_server/
├── main.py              # Entry point
├── server.py            # FastMCP server registration
├── shared/              # Shared utilities
│   ├── auth_handler.py  # Authentication
│   ├── config_manager.py # Configuration
│   └── clients/         # Service-specific API clients
├── tools/               # MCP tool implementations
│   ├── storage/         # Storage service tools
│   ├── search/          # Search service tools
│   └── ...
├── prompts/             # MCP prompts
└── resources/           # Templates and references

tests/                   # Mirrors src/ structure
```

## Adding New Features

### Adding a New Tool

1. **Create tool module** in appropriate service directory:
   ```python
   # src/osdu_mcp_server/tools/storage/my_tool.py
   from osdu_mcp_server.shared.exceptions import handle_osdu_exceptions

   @handle_osdu_exceptions
   async def storage_my_tool(param: str) -> dict:
       """
       Brief description of what the tool does.

       Args:
           param: Description of parameter

       Returns:
           Description of return value
       """
       # Implementation
   ```

2. **Register in server.py:**
   ```python
   from .tools.storage import storage_my_tool
   mcp.tool()(storage_my_tool)  # type: ignore[arg-type]
   ```

3. **Add tests:**
   ```python
   # tests/tools/storage/test_my_tool.py
   @pytest.mark.asyncio
   async def test_my_tool_success():
       """Test successful execution."""
       # Test implementation
   ```

4. **Update documentation** if needed

## Code Review Process

1. **Automated Checks**: CI runs tests, linting, type checking
2. **Security Scans**: CodeQL and dependency scans
3. **Manual Review**: Maintainers review code and architecture
4. **Approval**: At least one maintainer approval required
5. **Merge**: Squash and merge with conventional commit message

## Release Process

Releases are automated using Release Please:

1. Merge commits to `main` using Conventional Commits
2. Release Please creates/updates a release PR
3. Merge the release PR to publish to PyPI
4. GitHub release is created automatically

## Getting Help

- **Documentation**: Check [docs/](docs/) directory
- **Issues**: Search existing issues or create a new one
- **Discussions**: Use GitHub Discussions for questions

## Code of Conduct

Be respectful and inclusive. We're all here to build great software together.

## License

By contributing, you agree that your contributions will be licensed under the Apache License 2.0.

---

## Additional Resources

- **[Architecture Overview](docs/project-architect.md)** - System design and patterns
- **[ADRs](docs/adr/README.md)** - All architectural decisions
- **[Authentication Guide](docs/authentication.md)** - Detailed auth setup

**Note:** This project was built with AI assistance (Claude Code and GitHub Copilot). While AI tools helped with development, all contributions follow the same standards regardless of how they were created.
