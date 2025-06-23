from langchain_nvidia_ai_endpoints import ChatNVIDIA
from dotenv import dotenv_values
from pathlib import Path
from typing import Any, Dict
from langgraph.graph import END, START, StateGraph
from graph.scriptsandbox import ScriptSandbox
from graph.scriptgen import ScriptGen
import logging
from graph.state import SandboxState
from langgraph.graph.state import CompiledStateGraph
from mcp.server.fastmcp import FastMCP

logging.basicConfig(level=logging.DEBUG)

config = dotenv_values(Path(".env"))

logger = logging.getLogger(__name__)


class DATAGENIE:
    def __init__(
        self,
    ):
        self.llm = ChatNVIDIA(
            model=config["LLM_NAME"],
            base_url=config["LLM_URL"],
            max_tokens=config["MAX_TOKENS"],
        )
        self.sandbox = config["SANDBOX_SSE"]
        self.ScriptGen = ScriptGen(llm=self.llm)
        self.ScriptRunner = ScriptSandbox()
        self.graph = self._create_graph()

    async def _generate_script(self, state: SandboxState) -> Dict[str, Any]:
        logger.debug("===== <light-blue>Generating Script</> =====")
        response = await self.ScriptGen.run(state.input)
        return {"python_script": response}

    async def _run_script(self, state: SandboxState) -> Dict[str, Any]:
        logger.debug("===== <light-blue>Running Script</> =====")
        response = await self.ScriptRunner.run(state.python_script)
        return response

    def _create_graph(self) -> CompiledStateGraph:
        workflow = StateGraph(SandboxState)
        workflow.add_node("gen script", self._generate_script)
        workflow.add_node("run script", self._run_script)

        workflow.add_edge(START, "gen script")
        workflow.add_edge("gen script", "run script")
        workflow.add_edge("run script", END)

        return workflow.compile()


mcp = FastMCP("datagenie", version="0.1.0")

@mcp.tool(
    name="generate_script", description="Generate Python script from a natural language prompt and run it in a sandbox environment, return the result"
)
async def generate_script(prompt: str) -> dict:
    datagenie = DATAGENIE()
    result = await datagenie.graph.ainvoke(SandboxState(input=prompt))
    return result