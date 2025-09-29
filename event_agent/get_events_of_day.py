import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from typing import Optional
import calendar
from multiprocessing.pool import ThreadPool

def extract_events(soup):
    """
    Extracts event information from a BeautifulSoup-parsed HTML document.
    Args:
        soup (bs4.BeautifulSoup): A BeautifulSoup object representing the parsed HTML content.
    Returns:
        list[dict]: A list of dictionaries, each containing details about an event. 
            Each dictionary may include the following keys:
                - 'title' (str): The title of the event.
                - 'url' (str): The URL associated with the event.
                - 'date' (str): The date of the event.
                - 'description' (str): A short description of the event.
                - 'image' (str): The URL of the event's image.
    """
    events = []
    # Rechercher la section des événements
    events_section = soup.find('div', class_='date-agenda--expo')
    
    if events_section:
        # Trouver toutes les entrées d'événements
        event_items = events_section.find_all('div', class_='row news')
        
        for item in event_items:
            event = {}
            
            # Extraire le titre
            title_elem = item.find('h4')
            if title_elem and title_elem.find('a'):
                event['title'] = title_elem.find('a').get_text(strip=True)
                event['url'] = title_elem.find('a').get('href', '')
            
            # Extraire la date
            date_elem = item.find('p', class_='date')
            if date_elem:
                event['date'] = date_elem.get_text(strip=True)
            
            # Extraire la description
            desc_elem = item.find('p')
            if desc_elem and desc_elem.find('a'):
                event['description'] = desc_elem.find('a').get_text(strip=True)
            
            if event:  # Ajouter seulement si on a trouvé des infos
                events.append(event)
    
    return events

def extract_spectacles(soup):
    """
    Extracts a list of spectacles from a BeautifulSoup-parsed HTML document.
    This function searches for a specific section in the HTML containing spectacle information,
    then iterates through each spectacle entry to extract details such as title, type, schedule,
    location, booking URL, and image.
    Args:
        soup (bs4.BeautifulSoup): A BeautifulSoup object representing the parsed HTML content.
    Returns:
        list[dict]: A list of dictionaries, each containing information about a spectacle with possible keys:
            - 'title' (str): The title of the spectacle.
            - 'type' (str): The type or date information of the spectacle.
            - 'schedule' (str): The schedule or time of the spectacle.
            - 'location' (str): The location where the spectacle takes place.
            - 'booking_url' (str): The URL for booking or more information.
            - 'image' (str): The URL of the spectacle's image.
    """
    spectacles = []
    # Rechercher la section des spectacles
    spectacles_section = soup.find('div', class_='date-agenda--spectacle')
    
    if spectacles_section:
        # Trouver toutes les entrées de spectacles
        spectacle_items = spectacles_section.find_all('div', class_='row news')
        
        for item in spectacle_items:
            spectacle = {}
            
            # Extraire le titre
            title_elem = item.find('h4')
            if title_elem:
                spectacle['title'] = title_elem.get_text(strip=True)
            
            # Extraire la date/type
            date_elem = item.find('p', class_='date')
            if date_elem:
                spectacle['type'] = date_elem.get_text(strip=True)
            
            # Extraire les horaires
            schedule_elem = item.find('span', property='dc:date')
            if schedule_elem:
                spectacle['schedule'] = schedule_elem.get_text(strip=True)
            
            # Extraire le lieu
            location_elem = item.find('p')
            if location_elem:
                location_text = location_elem.get_text(strip=True)
                # Extraire le lieu (généralement avant l'horaire)
                location_parts = location_text.split('\n')
                if location_parts:
                    spectacle['location'] = location_parts[0].strip()
            
            # Extraire le lien de réservation
            link_elem = item.find('a', href=True)
            if link_elem:
                spectacle['booking_url'] = link_elem.get('href', '')
            
            if spectacle:  # Ajouter seulement si on a trouvé des infos
                spectacles.append(spectacle)
    
    return spectacles


def get_events_of_day(date: str) -> dict:
    """Fetch events for a specific day from the Versailles Castle website.
    Args:
        date (str): Date in the format 'YYYY-MM-DD'.
    Returns:
        dict: A dictionary containing event details for the specified date.
    """
    url = f"https://www.chateauversailles.fr/actualites/agenda-chateau-versailles/fr-{date}"


    try:
        response = requests.get(url, verify=False, timeout=120)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        with ThreadPool(processes=2) as pool:
            events_result = pool.apply_async(extract_events, (soup,))
            spectacles_result = pool.apply_async(extract_spectacles, (soup,))
            events = events_result.get()
            spectacles = spectacles_result.get()

        return {
            "date": date,
            "url": url,
            "extraction_timestamp": datetime.now().isoformat(),
            "events": events,
            "spectacles": spectacles,
            "summary": {
                "total_events": len(events),
                "total_spectacles": len(spectacles),
            }
        }
    except requests.RequestException as e:
        print(f"❌ Erreur lors de la récupération: {e}")
        return None
    except Exception as e:
        print(f"❌ Erreur lors de l'extraction: {e}")
        return None
    
def get_events_of_month(year: Optional[int] = None, month: Optional[int] = None) -> dict:
    """
    Retrieve events for every day of a given month.
    Args:
        year (int): Year, e.g. 2025, default to current year if None
        month (int): Month number 1-12, default to current month if None
    Returns:
        dict: {
            "year": year,
            "month": month,
            "days": [ {daily result or None}, ... ],
            "summary": {
                "total_days_with_events": int,
                "total_events": int,
                "total_spectacles": int
            }
        }
    """
    if year is None:
        year = datetime.now().year

    if month is None:
        month = datetime.now().month

    _, ndays = calendar.monthrange(year, month)
    dates = [datetime(year, month, day).date().isoformat() for day in range(1, ndays + 1)]

    results = []
    total_events = 0
    total_spectacles = 0

    max_workers = min(8, len(dates))
    with ThreadPool(processes=max_workers) as pool:
        asyncs = [pool.apply_async(get_events_of_day, (d,)) for d in dates]
        for a in asyncs:
            res = a.get()
            results.append(res)
            if res:
                total_events += res.get("summary", {}).get("total_events", 0)
                total_spectacles += res.get("summary", {}).get("total_spectacles", 0)

    days_with_events = sum(1 for r in results if r and (r.get("summary", {}).get("total_events", 0) > 0 or r.get("summary", {}).get("total_spectacles", 0) > 0))

    return {
        "year": year,
        "month": month,
        "days": results,
        "summary": {
            "total_days_with_events": days_with_events,
            "total_events": total_events,
            "total_spectacles": total_spectacles
        }
    }