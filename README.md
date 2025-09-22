# Toying with MCP features

This project is a playground for experimenting and testing MCP features.

## Installation

To install the project and its dependencies, run the following commands:

```bash
uv sync
pip install -e .
```

## Usage

To run the server, execute the following command from the root of the repository:

```bash
python src/toying_with_mcp_features/server.py
```

The server will start and listen for requests on `stdio`.

## Dev mode

To run the server in dev mode:
```bash
fastmcp dev src/toying_with_mcp_features/server.py
```
