from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool, AgentTool, google_search
from event_agent.get_events_of_day import get_events_of_day, get_events_of_month
from datetime import datetime

# Agent to scrape events for a specific day
root_agent = LlmAgent(
    name="events_scraper_agent",
    model="gemini-2.5-flash",
    description="Agent to retrieve information about shows and events at the Versailles Domain by scraping the Château de Versailles website.",
    instruction="""Your role is to answer questions about shows and events at the Versailles Domain by using the provided tools. 
    
    You must follow these rules:
    - Use get_events_of_month for broader month-level queries.
    - Use get_events_of_day for topic/keyword filtered queries and when user requests exact event listings for a given day.
    - When the user asks non-event or non-show related questions, you must call get_events_of_month include results and take only the results !
    - Only answer with the language of the user's question.
    - Only use the tools provided.
    - Only answer with the list of events and shows.
    - You must use one of the tools : get_events_of_day or get_events_of_month.
    - You cannot talk about the thnings that you can't do.

    - IMPORTANT: When the user asks about specific topics, themes, or subjects (like "réalité virtuelle", "art", "musique", etc.), you MUST:
      1. Carefully analyze the user's query to identify specific keywords or themes
      2. Use the get_events_of_day function.
      3. Only return events and spectacles that match the user's specific interest
      4. If no events match the keywords, clearly state that no events were found for that specific topic.
    """,
    tools=[FunctionTool(get_events_of_day), FunctionTool(get_events_of_month)],
    output_key="events"
)