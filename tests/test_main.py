import json
import pytest
import asyncio
import os
from fastmcp import Client
from conftest import PORT

HOST = "localhost"
PATH = "/mcp"


@pytest.fixture(scope="module")
def mcp_client():

    base_url = f"http://{HOST}:{PORT}{PATH}"
    client = Client(base_url)

    try:
        yield client
    finally:
        if hasattr(client, "close") and callable(client.close):
            asyncio.run(client.close())


@pytest.mark.asyncio
async def test_client_Connection(mcp_client):
    """Test the generate_script tool using the FastMCP client."""
    async with mcp_client:
        await mcp_client.ping()

    async with mcp_client:
        tools = await mcp_client.list_tools()

    assert len(tools) > 0
    assert any(tool.name is not None or "" for tool in tools)
    assert any(tool.description is not None or "" for tool in tools)


@pytest.mark.asyncio
async def test_generate_script_with_error(mcp_client):
    async with mcp_client:
        result = await mcp_client.call_tool(
            "generate_script", {"prompt": "Generate code with an undefined variable"}
        )
    content = json.loads(result[0].text)
    assert content["python_script"] is not None
    assert content["error"] is not None
    assert content["script_result"] is None


@pytest.mark.asyncio
async def test_generate_script_data_analysis(mcp_client):
    async with mcp_client:
        result = await mcp_client.call_tool(
            "generate_script",
            {
                "prompt": "Create a list of the first 5 Fibonacci numbers and calculate their sum"
            },
        )

    content = json.loads(result[0].text)
    assert content["python_script"] is not None
    assert content["error"] is None
    assert content["script_result"] is not None
