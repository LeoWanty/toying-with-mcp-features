from dataclasses import dataclass
from typing import Literal

from fastmcp import FastMCP, Context
from fastmcp.exceptions import ToolError
from fastmcp.server.middleware import Middleware, MiddlewareContext

class PrivacyMiddleware(Middleware):

    async def on_call_tool(self, context: MiddlewareContext, call_next):
        tool_name = context.message.name
        tool = await context.fastmcp_context.fastmcp.get_tool(tool_name)
        if "private" in tool.tags:
            raise ToolError(f"Access denied to private tool: {tool_name}")
        # return the tool result only since it is not private!
        return await call_next(context)

mcp = FastMCP(name="test MCP features")


@dataclass
class StructuredInput:
    name: str
    age: int
    choices: Literal["low", "medium", "high"]
    accept: bool


@mcp.tool
async def does_sampling_work(ctx: Context):
    """
    Performs a sampling query.

    Returns:
        Any: The result of the sampling operation.
    """
    return await ctx.sample(
        "Does the MCP sampling work?",
        system_prompt="You're an assistant that answers questions after saying HEYYY BUDDY!",
    )


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
    
@mcp.tool(tags={"private"})
def  does_privacy_middleware_work():
    return "This is a private function!"

@mcp.tool()
async def does_hello_world_work():
    return "Hello World!"
    
mcp.add_middleware(PrivacyMiddleware())

if __name__ == "__main__":
    mcp.run()
