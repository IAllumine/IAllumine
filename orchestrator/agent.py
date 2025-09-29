from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool
from search_agent.agent import root_agent as search_agent

root_agent = LlmAgent(
    name="orchestrator",
    model="gemini-2.0-flash",
    description="Agent to answer questions about Versailles Castle.",
    instruction="Your role is to answer questions about Versailles Castle using the provided tool. Be clear and exhaustive in your answers.",
    tools=[AgentTool(agent=search_agent)]
)