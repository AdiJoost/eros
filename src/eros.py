from autogen import UserProxyAgent

from src.llm.agents.creative_bot import CreativeBot
from src.llm.gates.ollama_gate import OllamaGateFactory


def generate_date():

    ollama_config = OllamaGateFactory(
        model_name="llama3.1:8b"
    ).build()

    creative_agent = CreativeBot(
        llm_config=ollama_config
    ).build()
    
    response = creative_agent.run(
        message="Please generate me 3 date ideas for a monday evening into the tuesday morning",
        max_turns=3,
        user_input=True
    )
    response.process()
