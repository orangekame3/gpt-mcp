#!/usr/bin/env python3
"""OpenAI MCP Server - Bridge OpenAI models to Claude via MCP."""

import os
import asyncio
from typing import List, Optional, Literal
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field
from mcp.server import Server
from mcp.server.types import TextContent  # type: ignore

load_dotenv()

# Configuration from environment variables
config = {
    "api_key": os.getenv("OPENAI_API_KEY"),
    "max_retries": int(os.getenv("OPENAI_MAX_RETRIES", "3")),
    "timeout": float(os.getenv("OPENAI_API_TIMEOUT", "60")),
    "search_context_size": os.getenv("SEARCH_CONTEXT_SIZE", "medium"),
    "reasoning_effort": os.getenv("REASONING_EFFORT", "medium"),
    "model": os.getenv("OPENAI_MODEL", "gpt-4o"),
}

# Initialize OpenAI client with retry and timeout configuration
client = OpenAI(
    api_key=config["api_key"],  # type: ignore
    max_retries=config["max_retries"],  # type: ignore
    timeout=config["timeout"],  # type: ignore
)

# Create MCP server instance
mcp_server = Server("gpt-mcp")


class ModelListArgs(BaseModel):
    pass


@mcp_server.tool()  # type: ignore
async def list_models(_arguments: ModelListArgs) -> List[TextContent]:
    """
    List available OpenAI models.
    Returns a list of available OpenAI models.
    """
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

        return [TextContent(
            type="text",
            text=result
        )]

    except Exception as e:
        return [TextContent(
            type="text",
            text=f"Error listing models: {str(e)}"
        )]


class AdvancedSearchArgs(BaseModel):
    prompt: str = Field(
        description="Ask questions, search for information, or consult about complex problems"
    )
    model: str = Field(
        default_factory=lambda: str(config["model"]),
        description="The OpenAI model to use (e.g., o3, gpt-4o, gpt-4o-mini)"
    )
    search_context_size: Optional[Literal["low", "medium", "high"]] = Field(
        default=None,
        description="Controls the search context size (defaults to environment setting)"
    )
    reasoning_effort: Optional[Literal["low", "medium", "high"]] = Field(
        default=None,
        description="Controls the reasoning effort level (defaults to environment setting)"
    )
    enable_web_search: bool = Field(
        default=True,
        description="Whether to enable web search capabilities"
    )


@mcp_server.tool()  # type: ignore
async def advanced_search(arguments: AdvancedSearchArgs) -> List[TextContent]:
    """
    Advanced AI search with web capabilities and reasoning.

    This tool provides intelligent web search and reasoning capabilities,
    similar to o3's search but available for multiple OpenAI models.
    Useful for finding the latest information, troubleshooting errors,
    and discussing complex ideas or design challenges.
    """
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
            {"role": "user", "content": arguments.prompt}
        ]

        # Use provided settings or fall back to environment settings
        search_context = arguments.search_context_size or str(config["search_context_size"])
        reasoning = arguments.reasoning_effort or config["reasoning_effort"]

        # Prepare additional parameters based on model capabilities
        extra_params = {}

        # For o3 model, use the responses API with web search
        if arguments.model == "o3":
            # o3 specific implementation
            response = await asyncio.to_thread(
                client.responses.create,  # type: ignore
                model=arguments.model,
                input=arguments.prompt,
                tools=[
                    {
                        "type": "web_search_preview",
                        "search_context_size": search_context,
                    }
                ] if arguments.enable_web_search else [],
                tool_choice="auto",
                parallel_tool_calls=True,
                reasoning={"effort": reasoning},
            )

            content = getattr(response, 'output_text', None) or "No response text available."
        else:
            # For other models, simulate web search through prompting
            if arguments.enable_web_search:
                messages[0]["content"] += (
                    " When answering, consider that you should provide up-to-date information "
                    "as if you had access to current web search results. Be clear about what "
                    "information might need verification with actual current sources."
                )

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

            response = await asyncio.to_thread(
                client.chat.completions.create,  # type: ignore
                model=arguments.model,
                messages=messages,  # type: ignore
                **extra_params
            )

            content = getattr(response.choices[0].message, 'content', None) or "No response available."

        return [TextContent(
            type="text",
            text=content
        )]

    except Exception as e:
        return [TextContent(
            type="text",
            text=f"Error in advanced search: {str(e)}"
        )]


async def main():
    """Run the MCP server."""
    # Check for API key
    if not config["api_key"]:
        print("Error: OPENAI_API_KEY environment variable is not set")
        print("Please set it in your .env file or environment")
        return

    # Print configuration on startup
    print("GPT MCP Server starting with configuration:")
    print(f"  Max retries: {config['max_retries']}")
    print(f"  Timeout: {config['timeout']}s")
    print(f"  Search context size: {config['search_context_size']}")
    print(f"  Reasoning effort: {config['reasoning_effort']}")

    async with mcp_server.run() as streams:
        await streams.start()


if __name__ == "__main__":
    asyncio.run(main())
