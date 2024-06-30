from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain_anthropic.experimental import ChatAnthropic
from langserve import add_routes
from langchain_core.runnables import ConfigurableField

app = FastAPI()



@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")


openai = ChatOpenAI(model="gpt-4o").configurable_fields(
    temperature=ConfigurableField(
        id="llm_temperature",
        name="LLM Temperature",
        description="The temperature of the LLM",
    )
)

add_routes(
    app,
    openai,
    path="/openai",
)

add_routes(
    app,
    ChatAnthropic(model="claude-3-haiku-20240307"),
    path="/anthropic",
)

model = ChatAnthropic(model="claude-3-haiku-20240307")
prompt = ChatPromptTemplate.from_template("tell me a joke about {topic}")
add_routes(
    app,
    prompt | model,
    playground_type="chat",
    path="/joke",
)

# #
# # Chat playground
# #
# from langchain_core.prompts import MessagesPlaceholder
# from langchain_core.base_models import BaseModel

# prompt = ChatPromptTemplate.from_messages(
#     [
#         ("system", "You are a helpful, professional assistant named Cob."),
#         MessagesPlaceholder(variable_name="messages"),
#     ]
# )

# chain = prompt | ChatOpenAI(model="gpt-4o")


# class InputChat(BaseModel):
#     """Input for the chat endpoint."""

#     messages: List[Union[HumanMessage, AIMessage, SystemMessage]] = Field(
#         ...,
#         description="The chat messages representing the current conversation.",
#     )


# add_routes(
#     app,
#     chain.with_types(input_type=InputChat),
#     enable_feedback_endpoint=True,
#     enable_public_trace_link_endpoint=True,
#     playground_type="chat",
#     path="/chat"
# )

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
