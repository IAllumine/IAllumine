from bs4 import BeautifulSoup
from datetime import datetime
import json
import requests

from google.adk.agents.llm_agent import LlmAgent


def get_date() -> str:
    """Function retrieving the current date in YYYY-MM-DD format."""
    now = datetime.now()
    return now.strftime("%Y-%m-%d")

def extract_text_and_title(html_str):
    """Function parsing the JSON of the weather and agenda from Versailles website https://www.chateauversailles.fr/epv/infos/{date}"""
    if not html_str:
        return None, None
    soup = BeautifulSoup(html_str, "html.parser")
    text = soup.get_text(" ", strip=True)
    titles = [tag.get("title") for tag in soup.find_all() if tag.get("title")]
    return text, titles[0] if titles else None

def get_weather_opening_affluence(date: str) -> dict:

    """Tool getting the weather, opening times and affluence for the specified date.

    Args:
        date: The date in YYYY-MM-DD format.

    Returns:
        A dictionary containing the weather, opening times and affluence.
    """

    mapping = {
        "nid_11": "Château",
        "nid_14": "Le Domaine de Trianon",
        "nid_12": "Les Jardins",
        "nid_1221": "Le Parc",
        "nid_582": "La Salle du Jeu de Paume",
        "nid_15": "La Grande Ecurie",
        "nid_26594": "La Petite Ecurie",
        "nid_583": "Le Domaine de Marly"
    }
    
    try : 
        url = f"https://www.chateauversailles.fr/epv/infos/{date}"
        resp = requests.get(url, verify=False)
        data = resp.json()
        weather_text, weather_title = extract_text_and_title(data.get("weather"))
        agenda_text, agenda_title = extract_text_and_title(data.get("weather_agenda_day"))
    except Exception as e:
        print(f"Error fetching or parsing data: {e}")
        return {"error": "L'IA n'a pas réussi à récupérer les informations météo ou des affluences."}

    structured_output = {
        "weather": weather_text,
        "ensoleillement": weather_title,
        "hub_lieux": {}
    }

    for nid, html in data.get("hub_lieux", {}).items():
        name = mapping.get(nid, nid)
        structured_output["hub_lieux"][name] = extract_text_and_title(html)[0]

    return structured_output

root_agent = LlmAgent(
    name="weather_time_agent",
    model="gemini-2.5-pro",
    description=(
        "Agent giving informations about the weather, opening times and affluence in Versailles for a specific date"
    ),
    instruction=(
        f"""You are a helpful agent who can give information about the weather, opening times and affluence in Versailles for a specific date. The date will be given as argument to the tool get_weather_opening_affluence in the format YYYY-MM-DD. 
        Today's date is {get_date()}
        If no specified date is given, always calculate the wanted date based on the user's request through today's date.
        If no year is specified, the current year will be used.
        If no month is specified, the current month will be used.
        Otherwise, you must use the nearest future date that you can think about corresponding to the user's request.
        If push comes to shove, you can use one of next week date for the tool get_weather_opening_affluence.
        Answer only with the information you got from the tool get_weather_opening_affluence.
        If you have many date choices, choose a random date among the choices.

        IMPORTANT : 
        You MUST ALWAYS give a date to the tool get_weather_opening_affluence and use it. 
        """
    ),
    tools=[get_weather_opening_affluence]
)