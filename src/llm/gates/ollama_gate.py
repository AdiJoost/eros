import os

from autogen import LLMConfig


class OllamaGateFactory():

    def __init__(self, model_name: str, stream: bool = False):
        self.ollama_host = os.environ["OLLAMA_HOST"]
        self.model_name = model_name
        self.stream = stream

    def build(self) -> LLMConfig:
        return LLMConfig({
            "model": self.model_name,
            "api_type": "ollama",
            "stream": self.stream,
            "client_host": self.ollama_host
        })