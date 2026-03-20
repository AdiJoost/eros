from autogen import GroupChat, GroupChatManager, UserProxyAgent
from autogen.opentelemetry import instrument_agent, instrument_llm_wrapper
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import \
    OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (BatchSpanProcessor,
                                            ConsoleSpanExporter,
                                            SimpleSpanProcessor)

from src.llm.agents.creative_bot import CreativeBot
from src.llm.agents.internet_searcher import InternetSearcher
from src.llm.agents.planner import PlannerAgent
from src.llm.agents.validator_bot import ValidatorBot
from src.llm.gates.ollama_gate import OllamaGateFactory
from src.utilities.telemetry.telemetry import Telemetry
from src.utilities.telemetry.trace_provider import TraceProvider

def generate_date():
    tracer_provider = TraceProvider.set_trace_provider()
    Telemetry.setup(tracer_provider=tracer_provider, capture_messages=True)
    
    ollama_config = OllamaGateFactory(
        model_name="llama3.1:8b"
    ).build()

    creative_agent = CreativeBot(
        llm_config=ollama_config,
        name="CreativeBot1",
        tracer_provider=tracer_provider
    ).build()

    validatorbot = ValidatorBot(
        llm_config=ollama_config,
        name="ValidatorBot",
        tracer_provider=tracer_provider
    ).build()

    internet_searcher_agent = InternetSearcher(
        llm_config=ollama_config,
        name="InternetBot",
        tracer_provider=tracer_provider
    ).build()

    user_proxy = UserProxyAgent(
        name="user",
        human_input_mode="ALWAYS",
        max_consecutive_auto_reply=5,
    )

    planner = PlannerAgent(
        llm_config=ollama_config,
        agent_names= ["CreativeBot1", "ValidatorBot", "user", "InternetBot"],
        name="PlannerBot",
        tracer_provider=tracer_provider
    )

    groupchat = GroupChat(
    agents=[validatorbot, internet_searcher_agent, creative_agent, user_proxy],
    messages=[],
    max_round=20,
    speaker_selection_method=planner.planner_selection,
    )
    manager = GroupChatManager(groupchat=groupchat, llm_config=ollama_config)

    user_proxy.initiate_chat(
        manager,
        message="Im with my girlfriend in Chur from Monday evening until tuesday evening. We can sleep at my flat."
    )
