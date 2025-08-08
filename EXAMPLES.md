# GPT MCP Server Examples

This document provides practical examples of using the GPT MCP Server with Claude.

## Advanced Search Examples

### Debugging Code Issues

```
User: I'm getting "TypeError: Cannot read property 'map' of undefined" in my React component. 
     Use advanced_search to help me debug this.

Claude: I'll use advanced_search to find solutions for this common React error.
[Uses advanced_search tool with the error message]
```

### Research Current Technologies

```
User: Use advanced_search with high reasoning effort to find the best practices 
     for implementing WebRTC in 2025.

Claude: I'll search for the latest WebRTC implementation best practices with high reasoning effort.
[Uses advanced_search with reasoning_effort="high"]
```

### Architecture Design

```
User: I need to design a microservices architecture for an e-commerce platform. 
     Use advanced_search to explore modern patterns and considerations.

Claude: I'll search for modern microservices patterns for e-commerce platforms.
[Uses advanced_search with comprehensive query]
```

## Model-Specific Features

### Using o3 Model (with native web search)

```
User: Use advanced_search with the o3 model to find information about the latest 
     developments in quantum computing.

Claude: I'll use the o3 model with its native web search capabilities.
[Uses advanced_search with model="o3"]
```

### Comparing Different Models

```
User: Compare the responses from gpt-4o and gpt-4o-mini using advanced_search 
     about "implementing OAuth 2.0 in Node.js"

Claude: I'll search for OAuth 2.0 implementation guides using both models.
[Uses advanced_search twice with different models]
```

## Configuration Examples

### High Precision Search

```json
{
  "mcpServers": {
    "gpt": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/orangekame3/gpt-mcp.git", "gpt-mcp"],
      "env": {
        "OPENAI_API_KEY": "your-key",
        "SEARCH_CONTEXT_SIZE": "high",
        "REASONING_EFFORT": "high",
        "OPENAI_API_TIMEOUT": "120"
      }
    }
  }
}
```

### Fast Response Configuration

```json
{
  "mcpServers": {
    "gpt": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/orangekame3/gpt-mcp.git", "gpt-mcp"],
      "env": {
        "OPENAI_API_KEY": "your-key",
        "SEARCH_CONTEXT_SIZE": "low",
        "REASONING_EFFORT": "low",
        "OPENAI_API_TIMEOUT": "30"
      }
    }
  }
}
```

## Other Tools Examples

### Direct Chat Completion

```
User: Use chat_completion with gpt-4o to write a haiku about programming.

Claude: I'll use GPT-4o to create a programming haiku.
[Uses chat_completion tool]
```

### Image Generation

```
User: Generate an image of a cyberpunk cat using DALL-E 3 in HD quality.

Claude: I'll generate a cyberpunk cat image using DALL-E 3.
[Uses generate_image with model="dall-e-3" and quality="hd"]
```

### Model Discovery

```
User: List all available OpenAI models and categorize them by type.

Claude: I'll list all available OpenAI models for you.
[Uses list_models tool]
```

## Advanced Workflows

### Multi-Step Problem Solving

```
User: I want to build a real-time chat application. First, use advanced_search 
     to research WebSocket vs Server-Sent Events. Then, based on the findings, 
     generate example code using chat_completion.

Claude: I'll help you research and implement a real-time chat application.
1. First, I'll search for comparisons between WebSocket and SSE
   [Uses advanced_search]
2. Based on the research, I'll generate example code
   [Uses chat_completion]
```

### Research and Visualization

```
User: Use advanced_search to find trending UI design patterns for 2025, 
     then generate an image that represents these trends.

Claude: I'll research UI trends and create a visual representation.
1. Searching for 2025 UI design trends
   [Uses advanced_search]
2. Creating a visual based on the trends
   [Uses generate_image]
```

## Tips for Best Results

1. **Be Specific**: More detailed queries yield better results
2. **Adjust Settings**: Use high reasoning effort for complex problems
3. **Choose the Right Model**: o3 for web search, GPT-4o for general tasks
4. **Combine Tools**: Use multiple tools together for comprehensive solutions
5. **Iterate**: Refine your queries based on initial results