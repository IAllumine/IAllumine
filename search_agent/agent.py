from google.adk.agents import LlmAgent
from google.adk.tools import agent_tool
from google.adk.tools import google_search

root_agent = LlmAgent(
    name="search_agent",
    model="gemini-2.0-flash",
    description="Agent to answer questions about Versailles Castle.",
    instruction="Your role is to answer questions about Versailles Castle using the provided tool. Focus your search on this website : https://www.chateauversailles.fr/",
    # google_search is a pre-built tool which allows the agent to perform Google searches.
    tools=[google_search]
)