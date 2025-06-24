from fastmcp import FastMCP
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


async def main():
    await ScriptSandbox.warmup()
    await mcp.run_async(transport="streamable-http", host="0.0.0.0", port=8000)


if __name__ == "__main__":
    asyncio.run(main())
