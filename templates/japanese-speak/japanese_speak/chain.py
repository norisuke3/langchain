from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Translate user input into Japanese",
        ),
        ("human", "{text}"),
    ]
)
_model = ChatOpenAI(model='gpt-4o')

# if you update this, you MUST also update ../pyproject.toml
# with the new `tool.langserve.export_attr`
chain = _prompt | _model
