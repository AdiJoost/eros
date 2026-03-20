from typing import List
import random

from autogen import AssistantAgent, LLMConfig
from autogen.opentelemetry import instrument_agent


class PlannerAgent():

    DEFAULT_SYSTEM_MESSAGE="""
        You are a planner that orchestrates a group of agents.
        Available agents:
        - validatorbot: validates input and asks clarifying questions
        - user: answers questions
        - creative_agent: creates activity ideas
        - internet_searcher_agent: provides real-world info
        At each step, choose EXACTLY one next speaker by name.
        Focus on the validation happening at the start but quickly move over to let the creative_agent and internet_searcher_agent work together
        Only the internet_searcher is allowed to use tools
        """
    
    DEFAULT_DESCRIPTION="""
    The Planner is responsible for choosing the next agent to speak.
    """

    ENFORCE_OUTPUT ="""
        Only output the name of the next agent to speak.
        Valid options: $
        Do NOT explain.
        """

    def __init__(self, llm_config: LLMConfig, agent_names: List[str], name: str=None, system_message: str=None, tracer_provider=None, description: str= None):
        self.llm_config = llm_config
        self._agent_names = agent_names
        self._system_message= system_message if system_message else self.DEFAULT_SYSTEM_MESSAGE
        self._name = name if name else str(self.__class__)
        self._tracer_provider = tracer_provider
        self._description = description if description else self.DEFAULT_DESCRIPTION
        self._guardrail = self.ENFORCE_OUTPUT.replace("$", ", ".join(name for name in agent_names))
        print(self._guardrail)
        self._assistant = self.build()

    def build(self) -> AssistantAgent:
        planner = AssistantAgent(
            name=self._name,
            system_message=self._system_message,
            llm_config=self.llm_config,
            description=self._description
        )
        if self._tracer_provider:
            instrument_agent(planner, tracer_provider=self._tracer_provider)
        return planner
    
    def planner_selection(self, last_speaker, groupchat):
        messages = groupchat.messages.copy()
        messages.append({
            "role": "system",
            "content": self._guardrail
        })
        response = self._assistant.generate_reply(
            messages=messages,
            sender=None
        )
        if isinstance(response, dict):
            next_speaker_name = response.get("content", "").strip().lower()
        else:
            next_speaker_name = str(response).strip().lower()

        for agent in groupchat.agents:
            if agent.name.strip().lower() == next_speaker_name:
                return agent
        return random.choice(groupchat.agents)