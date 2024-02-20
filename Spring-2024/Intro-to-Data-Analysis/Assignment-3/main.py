"""
    Assignment 3
        Class: Intro to Data Analysis (CS6850)
        Instructor: Dr. Hamid Karimi
        Date: February 15, 2024
        Student: Paul Semadeni
"""
import pandas as pd
import mysql.connector
import helpers.constants as DB_CONN
import pymongo

# TODO: Open a connection to the database server on your machine.
def db_connection():
    cnx = mysql.connector.connect(user=DB_CONN.USERNAME, password=DB_CONN.PASSWORD, host=DB_CONN.HOST_NAME, database=DB_CONN.DATABASE_NAME)
    return cnx

cnx = db_connection()
cursor = cnx.cursor()
query = ""
# TODO: Create a table named Wiki Edit, which contains the following schema

query = "DROP TABLE wiki_edit;"
cursor.execute(query)
query = ("CREATE TABLE wiki_edit("
	"revision_id 		INT 				AUTO_INCREMENT"
    ", article_name 		VARCHAR(500)"
    ", edit_date 		DATE"
    ", user_name 		VARCHAR(50)"
    ", CONSTRAINT pk_id 	PRIMARY KEY 		(revision_id)"
");")
cursor.execute(query)

# TODO: Read the file wiki edit.txt directly, parse each line, and store the fields from each line in the database
values = list()
with open("./files/wiki_edit.txt") as file:
    for edit in file:
        value = tuple(edit.split(" "))
        values.append(value)
# Insert values into database
query = "INSERT INTO wiki_edit (revision_id, article_name, edit_date, user_name) VALUES (%s, %s, %s, %s)"
cursor.executemany(query, values)
cnx.commit()
print(cursor.rowcount, "rows were inserted")

# TODO: Query the database and find the Article name with the largest number of edits.
query = "SELECT article_name, COUNT(*) FROM wiki_edit GROUP BY article_name ORDER BY COUNT(*) DESC LIMIT 1"
cursor.execute(query)
row = cursor.fetchone()
print(row)
cursor.close()
cnx.close()

# TODO: Launch the MongoDB server.
def mongodb_connection():
    try:
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        mongo_db = client["mongo_db"]
        print("Successfully connected to MongoDB")
    except Exception as e:
        print("Failed to connect to MongoDB" + str(e))
    return mongo_db
 # TODO: Use pymongo and write a Python script that will store the JSON files of downloaded followers and followees from Assignment 2 into two collections named followers and followees, respectively.
with open("./files/followers.json", "r") as f1, open("./files/followees.json", "r") as f2:
    followers = pd.read_json(f1)
    followers["follower_or_followee"] = "follower"

    followees = pd.read_json(f2)
    followees["follower_or_followee"] = "followee"

combined = [followers, followees]
merged = pd.concat(combined)

merged_subset = merged[["id", "name", "screen_name", "follower_or_followee", "location", "description", "followers_count", "friends_count", "statuses_count", "favourites_count", "created_at", "verified"]]
merged_subset = merged_subset.rename(columns={"statuses_count": "number_of_tweets", "friends_count": "followees_count"})

tweet_dict = merged_subset.to_dict(orient="records")
# Insert into mongo_db
mongo_db = mongodb_connection()
col = mongo_db["twitter"]
if "twitter" in mongo_db.list_collection_names():
    col.drop()
    print("Twitter collection already exists")
x = col.insert_many(tweet_dict)
# TODO: The average followers count of your followers
query = {"follower_or_followee": "follower"}
count = 0
total = 0
for x in col.find(query, {"followers_count": 1}):
    count += x["followers_count"]
    total += 1
print("Your followers average # of followers: ", round(count / total, 0))

# TODO: The average followers count of your followees
query = {"follower_or_followee": "followee"}
count = 0
total = 0
for x in col.find(query, {"followers_count": 1}):
    count += x["followers_count"]
    total += 1
print("Your followees average # of followers: ", round(count / total, 0))

# TODO: The average followees count of your followers
query = {"follower_or_followee": "follower"}
count = 0
total = 0
for x in col.find(query, {"followees_count": 1}):
    count += x["followees_count"]
    total += 1
print("Your followers average # of followees: ", round(count / total, 0))

# TODO: The average followers count of your followees
query = {"follower_or_followee": "followee"}
count = 0
total = 0
for x in col.find(query, {"followees_count": 1}):
    count += x["followees_count"]
    total += 1
print("Your followees average # of followees: ", round(count / total, 0))

# TODO: The number of your verified followers/followees (separately and combined).
query = {"follower_or_followee": "follower", "verified": True}
total = 0
for x in col.find(query, {"follower_or_followee": 1, "verified": 1}):
    total += 1
print("# of verified followers: ", total)

query = {"follower_or_followee": "followee", "verified": True}
total = 0
for x in col.find(query, {"follower_or_followee": 1, "verified": 1}):
    total += 1
print("# of verified followees: ", total)

# TODO: The average favorites count of your followers/followees (separately and combined).
query = {"follower_or_followee": "follower"}
count = 0
total = 0
for x in col.find(query, {"follower_or_followee": 1, "favourites_count": 1}):
    count += x["favourites_count"]
    total += 1
print("Your followers average # of favorites: ", round(count / total, 0))

query = {"follower_or_followee": "followee"}
count = 0
total = 0
for x in col.find(query, {"follower_or_followee": 1, "favourites_count": 1}):
    count += x["favourites_count"]
    total += 1
print("Your followees average # of favorites: ", round(count / total, 0))

# TODO: The average number of tweets of your followers/followees (separately and com-bined)
query = {"follower_or_followee": "follower"}
count = 0
total = 0
for x in col.find(query, {"follower_or_followee": 1, "number_of_tweets": 1}):
    count += x["number_of_tweets"]
    total += 1
print("Your followers average # of tweets: ", round(count / total, 0))

query = {"follower_or_followee": "followee"}
count = 0
total = 0
for x in col.find(query, {"follower_or_followee": 1, "number_of_tweets": 1}):
    count += x["number_of_tweets"]
    total += 1
print("Your followees average # of tweets: ", round(count / total, 0))

# TODO: BONUS Extract the number of your followers and followees per year using the creation time field, e.g.
# pipeline = [
#     {"$group": {"_id": {"$year": "created_at"}}},
# ]
# print(list(col.aggregate(pipeline)))