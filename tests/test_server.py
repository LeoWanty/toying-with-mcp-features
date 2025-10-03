import asyncio

import pytest
from fastmcp.client import Client
from fastmcp.exceptions import ToolError

from toying_with_mcp_features import server


@pytest.mark.asyncio
async def test_hello_world():
    """
    Tests that the 'does_hello_world_work' tool returns the correct string.
    """
    async with Client(server.mcp) as client:
        result = await client.call_tool("does_hello_world_work")
        assert result.content[0].text == "Hello World!"


@pytest.mark.asyncio
async def test_does_logging_work_sends_logs_to_client():
    """
    Tests that ctx.log calls from a tool are sent to the client's
    log_handler.
    """
    # A list to store log messages received by our handler
    received_logs = []

    # A mock async handler to append messages to our list
    async def mock_log_handler(log_message):
        received_logs.append(log_message)

    # Initialize the client with our mock handler
    async with Client(server.mcp, log_handler=mock_log_handler) as client:
        await client.call_tool("does_logging_work")

    # Check that we received the logs.
    # The number of logs can vary depending on internal fastmcp logging,
    # so we'll check for the specific logs we care about.
    log_set = {(log.level.upper(), log.data["msg"]) for log in received_logs}

    expected_logs = {
        ("DEBUG", "This is a test debug message."),
        ("INFO", "This is a test info message."),
        ("WARNING", "This is a test warning message."),
        ("ERROR", "This is a test error message."),
    }

    assert expected_logs.issubset(log_set)


@pytest.mark.asyncio
async def test_does_sampling_work_uses_handler():
    """
    Tests that ctx.sample calls are sent to the client's sampling_handler
    and that the tool returns the handler's response.
    """
    import asyncio

    handler_response = "The sampling works!"
    handler_was_called = asyncio.Event()

    async def mock_sampling_handler(messages, params, context):
        assert len(messages) == 1
        assert messages[0].role == "user"
        assert messages[0].content.text == "Does the MCP sampling work?"
        handler_was_called.set()
        return handler_response

    async with Client(server.mcp, sampling_handler=mock_sampling_handler) as client:
        result = await client.call_tool("does_sampling_work")

    assert handler_was_called.is_set()
    assert result.content[0].text == handler_response


@pytest.mark.parametrize(
    "test_type, mock_response, expected_str_response",
    [
        ("None", None, "action='accept' data={}"),
        (
            "str",
            {"value": "test string"},
            "action='accept' data='test string'",
        ),
        ("int", {"value": 123}, "action='accept' data=123"),
        (
            "Literal",
            {"value": "medium"},
            "action='accept' data='medium'",
        ),
        (
            "structured",
            {"name": "test", "age": 99, "choices": "high", "accept": True},
            "action='accept' data=StructuredInput(name='test', age=99, choices='high', accept=True)",
        ),
    ],
)
@pytest.mark.asyncio
async def test_does_ellicit_work(test_type, mock_response, expected_str_response):
    """
    Tests that ctx.elicit calls are sent to the client's elicitation_handler
    and that the tool returns the handler's response.
    """
    handler_was_called = asyncio.Event()

    async def mock_elicitation_handler(message, response_type, params, context):
        assert message == f"Does ellicit work with type {test_type} ?"
        handler_was_called.set()
        return mock_response

    async with Client(
        server.mcp, elicitation_handler=mock_elicitation_handler
    ) as client:
        result = await client.call_tool("does_ellicit_work", {"type": test_type})

    assert handler_was_called.is_set()
    expected_return = (
        f"Ellicit works with type {test_type} and returns {expected_str_response}"
    )
    assert result.content[0].text == expected_return
    
    
@pytest.mark.asyncio
async def test_does_middleware_work():
    async with Client(server.mcp) as client:
        with pytest.raises(ToolError) as exc_info:
            await client.call_tool("does_privacy_middleware_work", {})
        assert "Access denied to private tool: does_privacy_middleware_work" in str(exc_info.value)

