# server.py
import re
from mcp.server.fastmcp import FastMCP
from mcp import ClientSession
from mcp.client.sse import sse_client
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from dotenv import load_dotenv
from pathlib import Path
from langchain_core import prompts
from .systemprompt import PLOT_PROMPT

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage

load_dotenv(dotenv_path=Path("../.env"))
from langchain_core.messages import ToolMessage


def stripfence(md: str) -> str:
    return re.sub(r"^```[^\n]*\n|```$", "", md, flags=re.MULTILINE)


class PlotSandbox:
    def __init__(self, sandbox_sse: str):
        self.sandbox_sse = sandbox_sse

    async def run(self, script: str) -> ToolMessage:
        async with sse_client(self.sandbox_sse) as (r, w):  # type: ignore
            async with ClientSession(r, w) as session:
                await session.initialize()
                res = await session.call_tool(
                    "run_python_code", {"python_code": script}
                )

        if res.is_error:
            raise RuntimeError(f"Sandbox Error: {res.content}")

        xml = "".join(getattr(seg, "text", str(seg)) for seg in res.content)
        m = re.search(r'{"\s*image"\s*:\s*"([^"]+)"}', xml, re.I)

        if not m:
            raise ValueError(
                "Sandbox Error: Plot node triggered, but no image generated."
            )

        output = {
            "artifacts": {"type": "image", "base64_data": m.group(1)},
            "stderr": None,
            "stdout": res.content,
        }
        return output
