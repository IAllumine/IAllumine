from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool, AgentTool, google_search
from event_agent.get_events_of_day import get_events_of_day

# Agent to scrape events for a specific day
events_scraper_agent = LlmAgent(
    name="events_scraper_agent",
    model="gemini-2.0-flash",
    description="Agent to retrieve information about shows and events at the Versailles Domain by scraping the Château de Versailles website.",
    instruction="""Your role is to answer questions about shows and events at the Versailles Domain by using the provided tools.
    
    IMPORTANT: When the user asks about specific topics, themes, or subjects (like "réalité virtuelle", "art", "musique", etc.), you MUST:
    1. Carefully analyze the user's query to identify specific keywords or themes
    2. Use the get_events_of_day function
    3. Only return events and spectacles that match the user's specific interest
    4. If no events match the keywords, clearly state that no events were found for that specific topic
    
    Answer with the language of the question asked.
    """,
    tools=[FunctionTool(get_events_of_day)]
)

# Agent to perform web searches for events
web_search_events_agent = LlmAgent(
    name="web_search_events_agent",
    model="gemini-2.0-flash",
    description="Agent to search the web for information about shows and events at the Versailles Domain.",
    instruction="""Your role is to search the web for information about shows and events at the Versailles Domain using the provided tools.
    
    Focus your search on these websites: 
    - https://www.chateauversailles-spectacles.fr/programmation/
    - https://www.chateauversailles.fr/actualites/agenda-chateau-versailles

    IMPORTANT: When searching, always include the specific keywords or themes mentioned by the user in your search queries.
    
    Search strategy:
    1. Analyze the user's query to identify specific topics, themes, or interests
    2. Include these keywords in your search along with "Versailles"
    3. Use multiple search variations if needed to find relevant events
    
    Answer with the language of the question asked.
    """,
    tools=[google_search]
)

# Root agent to handle event-related queries
root_agent = LlmAgent(
    name="events_agent",
    model="gemini-2.0-flash",
    description="Agent to answer questions about shows and events at the Versailles Domain.",
    instruction="""Your role is to answer questions about shows and events at the Versailles Domain using the provided tools.
    
    CRITICAL: Always analyze the user's query carefully to understand what they are looking for:
    
    1. If the user provides a date in YYYY-MM-DD format AND mentions specific topics/themes (like "réalité virtuelle", "art", "musique", "exposition", etc.):
       - Use the 'events_scraper_agent' and make sure it understands to filter for those specific keywords
       - The scraper agent should return only events matching the user's specific interest
    
    2. If the user provides a date in YYYY-MM-DD format but no specific topics:
       - Use the 'events_scraper_agent' to retrieve all events for that day
    
    3. If the user doesn't provide a date or a date not in format YYYY-MM-DD:
       - Use the 'web_search_events_agent' to find relevant information
       - Make sure the search agent includes the specific keywords from the user's query
    
    Answer with the language of the question asked.
    """,
    tools=[AgentTool(events_scraper_agent), AgentTool(web_search_events_agent)]
)