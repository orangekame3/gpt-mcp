# GPT MCP Server

An MCP (Model Context Protocol) server that provides access to OpenAI's models through Claude.

> **Note**: This project is strongly inspired by [yoshiko-pg/o3-search-mcp](https://github.com/yoshiko-pg/o3-search-mcp). While o3-search-mcp focuses on the o3 model, this server extends the concept to support all OpenAI models with similar web search capabilities.

## Features

- **Advanced Search with Web Capabilities** - Intelligent search and reasoning for all models (o3, GPT-5, GPT-4o, etc.)
- **Model Discovery** - List all available OpenAI models
- **Configurable Reasoning** - Adjust reasoning effort (low/medium/high)
- **Search Context Control** - Fine-tune search context size
- **Robust Error Handling** - Configurable retries and timeouts
- **Default GPT-5 Model** - Uses GPT-5 as the default model

## Installation

### Option 1: Using uvx (Recommended)

No installation needed! You can run directly with uvx:

```bash
# Run directly from GitHub
uvx --from git+https://github.com/orangekame3/gpt-mcp.git gpt-mcp
```

### Option 2: Using Claude Code (Recommended)

If you're using Claude Code, you can easily add this MCP server:

#### Method 1: Using claude mcp add command with environment variables

```bash
# Add as 'gpt' - this allows you to call it with just 'gpt'
claude mcp add gpt \
    -s user \
    -e OPENAI_API_KEY=your-api-key \
    -e SEARCH_CONTEXT_SIZE=medium \
    -e REASONING_EFFORT=medium \
    -e OPENAI_API_TIMEOUT=60 \
    -e OPENAI_MAX_RETRIES=3 \
    -e OPENAI_MODEL=gpt-5 \
    -- uvx --from git+https://github.com/orangekame3/gpt-mcp.git gpt-mcp
```

#### Method 2: Using .env file with source

If you have a `.env` file, you can source it first:

```bash
# Source your .env file
source .env

# Then add the MCP server using the environment variables
claude mcp add gpt \
    -s user \
    -e OPENAI_API_KEY=$OPENAI_API_KEY \
    -e SEARCH_CONTEXT_SIZE=$SEARCH_CONTEXT_SIZE \
    -e REASONING_EFFORT=$REASONING_EFFORT \
    -e OPENAI_API_TIMEOUT=$OPENAI_API_TIMEOUT \
    -e OPENAI_MAX_RETRIES=$OPENAI_MAX_RETRIES \
    -e OPENAI_MODEL=$OPENAI_MODEL \
    -- uvx --from git+https://github.com/orangekame3/gpt-mcp.git gpt-mcp
```

After installation, you can use it directly in Claude Code:
```bash
# Use advanced search
> Use advanced_search to find the latest React best practices

# List available models
> Use list_models to show available OpenAI models
```

### Option 3: Clone and Install

```bash
# Clone the repository
git clone https://github.com/orangekame3/gpt-mcp.git
cd gpt-mcp

# Install with uv
uv sync

# Or install with pip
pip install -e .
```

## Configuration

### Setting up OpenAI API Key

1. Get your API key from [OpenAI Platform](https://platform.openai.com/api-keys)

2. For local development, create `.env` file:
```bash
cp .env.example .env
# Edit .env and add your API key
```

### Using with Claude Code settings.json

For Claude Code users, you can also configure environment variables using `settings.json`:

```bash
# Copy the example settings file
cp settings.json.example settings.json
# Edit settings.json and add your API key
```

This file will be used by Claude Code to set environment variables for your session. Note that `settings.json` is gitignored to protect your credentials.

### Claude Desktop Configuration

Claude Desktop uses a `claude_desktop_config.json` file for MCP server configuration.

**Location:**
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- Linux: `~/.config/Claude/claude_desktop_config.json`

#### Using uvx (Recommended)

```json
{
  "mcpServers": {
    "gpt": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/orangekame3/gpt-mcp.git", "gpt-mcp"],
      "env": {
        "OPENAI_API_KEY": "your-api-key-here",
        "OPENAI_MODEL": "gpt-5",
        "SEARCH_CONTEXT_SIZE": "medium",
        "REASONING_EFFORT": "medium",
        "OPENAI_API_TIMEOUT": "60",
        "OPENAI_MAX_RETRIES": "3"
      }
    }
  }
}
```

#### Using local installation with uv

```json
{
  "mcpServers": {
    "gpt": {
      "command": "uv",
      "args": ["--directory", "/path/to/gpt-mcp", "run", "gpt-mcp"],
      "env": {
        "OPENAI_API_KEY": "your-api-key-here",
        "OPENAI_MODEL": "gpt-5",
        "SEARCH_CONTEXT_SIZE": "medium",
        "REASONING_EFFORT": "medium",
        "OPENAI_API_TIMEOUT": "60",
        "OPENAI_MAX_RETRIES": "3"
      }
    }
  }
}
```

#### Using pip installation

```json
{
  "mcpServers": {
    "gpt": {
      "command": "gpt-mcp",
      "env": {
        "OPENAI_API_KEY": "your-api-key-here",
        "OPENAI_MODEL": "gpt-5",
        "SEARCH_CONTEXT_SIZE": "medium",
        "REASONING_EFFORT": "medium",
        "OPENAI_API_TIMEOUT": "60",
        "OPENAI_MAX_RETRIES": "3"
      }
    }
  }
}
```

## Available Tools

### advanced_search
Advanced AI search with web capabilities and reasoning.

This tool provides intelligent web search and reasoning capabilities, similar to o3's search but available for multiple OpenAI models. Perfect for:
- Finding the latest information
- Troubleshooting errors 
- Discussing complex ideas or design challenges
- Research tasks requiring current data

Parameters:
- `prompt`: Your question or search query
- `model`: The model to use (default: uses environment variable OPENAI_MODEL or "gpt-5")
- `search_context_size`: Control search depth - "low", "medium", "high" (optional)
- `reasoning_effort`: Reasoning intensity - "low", "medium", "high" (optional)
- `enable_web_search`: Whether to enable web search (default: true)

### list_models
List all available OpenAI models, categorized by type (chat models and completion models).

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENAI_API_KEY` | Yes | - | Your OpenAI API key |
| `OPENAI_MODEL` | No | `gpt-5` | Default model to use for advanced_search |
| `SEARCH_CONTEXT_SIZE` | No | `medium` | Search context depth (low/medium/high) |
| `REASONING_EFFORT` | No | `medium` | Reasoning intensity (low/medium/high) |
| `OPENAI_API_TIMEOUT` | No | `60` | API timeout in seconds |
| `OPENAI_MAX_RETRIES` | No | `3` | Max retry attempts for failed requests |

## Use Cases

### 🐛 Debugging Complex Issues
```
> I'm getting a "WebSocket connection failed" error. Use advanced_search to find solutions.
```

### 📚 Research with Latest Information
```
> Use advanced_search to find the latest best practices for React Server Components in 2025.
```

### 🧩 Design and Architecture Discussions
```
> I want to design a real-time collaborative editor. Use advanced_search with high reasoning effort to explore architectures.
```

### 🔍 Comparing Technologies
```
> Use advanced_search to compare Rust vs Go for building high-performance web servers in 2025.
```

## Development

```bash
# Run the server directly
uv run gpt-mcp

# Run with Python
python -m src.server
```

## Notes

- For o3 model access, you need Tier 4 or organizational verification on OpenAI
- The `advanced_search` tool provides o3-like capabilities for all models
- Web search is simulated for non-o3 models through intelligent prompting
- All OpenAI rate limits and usage charges apply

## License

MIT