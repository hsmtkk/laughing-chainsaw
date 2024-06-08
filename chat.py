from langchain import hub
from langchain_openai import OpenAI
from langchain.agents import AgentExecutor, create_react_agent
import oreilly
from langchain.tools import tool


@tool
def search_oreilly(query: str) -> str:
    """Search O'Reilly books"""
    print(f"search_oreilly {query}")
    params = oreilly.SearchParams(
        query=query, sort=oreilly.Sort.relevance, order=oreilly.Order.desc
    )
    print(params)
    return oreilly.search(params).model_dump_json()


def main():
    llm = OpenAI(verbose=True)
    tools = [search_oreilly]
    prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm, tools, prompt)
    ex = AgentExecutor(agent=agent, tools=tools, verbose=True)
    while True:
        you = input("You > ")
        ai = ex.invoke({"input": you})
        print(ai)


if __name__ == "__main__":
    main()
