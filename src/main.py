from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import PlainTextResponse
import asyncio
from workflow import AnalysisWorkflow
from graph.scriptsandbox import ScriptSandbox

mcp = FastMCP(
    "datagenie",
    instructions="""
        This server provides data analysis tools.
        Call generate_script() to generate a script and run Python for collecting results.
        """,
)


@mcp.tool(
    name="generate_script",
    description="Generate Python script from a natural language prompt and run it in a sandbox environment, return the script result",
)
async def generate_script(prompt: str) -> dict:
    workflow = AnalysisWorkflow()
    result = await workflow.run(prompt)
    return result


@mcp.custom_route("/health", methods=["GET"])
async def health_check(request: Request) -> PlainTextResponse:
    return PlainTextResponse("OK")


async def main():
    await ScriptSandbox.warmup()
    await mcp.run_streamable_http_async()


if __name__ == "__main__":
    asyncio.run(main())
