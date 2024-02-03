"""
    Assignment 2
        Class: Intro to Data Analysis (CS6850)
        Instructor: Dr. Hamid Karimi
        Date: February 1, 2024
        Student: Paul Semadeni
"""
from bs4 import BeautifulSoup
import json
import pandas as pd
import requests
from helpers import constants

# TODO: Google's Geocoding API
def reverse_geocode(lat, lng):
    url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={ lat },{ lng }&key={ constants.KEY }"

    with requests.get(url, verify=True) as response:
        location = list()
        res = json.loads(response.text)
        results = res["results"][0]
        address = results["formatted_address"]

        address_components = results["address_components"]
        city_state = [ a["long_name"] for a in address_components if "administrative_area_level_1" in a["types"] or ("locality" in a["types"] or "sublocality" in a["types"])]
        if len(city_state):
            location.append([address, city_state[0], city_state[1]])
        else:
            location = []
    return location

# TODO: Extract city and country from ‘place’ field (if they exist). Then, print the number of tweets per city and country in descending order

with open("./files/FIFAWorldCup2022.json", "r") as file:
    tweets = pd.read_json(file)
    places = tweets["place"].dropna().apply(pd.Series)
    print(places.columns)
    # Print count of countries in descending order
    country_count = places["country"].value_counts()
    print(country_count)
    # Print count of cities in descending order
    places = places[places["place_type"] == "city"]
    city_count = places["name"].value_counts()
    print(city_count)

#TODO: Construct a Pandas data frame from the followers and followees data that includes thesefields: id, name, screen name, follower or followee, location, description, followers count, friends count (number of followees), favorite count, creation time (in datetime format), number of tweets (statuses  count) and verified
with open("./files/followers.json", "r") as f1, open("./files/followees.json", "r") as f2:
    followers = pd.read_json(f1)
    followers["follower_or_followee"] = "follower"
    print(followers.shape)

    followees = pd.read_json(f2)
    followees["follower_or_followee"] = "followee"
    print(followees.shape)

    combined = [followers, followees]
    merged = pd.concat(combined)
    print(merged.shape)

    merged_subset = merged[["id", "name", "screen_name", "follower_or_followee", "location", "description", "followers_count", "friends_count", "statuses_count", "favourites_count", "created_at", "verified"]]
    merged_subset = merged_subset.rename(columns={"statuses_count": "number_of_tweets", "friends_count": "followees_count"})
    print(merged_subset.dtypes)

    followers_subset = merged_subset[merged_subset["follower_or_followee"] == "follower"]
    followees_subset = merged_subset[merged_subset["follower_or_followee"] == "followee"]
# TODO: I)	    The average followers count of your followers
    print("\nThe average followers count of your followers")
    print(followers_subset["followers_count"].mean())
# TODO: II)	    The average followers count of your followees
    print("The average followers count of your followees")
    print(followees_subset["followers_count"].mean())
# TODO: III)	The average followees count of your followers
    print("The average followees count of your followers")
    print(followers_subset["followees_count"].mean())
# TODO: IV)	    The average followees count of your followeees
    print("The average followees count of your followees")
    print(followees_subset["followees_count"].mean())
# TODO: V)	    The number of your verified followers/followees (separately and combined).
    verified_followers = followers_subset[followers_subset["verified"] == True]
    verified_followees = followees_subset[followees_subset["verified"] == True]
    print("\nThe number of your verified followers")
    print(len(verified_followers.index))
    print("The number of your verified followees")
    print(len(verified_followees.index))
    print("Combined")
    print(len(verified_followers.index) + len(verified_followees.index))
# TODO: VI)	    The average favorites count of your followers/followees (separately and combined).
    print("\nThe average favourites count of your followers")
    print(followers_subset["favourites_count"].mean())
    print("The average favourites count of your followees")
    print(followees_subset["favourites_count"].mean())
    print("Combined")
    print(followers_subset["favourites_count"].mean() + followees_subset["favourites_count"].mean())
# TODO: VII)	The average number of tweets of your followers/followees (separately and combined).
    print("\nThe average number of tweets of your followers")
    print(followers_subset["number_of_tweets"].mean())
    print("The average number of tweets of your followees")
    print(followees_subset["number_of_tweets"].mean())
    print("Combined")
    print(followers_subset["number_of_tweets"].mean() + followees_subset["number_of_tweets"].mean())
# TODO: VIII)	Extract the number of your followers and followees per year using the creation time field,e.g.:
    print("\nNumber of followers per year")
    print(followers_subset["created_at"].dt.year.value_counts())
    print("Number of followees per year")
    print(followees_subset["created_at"].dt.year.value_counts())

# TODO: Use BeautifulSoup python package and retrieve project information and descriptions from my lab’s research website
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/75.0.3770.80 Safari/537.36'}
page = requests.get("https://cs.usu.edu/people/HamidKarimi/projects.html", headers=headers, verify=False)
soup = BeautifulSoup(page.content, "html.parser")
# print(soup.prettify())

projects = list()
for project in soup.find_all("div", {"class": "project"}):
    temp_list = list()
    t = project.find("h3", {"class": "project-title"})
    d = project.find("p")
    l = [li.string for li in project.find("li")]
    if t:
        temp_list.append(t.b.string)
    if d:
        temp_list.append(d.string)
    if l:
        temp_list.append(",".join(l))

    projects.append(temp_list)

print("\n")
print(projects)
print(len(projects))

# TODO: Extract the latitude and longitude of each tweet of ‘geo tagged tweets.json’ file (available in the Data folder on Canvas) and use Google Maps Geocoding to convert them to human-readable addresses. Print the addresses and extract cities and states.
print("\n")
with open("./files/geo_tagged_tweets.json", "r") as file:
    json_str = json.load(file)
    tweets = json.loads(json_str)
    locations = list()
    for tweet in tweets:
        coordinates = tweet["geo"]["coordinates"]
        lat = coordinates[0]
        lng = coordinates[1]
        locations += reverse_geocode(lat, lng)

    print(f"Address".ljust(100), f"City".ljust(30), f"State".ljust(30))
    for location in locations:
        print(f"{location[0]}".ljust(100), f"{location[1]}".ljust(30), f"{location[2]}".ljust(30))