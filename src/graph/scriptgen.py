from langchain_nvidia_ai_endpoints import ChatNVIDIA
from dotenv import load_dotenv
from pathlib import Path
from langchain_core import prompts
from .systemprompt import SCRIPT_PROMPT
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage

load_dotenv(dotenv_path=Path("../.env"))
from langchain_core.messages import ToolMessage
from langchain_core.prompts import ChatPromptTemplate
import re


def stripfence(md: str) -> str:
    return re.sub(r"^```[^\n]*\n|```$", "", md, flags=re.MULTILINE)


class ScriptGen:
    def __init__(
        self,
        llm: BaseChatModel,
    ):
        self.llm = llm
        self.qa_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", SCRIPT_PROMPT),
                ("human", "{input}"),
            ]
        )

    async def run(self, input_text: str):
        request = self.qa_prompt.invoke({"input": input_text})
        response = self.llm.invoke(request)

        return stripfence(response.content)  # type: ignore
