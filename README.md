# Toying with MCP features

This project is a playground for experimenting and testing MCP features.

- The `src/toying_with_mcp_features_/server.py` contains the tool's dummy features
- The `test/test_server.py` proposes a `sampling_handler` and `elicitation_handler` for a local client with FastMCP

*Still TODO* : Creating dummies for pytest testing (not working for now)

## How to toy ?

Either with **MCP Inspector** (see bellow Dev Mode) or a **local MCP client** (start with copying the content of the `test_server.py`) in a notebook.

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
