import os
from dataclasses import dataclass
from dotenv import load_dotenv
import chainlit as cl
from openai import AsyncOpenAI
from agents import (
    Agent, Runner, OpenAIChatCompletionsModel,
    set_tracing_disabled, function_tool, RunContextWrapper
)

load_dotenv()
set_tracing_disabled(True)

# Gemini LLM setup
client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai"
)
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client
)

# Context dataclass for todo list (local only, not shown to LLM)
@dataclass
class TodoContext:
    todos: list[str]

# Tool function: operates on ctx.context.todos
@function_tool
def todo_manager_tool(
    ctx: RunContextWrapper[TodoContext],
    action: str,
    item: str | None = None
) -> str:
    todos = ctx.context.todos

    if action == "add" and item:
        todos.append(item)
        return f"✅ Added '{item}'."
    elif action == "remove" and item:
        try:
            removed = todos.pop(int(item) - 1)
            return f"🗑️ Removed '{removed}'."
        except Exception:
            return "❗ Invalid index."
    else:
        if not todos:
            return "📭 No tasks."
        return "\n".join(f"{i+1}. {t}" for i, t in enumerate(todos))

# Create Stateful Agent
todo_agent = Agent[TodoContext](
    name="Hermes Todo Assistant",
    instructions="""
You are “Hermes,” a strategic and efficient AI task manager.

CONTEXT:
You help users add, remove, list, prioritize, and review tasks in their to‑do list using a dedicated tool.

OBJECTIVES:
• Always use the todo_manager_tool to make any changes.
• Confirm every update with a clear message.
• Ask for clarification if the user’s request is vague.

TONE & STYLE:
• Use friendly, concise language.
• Include bullet points or numbered lists when showing tasks.
• Begin confirmations with “✅” for successes and “❗” for issues.

POWER WORDS:
• Actionable
• Prioritized
• Bullet-pointed

TOOL USAGE:
• For add: call `todo_manager_tool(ctx, "add", "<task>")`.
• For remove: call `todo_manager_tool(ctx, "remove", "<index>")`.
• For list: call `todo_manager_tool(ctx, "list", None)`.

CONSTRAINTS:
• Do NOT act without tool use.
• Use tools exactly as instructed.
• If unclear—ask a single clarifying question.

RESPONSE FORMAT:
• Use a checkmark or bullet list based on response type.


""",
    model=model,
    tools=[todo_manager_tool],
)

# Initialize session
@cl.on_chat_start
async def on_start():
    cl.user_session.set("agent_context", TodoContext(todos=[]))
    await cl.Message("👋 Hi there! I can add, remove, or list your tasks.").send()

# Handle messages
@cl.on_message
async def handle(message: cl.Message):
    agent = todo_agent
    ctx = cl.user_session.get("agent_context")

    result = await Runner.run(
        agent,
        message.content,
        context=ctx
    )

    # Context mutated in-place by tool
    cl.user_session.set("agent_context", ctx)

    await cl.Message(result.final_output).send()
