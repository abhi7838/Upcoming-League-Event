from django.shortcuts import render
import requests
import os 
from datetime import datetime 
from django.shortcuts import render


def upcoming_matches_view(request):
    # Retrieve API key securely from environment variables.
    # '1' is often used as a placeholder API key for basic free access with TheSportsDB V1.
    api_key = os.environ.get('SPORTSDB_API_KEY', '1')

    # Choose a league ID (e.g., 4328 for English Premier League Soccer, 4387 for NBA Basketball)
    league_id = '4328' # Defaulting to Soccer: English Premier League
    sport_name = 'Soccer' # Default sport name for display

    # Construct the API URL
    api_url = f"https://www.thesportsdb.com/api/v1/json/{api_key}/eventsnextleague.php?id={league_id}"

    matches_data = [] # Initialize an empty list to store processed match data

    try:
        # Make the API request with a timeout to prevent indefinite hanging [18]
        response = requests.get(api_url, timeout=10)
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)

        data = response.json() # Parse the JSON response into a Python dictionary

        # Check if the 'events' key exists and is not empty
        if data and data.get('events'):
            for event in data['events']:
                # Extract relevant data, providing default 'N/A' for missing fields
                home_team = event.get('strHomeTeam', 'N/A')
                away_team = event.get('strAwayTeam', 'N/A')
                event_date = event.get('dateEvent', 'N/A')
                event_time = event.get('strTime', 'N/A')

                # Combine date and time, then format for user-friendly display
                display_datetime = f"{event_date} {event_time}" # Default fallback
                try:
                    # Attempt to parse date and time. TheSportsDB can have different time formats.
                    # Example: "2024-12-25 15:00:00+00:00" or "2024-12-25 15:00"
                    if event_time and '+' in event_time:
                        dt_obj = datetime.strptime(f"{event_date} {event_time}", "%Y-%m-%d %H:%M:%S%z")
                    elif event_time:
                        dt_obj = datetime.strptime(f"{event_date} {event_time}", "%Y-%m-%d %H:%M")
                    else: # If only date is available
                        dt_obj = datetime.strptime(event_date, "%Y-%m-%d")
                    # Format for display: "Wednesday, December 25, 2024 at 03:00 PM"
                    display_datetime = dt_obj.strftime("%A, %B %d, %Y at %I:%M %p")
                except ValueError as e:
                    print(f"Warning: Could not parse date/time for event {home_team} vs {away_team}: {e}")
                    # Fallback to unformatted string if parsing fails

                matches_data.append({
                    'home_team': home_team,
                    'away_team': away_team,
                    'date_time': display_datetime,
                })
        else:
            print("No upcoming events found or API response format unexpected.")

    except requests.exceptions.RequestException as e:
        # Catch network-related errors (connection issues, timeouts)
        print(f"API request failed: {e}")
        # In a production application, this error would typically be logged and a user-friendly message displayed.
    except ValueError as e:
        # Catch errors during JSON parsing or date/time conversion
        print(f"Error processing API response: {e}")

    # Prepare the context dictionary to pass data to the template [15, 19, 20]
    context = {
        'matches': matches_data,
        'sport_name': sport_name,
    }
    # Render the HTML template with the prepared context
    return render(request, 'upcoming_matches.html', context)