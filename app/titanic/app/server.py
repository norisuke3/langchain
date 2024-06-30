from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from langserve import add_routes
from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain_openai import ChatOpenAI, OpenAI
import getpass
import os

if os.environ["LANGCHAIN_API_KEY"] == "":
    print("enter LANGCHAIN_API_KEY:")
    os.environ["LANGCHAIN_API_KEY"] = getpass.getpass()
    os.environ["LANGCHAIN_TRACING_V2"] = "true"

if os.environ["OPENAI_API_KEY"] == "":
    print("enter OPENAI_API_KEY:")
    os.environ["OPENAI_API_KEY"] = getpass.getpass()

app = FastAPI()


@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")

# Define an agent
agent = create_csv_agent(
    ChatOpenAI(model="gpt-4", temperature=0),  # "gpt-4" モデルを指定
    "titanic.csv",
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    allow_dangerous_code=True  # ここで直接指定
)

add_routes(
    app,
    agent,
    path="/chain",
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
