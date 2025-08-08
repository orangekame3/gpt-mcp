# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python-based MCP (Model Context Protocol) server that provides access to OpenAI models through Claude Desktop. It's inspired by o3-search-mcp but supports all OpenAI models with intelligent web search simulation.

## Development Commands

### Running the Server
```bash
# Run the server directly
uv run gpt-mcp

# Run with Python module
python -m src.server

# Test server installation with uvx
uvx --from git+https://github.com/orangekame3/gpt-mcp.git gpt-mcp
```

### Package Management
```bash
# Install dependencies
uv sync

# Add new dependency
uv add package_name

# Remove dependency
uv remove package_name

# Update lockfile
uv lock

# Build package
uv build
```

### Environment Setup
```bash
# Copy and configure environment
cp .env.example .env
# Edit .env to add OPENAI_API_KEY
```

## Architecture

### Core Components

**Server Entry Point** (`src/server.py:197`): The `main()` function initializes the MCP server with configuration validation and starts the server streams.

**MCP Tools**: Two main tools are registered with the server:
- `list_models()` (`src/server.py:41`): Lists available OpenAI models, categorized by type
- `advanced_search()` (`src/server.py:107`): Primary tool providing intelligent search with web capabilities

**Configuration System**: Environment-based configuration loaded at startup:
- OpenAI API settings (key, timeout, retries)
- Search parameters (context size, reasoning effort)
- Default model selection

### Key Patterns

**Pydantic Models**: Uses Pydantic for argument validation:
- `ModelListArgs` (`src/server.py:36`): Empty model for list_models tool
- `AdvancedSearchArgs` (`src/server.py:84`): Complex model with optional parameters and defaults

**Async/Await Pattern**: All tool functions are async and use `asyncio.to_thread()` for OpenAI API calls to avoid blocking.

**Error Handling**: Comprehensive try-catch blocks return user-friendly error messages as TextContent objects.

**Model-Specific Logic**: The `advanced_search` tool handles o3 model differently:
- o3 models use the `responses.create` API with native web search
- Other models use `chat.completions.create` with simulated web search through prompting

## Configuration Files

- **pyproject.toml**: Project metadata, dependencies, and build configuration
- **mcp.json**: Local MCP server configuration for Claude Desktop
- **.env**: Environment variables (not committed to git)
- **uv.lock**: Dependency lockfile (similar to package-lock.json)

## Integration Points

**Claude Desktop**: The server integrates via the MCP protocol. Users configure it in `claude_desktop_config.json` with command `uvx --from git+https://github.com/orangekame3/gpt-mcp.git gpt-mcp`.

**OpenAI API**: Direct integration with OpenAI's Python client library. Supports both new response API (o3) and traditional chat completions.

**Environment Variables**: All sensitive configuration via environment variables:
- `OPENAI_API_KEY` (required)
- `SEARCH_CONTEXT_SIZE`, `REASONING_EFFORT`, `OPENAI_API_TIMEOUT`, `OPENAI_MAX_RETRIES` (optional)

## Development Notes

- Single Python file architecture in `src/server.py`
- Uses modern Python async/await patterns throughout
- No test files present - manual testing via MCP protocol
- Build system uses `uv` (modern Python package manager)
- Distribution via git+https URLs for easy installation with uvx