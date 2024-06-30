from langchain.tools import tool

@tool
def _search(input: str) -> str:
    """like a gorilla!!."""
    return f"Ooh ooh! {input}"


# if you update this, you MUST also update ../pyproject.toml
# with the new `tool.langserve.export_attr`
chain = _search
