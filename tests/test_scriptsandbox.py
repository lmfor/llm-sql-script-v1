import pytest
from graph.scriptsandbox import ScriptSandbox

class DummyContent:
    def __init__(self, text):
        self.text = text

class DummyResponse:
    def __init__(self, text):
        self.content = [DummyContent(text)]


def test_parse_mcp_response_output():
    sandbox = ScriptSandbox()
    xml = '<output>42</output><error></error>'
    resp = DummyResponse(xml)
    result = sandbox._parse_mcp_response(resp)
    assert result['script_result'] == '42'
    assert result['error'] == '' or result['error'] is None


def test_parse_mcp_response_error():
    sandbox = ScriptSandbox()
    xml = '<output></output><error>Some error</error>'
    resp = DummyResponse(xml)
    result = sandbox._parse_mcp_response(resp)
    assert result['script_result'] == '' or result['script_result'] is None
    assert result['error'] == 'Some error'


