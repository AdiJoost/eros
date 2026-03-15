from autogen import ConversableAgent, LLMConfig


class CreativeBot:

    DEFAULT_SYSTEM_MESSAGE="""
    You are an helpful assistant that is tasked with comming up with some date ideas.
    """

    def __init__(self, llm_config: LLMConfig, name: str=None, system_message: str=None):
        self.llm_config = llm_config
        self._system_message= system_message if system_message else self.DEFAULT_SYSTEM_MESSAGE
        self._name = name if name else str(self.__class__)

    def build(self) -> ConversableAgent:
        return ConversableAgent(
            name=self._name,
            system_message=self._system_message,
            llm_config=self.llm_config
        )