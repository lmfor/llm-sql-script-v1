# server.py
import asyncio
import re
import subprocess
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.types import CallToolResult


def stripfence(md: str) -> str:
    return re.sub(r"^```[^\n]*\n|```$", "", md, flags=re.MULTILINE)


class ScriptSandbox:
    def __init__(self):
        self.server_params = StdioServerParameters(
            command="deno",
            args=[
                "run",
                "--allow-net",
                "--allow-read=node_modules",
                "--allow-write=node_modules",
                "--node-modules-dir=true",
                "jsr:@pydantic/mcp-run-python",
                "stdio",
            ],
        )

    @staticmethod
    async def warmup():
        cmd = [
            "deno",
            "run",
            "--allow-net",
            "--allow-read=node_modules",
            "--allow-write=node_modules",
            "--node-modules-dir=true",
            "jsr:@pydantic/mcp-run-python",
            "warmup",
        ]
        subprocess.run(
            cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )

    def _parse_mcp_response(self, response: CallToolResult) -> dict:
        xml = response.content[0].text
        error_match = re.search(r"<error>(.*?)</error>", xml, re.DOTALL)
        output_match = re.search(r"<output>(.*?)</output>", xml, re.DOTALL)
        error = error_match.group(1).strip() if error_match else None
        output = output_match.group(1).strip() if output_match else None
        return {"script_result": output, "error": error}

    async def run(self, script: str) -> dict:
        async with stdio_client(self.server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                res = await session.call_tool(
                    "run_python_code", {"python_code": script}
                )
        return self._parse_mcp_response(res)
