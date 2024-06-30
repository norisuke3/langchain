import asyncio
from langchain.schema import SystemMessage, HumanMessage
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnableMap
from langserve import RemoteRunnable

openai = RemoteRunnable("http://localhost:8000/openai/")
anthropic = RemoteRunnable("http://localhost:8000/anthropic/")
joke_chain = RemoteRunnable("http://localhost:8000/joke/")

async def main():
    # 同期的な呼び出し
    result = joke_chain.invoke({"topic": "parrots"})
    print(result)

    # 非同期的な呼び出し
    result = await joke_chain.ainvoke({"topic": "parrots"})
    print(result)

    prompt = [
        SystemMessage(content='Act like either a cat or a parrot.'),
        HumanMessage(content='Hello!')
    ]

    # 非同期ストリームの処理
    async for msg in anthropic.astream(prompt):
        print(msg, end="", flush=True)

    prompt_template = ChatPromptTemplate.from_messages(
        [("system", "Tell me a long story about {topic}")]
    )

    # カスタムチェーンの定義
    chain = prompt_template | RunnableMap({
        "openai": openai,
        "anthropic": anthropic,
    })

    # バッチ処理
    results = chain.batch([{"topic": "parrots"}, {"topic": "cats"}])
    print(results)

# メイン関数を実行
asyncio.run(main())
