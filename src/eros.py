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

    creative_agent_2 = CreativeBot(
        llm_config=ollama_config,
        name="CreativeBot2",
        tracer_provider=tracer_provider
    ).build()

    internet_searcher_agent = InternetSearcher(
        llm_config=ollama_config,
        tracer_provider=tracer_provider
    ).build()

    groupchat = GroupChat(
    agents=[creative_agent, creative_agent_2, internet_searcher_agent],
    messages=[],
    max_round=10,
    speaker_selection_method="auto",
    )
    manager = GroupChatManager(groupchat=groupchat, llm_config=ollama_config)

    user_proxy = UserProxyAgent(
        name="user",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=5,
    )
    user_proxy.initiate_chat(
        manager,
        message="Generate 3 thoughtful date ideas for Monday evening into Tuesday morning."
    )
