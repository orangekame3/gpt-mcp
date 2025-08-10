#!/usr/bin/env python3
"""OpenAI MCP Server - Bridge OpenAI models to Claude via MCP."""

import os
from typing import Optional
from dotenv import load_dotenv
from openai import OpenAI
from mcp.server.fastmcp import FastMCP

load_dotenv()

# Configuration from environment variables
config = {
    "api_key": os.getenv("OPENAI_API_KEY"),
    "max_retries": int(os.getenv("OPENAI_MAX_RETRIES", "3")),
    "timeout": float(os.getenv("OPENAI_API_TIMEOUT", "60")),
    "reasoning_effort": os.getenv("REASONING_EFFORT", "minimal"),
    "verbosity": os.getenv("VERBOSITY", "low"),
    "model": os.getenv("OPENAI_MODEL", "gpt-5"),
}

# OpenAI client will be initialized in main() after config validation
client = None

# Create MCP server instance
mcp_server = FastMCP("gpt-mcp")


@mcp_server.tool()
def list_models() -> str:
    """List available OpenAI models (filtered to supported models only)."""
    if client is None:
        return "Error: OpenAI client not initialized"
    
    # Supported models only
    supported_models = [
        "o3",
        "gpt-5"
    ]
    
    result = "Available OpenAI Models (Supported by this server):\n\n"
    result += "Chat Models with Web Search:\n"
    result += "\n".join(f"- {m}" for m in supported_models)
    result += "\n\n"
    
    return result


@mcp_server.tool()
def advanced_search(
    prompt: str,
    model: Optional[str] = None,
    reasoning_effort: Optional[str] = None,
    verbosity: Optional[str] = None,
    enable_web_search: bool = True
) -> str:
    """Advanced AI search with web capabilities and reasoning.
    
    This tool provides intelligent web search and reasoning capabilities,
    similar to o3's search but available for multiple OpenAI models.
    Useful for finding the latest information, troubleshooting errors,
    and discussing complex ideas or design challenges.
    
    Args:
        prompt: The search query or prompt
        model: Model to use (o3, gpt-5). Defaults to environment setting
        reasoning_effort: Reasoning level (minimal, low, medium, high)
        verbosity: Output detail level (low, medium, high) - GPT-5 only
        enable_web_search: Enable web search capabilities
    
    Supported models: o3, gpt-5
    """
    if client is None:
        return "Error: OpenAI client not initialized"
    
    # Supported models only
    supported_models = ["o3", "gpt-5"]
    
    # Use provided model or fall back to environment/config default
    selected_model = model or config["model"]
    
    # Validate model is supported
    if selected_model not in supported_models:
        return f"Error: Model '{selected_model}' is not supported. Supported models: {', '.join(supported_models)}"
    
    reasoning = reasoning_effort or config["reasoning_effort"]
    selected_verbosity = verbosity or config["verbosity"]
        
    try:
        # Build parameters for responses.create
        params = {
            "model": selected_model,
            "input": prompt,
        }
        
        # Add web search tools if enabled
        if enable_web_search:
            params["tools"] = [{"type": "web_search_preview"}]
        
        # Add reasoning for o3 family models and gpt-5
        if selected_model.startswith("o3") or selected_model == "gpt-5":
            params["reasoning"] = {"effort": reasoning}
        
        # Add verbosity control for GPT-5
        if selected_model == "gpt-5":
            params["text"] = {"verbosity": selected_verbosity}
        
        response = client.responses.create(**params)  # type: ignore
        content = getattr(response, 'output_text', None) or "No response text available."

        # Add model information to the response
        result = f"**Model Used:** {selected_model}\n**Reasoning Effort:** {reasoning}\n**Verbosity:** {selected_verbosity}\n\n{content}"
        return result

    except Exception as e:
        return f"Error in advanced search: {str(e)}"


def main():
    """Run the MCP server."""
    global client
    
    # Check for API key
    if not config["api_key"]:
        print("Error: OPENAI_API_KEY environment variable is not set")
        print("Please set it in your .env file or environment")
        return

    # Initialize OpenAI client with retry and timeout configuration
    client = OpenAI(
        api_key=config["api_key"],  # type: ignore
        max_retries=config["max_retries"],  # type: ignore
        timeout=config["timeout"],  # type: ignore
    )

    # Print configuration on startup
    print("GPT MCP Server starting with configuration:")
    print(f"  Max retries: {config['max_retries']}")
    print(f"  Timeout: {config['timeout']}s")
    print(f"  Reasoning effort: {config['reasoning_effort']}")
    print(f"  Verbosity: {config['verbosity']}")
    print("  Supported models: o3, gpt-5")

    # Run the server
    mcp_server.run()


if __name__ == "__main__":
    main()
