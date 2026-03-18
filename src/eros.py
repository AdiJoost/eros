from autogen import UserProxyAgent
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
        tracer_provider=tracer_provider
    ).build()
    
    response = creative_agent.run(
        message="Please generate me 3 date ideas for a monday evening into the tuesday morning",
        max_turns=3,
        user_input=True
    )
    response.process()
