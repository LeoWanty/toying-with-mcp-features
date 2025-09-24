from dataclasses import dataclass
from typing import Literal

from fastmcp import FastMCP, Context

mcp = FastMCP(name="test MCP sampling")


@dataclass
class StructuredInput:
    name: str
    age: int
    choices: Literal["low", "medium", "high"]
    accept: bool


from fastmcp.client.sampling import SamplingMessage
from mcp.types import TextContent


@mcp.tool
async def does_sampling_work(ctx: Context):
    """
    Performs a sampling query.

    Returns:
        Any: The result of the sampling operation.
    """
    messages = [
        SamplingMessage(
            role="user",
            content=TextContent(type="text", text="Does the MCP sampling work?"),
        )
    ]
    return await ctx.sample(messages)


@mcp.tool
async def does_ellicit_work(ctx: Context, type: Literal["None", "str", "int", "Literal", "structured"]):
    """
    Performs a ellicit request and echo the result.

    Args:
        type: The type of the input to ellicit.
            None for accept/reject
            str for text input
            int for number input
            Litteral for a choice in a list
            structured for a structured input

    Returns:
        Any: The result of the sampling operation.
    """
    response_type = NotImplemented
    if type == "None":
        response_type = None
    elif type == "str":
        response_type = str
    elif type == "int":
        response_type = int
    elif type == "Literal":
        response_type = Literal["low", "medium", "high"]
    elif type == "structured":
        response_type = StructuredInput

    ellicit_response = await ctx.elicit(f"Does ellicit work with type {type} ?", response_type)
    return f"Ellicit works with type {type} and returns {ellicit_response}"

@mcp.tool
async def does_logging_work(ctx: Context):
    """
    Check if logging works as expected.

    Returns:
        Any: a message.
    """
    await ctx.debug("This is a test debug message.")
    await ctx.info("This is a test info message.")
    await ctx.warning("This is a test warning message.")
    await ctx.error("This is a test error message.")
    return "No error returned. Check the console to see test log messages"

@mcp.tool()
async def does_hello_world_work():
    return "Hello World!"

if __name__ == "__main__":
    mcp.run()