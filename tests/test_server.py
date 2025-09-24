import logging
from typing import Literal, get_origin, get_args

import lmstudio
import pytest
from fastmcp.client import Client
from fastmcp.client.sampling import (
    SamplingMessage,
    SamplingParams,
    RequestContext,
)

from toying_with_mcp_features.server import mcp


def input_given_type(expected_type, message_prefix: str | None = None):
    if message_prefix is None:
        message_prefix = ""

    if expected_type is bool:
        message = "Accept or reject (Y/N) : "
        user_input = input(message_prefix + message)
        if user_input.upper().strip() == "Y":
            return True
        elif user_input.upper().strip() == "N":
            return False
        else:
            raise ValueError("Invalid input. Please enter Y or N.")
    elif expected_type in [str, int, float]:
        message = f"Enter a value of type {expected_type} : "
        user_input = input(message_prefix + message)
        return expected_type(user_input)
    elif get_origin(expected_type) is Literal:
        message = f"Select a value from {get_args(expected_type)} : "
        return input(message_prefix + message)
    elif expected_type is dict:
        return input_given_properties(expected_type)
    else:
        raise NotImplementedError(f"type {expected_type} not supported yet.")


def input_given_properties(properties: dict):
    return {
        prop_name: input_given_type(prop, f"For {prop_name} : ")
        for prop_name, prop in properties.items()
    }

async def elicitation_handler(
        message: str,
        response_type: type,
        params,
        context,
):
    logging.warning(f"Elicitation handler called with message: {message}")
    # Present the message to the user and collect input
    if response_type is None:
        user_input = None
    else:
        properties = response_type.__dict__["__annotations__"]
        user_input = input_given_properties(properties)


    # Create response using the provided dataclass type
    if response_type is None:
        return None
    else:
        return user_input


async def sampling_handler(
    messages: list[SamplingMessage],
    params: SamplingParams,
    context: RequestContext
) -> str:
    llm = lmstudio.llm("openai/gpt-oss-20b")
    logging.warning(f"Sampling handler operation with message: {messages}")
    message = "\n\n".join(
        [
            f"Message {i}:\n{m.content.text}"
            for i, m in enumerate(messages)
        ]
    )

    response = llm.respond(message)
    logging.warning(f"LLM response: {response.content}")
    return response.content


client = Client(
    mcp,
    elicitation_handler=elicitation_handler,
    sampling_handler=sampling_handler,
)

@pytest.mark.skip(reason="Legacy test, covered by new tests in test_mcp_features.py")
@pytest.mark.asyncio
async def test_logging_feature():
    async with client:
        await client.call_tool("does_logging_work")


@pytest.mark.skip(reason="Legacy test, covered by new tests in test_mcp_features.py")
@pytest.mark.parametrize("type", ["None", "str", "int", "Literal", "structured"])
@pytest.mark.asyncio
async def test_ellicit_feature(type):
    async with client:
        return await client.call_tool("does_ellicit_work", {"type": type})


@pytest.mark.skip(reason="Legacy test, covered by new tests in test_mcp_features.py")
@pytest.mark.asyncio
async def test_sampling_feature():
    async with client:
        await client.call_tool("does_sampling_work")

async def main():
    async with client:
        # Basic server interaction
        await client.ping()

        # # List available operations
        tools = await client.list_tools()
        resources = await client.list_resources()
        prompts = await client.list_prompts()
        logging.warning(tools)
        logging.warning(resources)
        logging.warning(prompts)


        # Execute features
        logging_result = await client.call_tool("does_logging_work")
        logging.warning(logging_result)

        # for type in ["None", "str", "int", "Literal", "structured"]:
        #     logging.warning(f">>> Testing ellicitation feature with type: {type}")
        #     ellicit_result = await client.call_tool("does_ellicit_work", {"type": type})
        #     logging.warning(ellicit_result)

        sampling_result = await client.call_tool("does_sampling_work")
        logging.warning(sampling_result)
