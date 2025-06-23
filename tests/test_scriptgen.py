import pytest
from graph.scriptgen import ScriptGen, stripfence


class DummyLLM:
    def invoke(self, prompt):
        class Response:
            content = '```python\nprint("abcd")\n```'

        return Response()


def test_stripfence():
    md = '```python\nprint("abcd")\n```'
    assert stripfence(md) == 'print("abcd")\n'


@pytest.mark.asyncio
async def test_scriptgen_run():
    llm = DummyLLM()
    sg = ScriptGen(llm=llm)
    result = await sg.run("fake input")
    assert result == 'print("abcd")\n'
