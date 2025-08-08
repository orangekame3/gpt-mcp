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
    "search_context_size": os.getenv("SEARCH_CONTEXT_SIZE", "medium"),
    "reasoning_effort": os.getenv("REASONING_EFFORT", "medium"),
    "model": os.getenv("OPENAI_MODEL", "gpt-5"),
}

# OpenAI client will be initialized in main() after config validation
client = None

# Create MCP server instance
mcp_server = FastMCP("gpt-mcp")


@mcp_server.tool()
def list_models() -> str:
    """List available OpenAI models."""
    if client is None:
        return "Error: OpenAI client not initialized"
    
    try:
        models = client.models.list()

        # Filter and organize models
        chat_models = []
        completion_models = []

        for model in models.data:
            if "gpt" in model.id:
                if "instruct" in model.id:
                    completion_models.append(model.id)
                else:
                    chat_models.append(model.id)

        result = "Available OpenAI Models:\n\n"

        if chat_models:
            result += "Chat Models:\n"
            result += "\n".join(f"- {m}" for m in sorted(chat_models))
            result += "\n\n"

        if completion_models:
            result += "Completion Models:\n"
            result += "\n".join(f"- {m}" for m in sorted(completion_models))
            result += "\n\n"

        return result

    except Exception as e:
        return f"Error listing models: {str(e)}"


@mcp_server.tool()
def advanced_search(
    prompt: str,
    model: Optional[str] = None,
    search_context_size: Optional[str] = None,
    reasoning_effort: Optional[str] = None,
    enable_web_search: bool = True
) -> str:
    """Advanced AI search with web capabilities and reasoning.
    
    This tool provides intelligent web search and reasoning capabilities,
    similar to o3's search but available for multiple OpenAI models.
    Useful for finding the latest information, troubleshooting errors,
    and discussing complex ideas or design challenges.
    """
    if client is None:
        return "Error: OpenAI client not initialized"
    
    # Use provided model or fall back to environment/config default
    selected_model = model or config["model"]
        
    try:
        # Prepare the message with search context
        messages = [
            {
                "role": "system",
                "content": (
                    "You are an AI assistant with advanced web search and reasoning capabilities. "
                    "Provide comprehensive, well-researched answers based on the latest information available. "
                    "When relevant, cite sources and explain your reasoning process."
                )
            },
            {"role": "user", "content": prompt}
        ]

        # Use provided settings or fall back to environment settings
        search_context = search_context_size or str(config["search_context_size"])
        reasoning = reasoning_effort or config["reasoning_effort"]

        # Prepare additional parameters based on model capabilities
        extra_params = {}

        # For o3 model, use the responses API with web search
        if selected_model == "o3":
            # o3 specific implementation
            try:
                response = client.responses.create(  # type: ignore
                    model=selected_model,
                    input=prompt,
                    tools=[
                        {
                            "type": "web_search_preview",
                            "search_context_size": search_context,
                        }
                    ] if enable_web_search else [],
                    tool_choice="auto",
                    parallel_tool_calls=True,
                    reasoning={"effort": reasoning},
                )
                content = getattr(response, 'output_text', None) or "No response text available."
            except Exception as e:
                return f"Error with o3 model: {str(e)}"
        else:
            # For other models, simulate web search through prompting
            if enable_web_search:
                messages[0]["content"] += (
                    " When answering, consider that you should provide up-to-date information "
                    "as if you had access to current web search results. Be clear about what "
                    "information might need verification with actual current sources."
                )

            # Only add temperature/top_p for models that support them
            # Skip temperature/top_p for certain models that don't support them
            unsupported_models = [
                "-search-preview", "gpt-5", "gpt-4.1", "-audio-preview", 
                "-realtime-preview", "-transcribe", "-tts", "gpt-image-1"
            ]
            if not any(unsupported in selected_model for unsupported in unsupported_models):
                # Adjust parameters based on reasoning effort
                if reasoning == "high":
                    extra_params["temperature"] = 0.3
                    extra_params["top_p"] = 0.9
                elif reasoning == "low":
                    extra_params["temperature"] = 0.9
                    extra_params["top_p"] = 1.0
                else:  # medium
                    extra_params["temperature"] = 0.7
                    extra_params["top_p"] = 0.95

            response = client.chat.completions.create(
                model=selected_model,
                messages=messages,  # type: ignore
                **extra_params
            )

            content = getattr(response.choices[0].message, 'content', None) or "No response available."

        # Add model information to the response
        result = f"**Model Used:** {selected_model}\n\n{content}"
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
    print(f"  Search context size: {config['search_context_size']}")
    print(f"  Reasoning effort: {config['reasoning_effort']}")

    # Run the server
    mcp_server.run()


if __name__ == "__main__":
    main()
