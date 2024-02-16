An important note: you must work individually on this assignment. Violation of this will be

considered Plagiarism and Cheating (outlined in the Syllabus) and can incur drastic academic consequences.
Due Date: Feb 19, 2024 (11:59 PM)
Total points: 100 + 10 (Bonus)
Purpose
This assignment will help you practice storing and retrieving data to/from relational and non-relational databases using SQL and NoSQL, respectively.
For this assignment, you need to install MySQL and MongoDB on your machine. Several links were provided in the slides. Also, if you search online, you can find easy-to-follow instructions on how to install them.
1. [40 points] SQL
Write a python script using the mysql-connector library to perform the following steps:
    (a)	[5 points] Open a connection to the database server on your machine.
    (b)	[15 points] Create a table named Wiki Edit, which contains the following schema:
            RevisionID: int Primary Key
            ArticleName: varchar(500)
            EditDate: date
            UserName: varchar(50)
    (c)	[15 points] Read the file wiki edit.txt and parse each line to identify the individual fields. For this question, do not use the read table and DataFrame approaches presented in the lecture. Instead, you should read the file directly, parse each line, and store the fields from each line in the database. You can refer to the example given in (Data Representation.pptx) on how to read from the data file directly and split each line into individual fields.
    (d)	[5 points] Query the database and find the Article name with the largest number of edits.
2. [70 points] NoSQL
    (a)	Launch the MongoDB server.
    (b)	[10 points ] Use pymongo and write a Python script that will store the JSON files of downloaded followers and followees from Assignment 2 into two collections named followers and followees, respectively. You need to insert only these fields: id, name, screen name, follower or followee, location, description, followers count, friends count (number of followees), favorite count, creation time (in datetime format), number of tweets (statuses count) and verified. However, you can easily insert all data of each JSON object.
    (c)	[50+10 points] Write queries to compute the following:
        I)	[5 points] The average followers count of your followers
        II)	[5 points] The average followers count of your followees
        III)	[5 points] The average followees count of your followers
        IV)	[5 points] The average followees count of your followeees
        V)	[10 points] The number of your verified followers/followees (separately and combined).
        VI)	[10 points] The average favorites count of your followers/followees (separately and combined).
        VII)	[10 points] The average number of tweets of your followers/followees (separately and com-bined).
        VIII)	Bonus [10 points] Extract the number of your followers and followees per year using the creation time field, e.g.:

            Year	Number of followers
            2019	23
            2016	21
            2013	46

            Year	Number of followees
            2020	6
            2017	18
            2013	20

Deliverable:
Assignmnet3.ipnyb: Your python notebook contains the code for all questions. Please properly separate the solution to each question. You need to make sure SQL and NoSQL commands and their results are included. You can submit other files if you consider them necessary.
