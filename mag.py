#!/home/pdennis/projects/magazine/venv/bin/python
import requests
import random
import webbrowser
import time
import sys
import argparse

def get_random_magazine(collection=None, max_results=100, min_year=None, max_year=None, random_page=True):
    """
    Fetch a random magazine from the Internet Archive.

    Args:
        collection (str, optional): Specific collection to search within.
                                   Default is None (search all magazines).
        max_results (int, optional): Maximum number of results to retrieve.
                                    Default is 100.
        min_year (int, optional): Minimum publication year to include.
        max_year (int, optional): Maximum publication year to include.
        random_page (bool, optional): If True, request a random page of results.
                                     Default is True.

    Returns:
        dict: Details of the randomly selected magazine
    """
    # Base URL for Internet Archive API
    base_url = "https://archive.org/advancedsearch.php"

    # Build the query
    query = "mediatype:texts AND format:(magazine OR periodical)"

    # Add collection constraint if specified
    if collection:
        query += f" AND collection:{collection}"

    # Add year range if specified
    if min_year and max_year:
        query += f" AND year:[{min_year} TO {max_year}]"
    elif min_year:
        query += f" AND year:[{min_year} TO 2025]"
    elif max_year:
        query += f" AND year:[1800 TO {max_year}]"

    # Get total number of results to calculate random page
    count_params = {
        "q": query,
        "rows": 1,
        "output": "json"
    }

    try:
        # First get the total count
        count_response = requests.get(base_url, params=count_params)
        count_response.raise_for_status()
        total_results = count_response.json().get("response", {}).get("numFound", 0)

        if total_results == 0:
            print("No magazines found with the specified criteria.")
            return None

        # Calculate a random page number if requested
        page = 1
        if random_page and total_results > max_results:
            max_page = min(1000, total_results) // max_results  # API typically limits to ~1000 results
            page = random.randint(1, max_page)
            print(f"Searching page {page} of approximately {max_page} pages ({total_results} total results)")

        # Create parameters for the API request
        params = {
            "q": query,
            "fl[]": ["identifier", "title", "year", "creator", "collection", "description", "subject"],
            "rows": max_results,
            "page": page,
            "sort[]": ["random"],  # Request random sorting
            "output": "json"
        }

        # Make the request to the Internet Archive API
        response = requests.get(base_url, params=params)
        response.raise_for_status()

        # Parse the JSON response
        data = response.json()

        # Get the list of documents (items) from the response
        docs = data.get("response", {}).get("docs", [])

        if not docs:
            print("No magazines found with the specified criteria.")
            return None

        # Select a random magazine
        random_magazine = random.choice(docs)
        return random_magazine

    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Internet Archive: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def open_magazine(magazine):
    """
    Open the magazine in the default web browser.

    Args:
        magazine (dict): The magazine details
    """
    if not magazine:
        return

    identifier = magazine.get("identifier")
    url = f"https://archive.org/details/{identifier}"

    print(f"\nOpening: {magazine.get('title', 'Unknown Title')}")
    if "year" in magazine:
        print(f"Year: {magazine.get('year')}")
    if "creator" in magazine:
        print(f"Creator: {magazine.get('creator')}")
    if "collection" in magazine:
        collections = magazine.get("collection")
        if isinstance(collections, list):
            print(f"Collections: {', '.join(collections[:5])}")
        else:
            print(f"Collection: {collections}")
    if "subject" in magazine:
        subjects = magazine.get("subject")
        if isinstance(subjects, list):
            print(f"Subjects: {', '.join(subjects[:5])}")
        else:
            print(f"Subject: {subjects}")

    print(f"URL: {url}")
    webbrowser.open(url)

def list_popular_collections():
    """
    Display a list of popular magazine collections on Internet Archive.
    """
    collections = [
        "magazine_rack",
        "computers_and_techmagazines",
        "magazine_rack_additional",
        "pulpmagazinearchive",
        "vintage_computer_magazines",
        "national_geographic_magazine",
        "lifemagazine",
        "time_magazine_archives",
        "popular_mechanics",
        "newstatesman",
        "scientific_american",
        "magazine_collection",
        "popsci",  # Popular Science
        "vogue",
        "new_yorker",
        "harpers",
        "wired",
        "theleadingmagazine"
    ]

    print("\nPopular magazine collections on Internet Archive:")
    for i, collection in enumerate(collections, 1):
        print(f"{i}. {collection}")
    print("\nUse with: python random_magazine.py --collection collection_name")

def main():
    parser = argparse.ArgumentParser(description="Open a random magazine from the Internet Archive")
    parser.add_argument("--collection", type=str, help="Specific collection to search within")
    parser.add_argument("--max", type=int, default=100, help="Maximum number of results to search through")
    parser.add_argument("--min-year", type=int, help="Minimum publication year to include")
    parser.add_argument("--max-year", type=int, help="Maximum publication year to include")
    parser.add_argument("--list-collections", action="store_true", help="List popular magazine collections")
    parser.add_argument("--continuous", action="store_true", help="Open magazines continuously with a delay")
    parser.add_argument("--delay", type=int, default=30, help="Delay in seconds between magazines in continuous mode")
    parser.add_argument("--decade", type=int, help="Specify a decade (e.g., 1960 for the 1960s)")

    args = parser.parse_args()

    if args.list_collections:
        list_popular_collections()
        return

    # Handle decade argument
    if args.decade:
        args.min_year = args.decade
        args.max_year = args.decade + 9

    print("Fetching a random magazine from Internet Archive...")
    if args.min_year or args.max_year:
        year_range = f"from {args.min_year if args.min_year else 'earliest'} to {args.max_year if args.max_year else 'latest'}"
        print(f"Year range: {year_range}")

    try:
        if args.continuous:
            print(f"Continuous mode enabled. Press Ctrl+C to exit.")
            count = 1

            while True:
                print(f"\n[{count}] Finding next random magazine...")
                magazine = get_random_magazine(
                    args.collection,
                    args.max,
                    args.min_year,
                    args.max_year
                )
                open_magazine(magazine)
                print(f"Waiting {args.delay} seconds before opening the next magazine...")
                time.sleep(args.delay)
                count += 1
        else:
            magazine = get_random_magazine(
                args.collection,
                args.max,
                args.min_year,
                args.max_year
            )
            open_magazine(magazine)

    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
        sys.exit(0)

if __name__ == "__main__":
    main()
