# MCP Server Setup Guide

This guide explains how to set up the GPT MCP server with Claude Desktop.

## What is MCP?

MCP (Model Context Protocol) is an open protocol that enables seamless integration between AI assistants and external tools. It allows Claude to interact with various services and APIs through a standardized interface.

## Prerequisites

- Claude Desktop app installed
- OpenAI API key
- Python 3.9+ (if installing locally)
- uv/uvx (recommended) or pip

## Quick Start with Claude Code

The easiest way to use this MCP server is with Claude Code:

```bash
claude mcp add gpt \
    -s user \
    -e OPENAI_API_KEY=your-api-key \
    -e SEARCH_CONTEXT_SIZE=medium \
    -e REASONING_EFFORT=medium \
    -- uvx --from git+https://github.com/orangekame3/gpt-mcp.git gpt-mcp
```

## Manual Setup with uvx

Alternatively, you can set it up manually with `uvx`:

1. Install uv/uvx if you haven't already:
```bash
# On macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

2. Edit your Claude Desktop configuration file:

**Find the config file:**
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- Linux: `~/.config/Claude/claude_desktop_config.json`

3. Add the GPT MCP server configuration:

```json
{
  "mcpServers": {
    "gpt": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/orangekame3/gpt-mcp.git", "gpt-mcp"],
      "env": {
        "OPENAI_API_KEY": "sk-your-openai-api-key-here",
        "SEARCH_CONTEXT_SIZE": "medium",
        "REASONING_EFFORT": "medium",
        "OPENAI_API_TIMEOUT": "60",
        "OPENAI_MAX_RETRIES": "3"
      }
    }
  }
}
```

4. Restart Claude Desktop

## Configuration Options

### Multiple MCP Servers

You can run multiple MCP servers simultaneously:

```json
{
  "mcpServers": {
    "gpt": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/orangekame3/gpt-mcp.git", "gpt-mcp"],
      "env": {
        "OPENAI_API_KEY": "sk-your-key"
      }
    },
    "another-server": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/example/another-mcp.git", "another-mcp"],
      "env": {
        "API_KEY": "another-key"
      }
    }
  }
}
```

### Environment Variables

You can use system environment variables instead of hardcoding API keys:

```json
{
  "mcpServers": {
    "gpt": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/orangekame3/gpt-mcp.git", "gpt-mcp"]
    }
  }
}
```

Then set the environment variable in your shell:
```bash
export OPENAI_API_KEY="sk-your-key"
```

## Troubleshooting

### Server not connecting

1. Check Claude Desktop logs:
   - macOS: `~/Library/Logs/Claude/`
   - Windows: `%LOCALAPPDATA%\Claude\logs\`
   - Linux: `~/.local/share/Claude/logs/`

2. Verify your API key is correct

3. Ensure you've restarted Claude Desktop after updating the config

### Permission issues

On macOS/Linux, ensure the config file has proper permissions:
```bash
chmod 644 ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

### Testing the server

You can test the server directly:
```bash
uvx --from git+https://github.com/orangekame3/gpt-mcp.git gpt-mcp
```

If it starts without errors, the server is working correctly.

## Using the Server in Claude

Once configured, you can use the OpenAI tools in Claude:

1. **Advanced Search** - The main feature for intelligent search and reasoning
2. **Chat Completions** - Direct access to specific models
3. **Image Generation** - Create images with DALL-E
4. **Model Discovery** - List available models

### Example Prompts

#### For Debugging:
```
> I'm getting this error: [paste error]. Use advanced_search to find solutions.
```

#### For Research:
```
> Use advanced_search to find the latest information about WebAssembly performance optimizations.
```

#### For Design Discussions:
```
> I want to build a distributed cache system. Use advanced_search with high reasoning effort to explore design patterns.
```

#### For Direct Model Access:
```
> Use chat_completion with gpt-4o to explain the difference between TCP and UDP.
```

#### For Image Generation:
```
> Generate an image of a futuristic city using DALL-E 3.
```

## Security Notes

- Never commit your API keys to version control
- Use environment variables for sensitive data when possible
- Regularly rotate your API keys
- Monitor your OpenAI usage to prevent unexpected charges

## Differences from o3-search-mcp

This server is inspired by o3-search-mcp but offers:

1. **Multi-Model Support** - Works with all OpenAI models, not just o3
2. **Flexible Implementation** - Native o3 web search when available, intelligent prompting for other models
3. **Python-Based** - Easy to extend and modify
4. **Additional Tools** - Beyond search: chat, completion, image generation, and model listing

## Additional Resources

- [MCP Documentation](https://modelcontextprotocol.io/)
- [Claude Desktop Docs](https://docs.anthropic.com/claude/docs/claude-desktop)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [o3 Model Access Requirements](https://help.openai.com/en/articles/10362446-api-access-to-o1-o3-and-o4-models)