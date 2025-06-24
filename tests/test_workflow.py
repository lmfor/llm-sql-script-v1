import pytest
from workflow import AnalysisWorkflow
from graph.state import SandboxState


@pytest.mark.asyncio
async def test_dataview_graph_basic():
    workflow = AnalysisWorkflow()
    initial_state = SandboxState(input="print 42")
    result = await workflow.graph.ainvoke(initial_state)
    assert isinstance(result, dict)
    assert result.get("error") is None
    assert "print" in result.get("python_script")
    assert result.get("script_result") == "42"


@pytest.mark.asyncio
async def test_dataview_graph_empty_input():
    workflow = AnalysisWorkflow()
    initial_state = SandboxState(
        input="give me fibonacci sequence starting from 0, end at 5"
    )
    result = await workflow.graph.ainvoke(initial_state)
    assert isinstance(result, dict)
    assert result.get("error") is None
    assert result.get("script_result") == "[0, 1, 1, 2, 3, 5]"


@pytest.mark.asyncio
async def test_dataview_graph_unicode_input():
    workflow = AnalysisWorkflow()
    initial_state = SandboxState(
        input="give me a buggy fib function in python, and casues a runtime error"
    )
    result = await workflow.graph.ainvoke(initial_state)
    assert isinstance(result, dict)
    assert result.get("error") is not None
    assert result.get("script_result") is None
