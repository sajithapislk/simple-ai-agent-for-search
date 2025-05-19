from langchain_community.llms import Ollama
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.agents import initialize_agent, AgentType
import logging
from app.config import Config  # Add this import

logger = logging.getLogger(__name__)

class AIAgent:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AIAgent, cls).__new__(cls)
            cls._instance._initialize_agent()
        return cls._instance
    
    def _initialize_agent(self):
        try:
            logger.info("Initializing AI Agent...")
            llm = Ollama(
                model=Config.OLLAMA_MODEL,
                base_url=Config.OLLAMA_BASE_URL,
                temperature=0.7 
            )
            search_tool = DuckDuckGoSearchRun()

            self.agent = initialize_agent(
                tools=[search_tool],
                llm=llm,
                agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                verbose=True,
                handle_parsing_errors=True,
                max_iterations=10,  # Increased from default 5
                max_execution_time=60,  # 60 seconds timeout
                early_stopping_method="generate",  # Better stopping condition
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
            logger.info("AI Agent initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize AI Agent: {str(e)}")
            raise
    
    def ask(self, question: str) -> str:
        try:
            logger.info(f"Processing question: {question}")
            response = self.agent.run(question)
            logger.info(f"Response generated for question: {question}")
            return response
        except Exception as e:
            logger.error(f"Error processing question: {str(e)}")
            raise