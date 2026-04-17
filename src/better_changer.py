from autogen import ConversableAgent, GroupChat, GroupChatManager

from src.llm.gates.ollama_gate import OllamaGateFactory
from mcp.client.streamable_http import streamable_http_client
from mcp import ClientSession
from autogen.mcp import create_toolkit

from src.utilities.telemetry.telemetry import Telemetry
from src.utilities.telemetry.trace_provider import TraceProvider

async def update_testcase(user_prompt: str):
    ollama_config = OllamaGateFactory(
            model_name="gemma4:31b"
        ).build()
    async with (streamable_http_client("http://127.0.0.1:8000/mcp") as (read, write, _), ClientSession(read, write) as session,):
        await session.initialize()
        tracer_provider = TraceProvider.set_trace_provider()
        Telemetry.setup(tracer_provider=tracer_provider, capture_messages=True)
        toolkit = await create_toolkit(session=session)

        planner = ConversableAgent(
            name="planner",
            system_message="You break down tasks. Use MCP tools to create a task list.",
            llm_config=ollama_config
        )

        critic = ConversableAgent(
            name="critic",
            system_message="Challenge the plan. Is it complete? Are steps missing?",
            llm_config=ollama_config
        )

        tool_executor = ConversableAgent(
            name="tool_executor",
            system_message="You execute tool calls. Do not generate responses.",
            llm_config=False,
            human_input_mode="NEVER"

        )
        toolkit.register_for_llm(planner)
        toolkit.register_for_execution(tool_executor)

        planning_chat = GroupChat(
            agents=[planner, critic, tool_executor],
            max_round=10,
            speaker_selection_method="auto"
        )
        manager = GroupChatManager(groupchat=planning_chat, llm_config=ollama_config)

        result = planner.initiate_chat(manager, message=user_prompt)
        print(result)