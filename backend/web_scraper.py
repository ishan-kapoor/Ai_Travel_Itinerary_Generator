import requests
from bs4 import BeautifulSoup

def fetch_activity_details(activity_names, location=""):
    """
    Fetches details of activities (name, description, and image URL) using web scraping.

    :param activity_names: List of activity names to search for.
    :param location: The destination location.
    :return: List of dictionaries with activity details.
    """

    activity_details = []

    for activity in activity_names:
        search_query = f"{activity} in {location} site:tripadvisor.com"
        google_search_url = f"https://www.google.com/search?q={search_query.replace(' ', '+')}"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        }

        response = requests.get(google_search_url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            # Extract the first search result
            first_link = soup.find("a", href=True)
            if first_link:
                tripadvisor_url = first_link["href"]

                # Fetch actual activity details from TripAdvisor
                tripadvisor_response = requests.get(tripadvisor_url, headers=headers)
                tripadvisor_soup = BeautifulSoup(tripadvisor_response.text, "html.parser")

                # Extract activity description
                description = tripadvisor_soup.find("meta", {"name": "description"})
                activity_description = description["content"] if description else "No description available."

                # Extract image (usually inside an <img> tag)
                image_tag = tripadvisor_soup.find("img")
                activity_image = image_tag["src"] if image_tag else None

                activity_details.append({
                    "name": activity,
                    "description": activity_description,
                    "image": activity_image,
                    "link": tripadvisor_url
                })
            else:
                activity_details.append({
                    "name": activity,
                    "description": "No details found.",
                    "image": None,
                    "link": None
                })
        else:
            activity_details.append({
                "name": activity,
                "description": "Failed to fetch data.",
                "image": None,
                "link": None
            })

    return activity_details
