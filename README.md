# GPT MCP Server

An MCP (Model Context Protocol) server that provides access to OpenAI's models through Claude, inspired by o3-search-mcp but with support for all OpenAI models.

## Features

- **Advanced Search with Web Capabilities** - Intelligent search and reasoning for all models (o3, GPT-4o, etc.)
- **Chat Completions** - Support for GPT-4o, GPT-4o-mini, and other chat models
- **Text Completion** - Traditional completion with instruction-following models
- **Image Generation** - Create images with DALL-E 2 and DALL-E 3
- **Model Discovery** - List all available OpenAI models
- **Configurable Reasoning** - Adjust reasoning effort (low/medium/high)
- **Search Context Control** - Fine-tune search context size
- **Robust Error Handling** - Configurable retries and timeouts

## Installation

### Option 1: Using uvx (Recommended)

No installation needed! You can run directly with uvx:

```bash
# Run directly from GitHub
uvx --from git+https://github.com/orangekame3/gpt-mcp.git gpt-mcp
```

### Option 2: Using Claude Code (Recommended)

If you're using Claude Code, you can easily add this MCP server:

```bash
# Add as 'gpt' - this allows you to call it with just 'gpt'
claude mcp add gpt \
    -s user \
    -e OPENAI_API_KEY=your-api-key \
    -e SEARCH_CONTEXT_SIZE=medium \
    -e REASONING_EFFORT=medium \
    -e OPENAI_API_TIMEOUT=60 \
    -e OPENAI_MAX_RETRIES=3 \
    -- uvx --from git+https://github.com/orangekame3/gpt-mcp.git gpt-mcp
```

After installation, you can use it directly in Claude Code:
```bash
# Use advanced search
> Use advanced_search to find the latest React best practices

# Use image generation  
> Generate an image of a cyberpunk city using DALL-E 3

# Use chat completion with specific models
> Use chat_completion with gpt-4o to explain quantum computing
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
        "OPENAI_API_KEY": "your-api-key-here"
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
        "OPENAI_API_KEY": "your-api-key-here"
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
        "OPENAI_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

## Available Tools

### advanced_search
Advanced AI search with web capabilities and reasoning.

This is the main tool inspired by o3-search-mcp, but works with all OpenAI models. Perfect for:
- Finding the latest information
- Troubleshooting errors 
- Discussing complex ideas or design challenges
- Research tasks requiring current data

Parameters:
- `prompt`: Your question or search query
- `model`: The model to use (default: "gpt-4o", supports "o3" for native web search)
- `search_context_size`: Control search depth - "low", "medium", "high" (optional)
- `reasoning_effort`: Reasoning intensity - "low", "medium", "high" (optional)
- `enable_web_search`: Whether to enable web search (default: true)

### chat_completion
Send chat completion requests to OpenAI's chat models.

Parameters:
- `model`: The model to use (default: "gpt-4o-mini")
- `messages`: List of message objects with "role" and "content"
- `temperature`: Sampling temperature 0-2 (default: 0.7)
- `max_tokens`: Maximum tokens to generate (optional)
- `system`: System message to prepend (optional)

### text_completion
Generate text using OpenAI's completion API.

Parameters:
- `prompt`: The text prompt
- `model`: The model to use (default: "gpt-3.5-turbo-instruct")
- `max_tokens`: Maximum tokens to generate (default: 100)
- `temperature`: Sampling temperature 0-2 (default: 0.7)

### generate_image
Generate images using DALL-E models.

Parameters:
- `prompt`: The image description
- `model`: "dall-e-2" or "dall-e-3" (default: "dall-e-3")
- `size`: Image size (default: "1024x1024")
- `quality`: "standard" or "hd" for DALL-E 3 (default: "standard")
- `n`: Number of images to generate (default: 1)

### list_models
List all available OpenAI models.

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENAI_API_KEY` | Yes | - | Your OpenAI API key |
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
python -m openai_mcp_server
```

## Notes

- For o3 model access, you need Tier 4 or organizational verification on OpenAI
- The `advanced_search` tool provides o3-like capabilities for all models
- Web search is simulated for non-o3 models through intelligent prompting
- All OpenAI rate limits and usage charges apply

## License

MIT