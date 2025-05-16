from langchain_community.llms import Ollama
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.agents import initialize_agent, AgentType

llm = Ollama(model="llama2", base_url="http://localhost:11434")
search_tool = DuckDuckGoSearchRun()

agent = initialize_agent(
    tools=[search_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True,
    agent_kwargs={
        "system_message": (
            "You are a helpful assistant. "
            "Always use this format:\n"
            "Action: <action name>\n"
            "Action Input: <input>\n"
            "Observation: <observation>\n"
            "Thought: <your reasoning>\n"
            "Final Answer: <your answer>\n"
            "If you know the answer, respond with Final Answer only."
        )
    }
)

response = agent.run("What are the latest trends in software engineering?")
print(response)
