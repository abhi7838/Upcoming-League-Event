from django.shortcuts import render
import requests
import os 
from datetime import datetime 
from django.shortcuts import render


def upcoming_matches_view(request):

    # api_key = os.environ.get('SPORTSDB_API_KEY', '1')
    api_key = '123'
    # Choose a league ID (e.g., 4328 for English Premier League Soccer, 4387 for NBA Basketball)
    league_id = '4387' # Defaulting to Soccer: English Premier League
    sport_name = 'Basketball' # Default sport name for display

    # Construct the API URL
    api_url = f"https://www.thesportsdb.com/api/v1/json/{api_key}/eventsnextleague.php?id={league_id}"
    print(api_url)
    

    matches_data = [] 

    try:
        response = requests.get(api_url, timeout=10)
        response.raise_for_status() 

        data = response.json() 
        
        if data and data.get('events'):
            for event in data['events']:
                home_team = event.get('strHomeTeam', 'N/A')
                away_team = event.get('strAwayTeam', 'N/A')
                event_date = event.get('dateEvent', 'N/A')
                event_time = event.get('strTime', 'N/A')

                display_datetime = f"{event_date} {event_time}" # Default fallback
                try:
                    if event_time and '+' in event_time:
                        dt_obj = datetime.strptime(f"{event_date} {event_time}", "%Y-%m-%d %H:%M:%S%z")
                    elif event_time:
                        dt_obj = datetime.strptime(f"{event_date} {event_time}", "%Y-%m-%d %H:%M")
                    else: # If only date is available
                        dt_obj = datetime.strptime(event_date, "%Y-%m-%d")
                        
                    # Format for display: "Thursday, December 26, 2024 at 03:00 PM"
                    display_datetime = dt_obj.strftime("%A, %B %d, %Y at %I:%M %p")
                
                except ValueError as e:
                    print(f"Warning: Could not parse date/time for event {home_team} vs {away_team}: {e}")
                    #  unformatted string if parsing fails

                matches_data.append({
                    'home_team': home_team,
                    'away_team': away_team,
                    'date_time': display_datetime,
                })
        else:
            print("No upcoming events found or API response format unexpected.")

    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
    except ValueError as e:
        # errors during JSON parsing or date/time conversion
        print(f"Error processing API response: {e}")

    # context dictionary to pass data to the template [15, 19, 20]
    context = {
        'matches': matches_data,
        'sport_name': sport_name,
    }
    return render(request, 'upcoming_matches.html', context)

def basic(request): # just to check if django is working or not 
    return render(request, 'basic.html')