# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2025-01-08

### Added
- Advanced search tool with web capabilities and reasoning, inspired by o3-search-mcp
- Support for all OpenAI models (o3, GPT-4o, GPT-4o-mini, etc.)
- Configurable search context size (low/medium/high)
- Configurable reasoning effort levels
- Environment variable configuration for timeouts and retries
- Native o3 web search support when using o3 model
- Intelligent prompting for web search simulation on other models

### Features
- Chat completions with all OpenAI chat models
- Text completion with instruction-following models
- Image generation with DALL-E 2 and DALL-E 3
- Model listing functionality
- Robust error handling with configurable retries

[Unreleased]: https://github.com/orangekame3/gpt-mcp/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/orangekame3/gpt-mcp/releases/tag/v0.1.0