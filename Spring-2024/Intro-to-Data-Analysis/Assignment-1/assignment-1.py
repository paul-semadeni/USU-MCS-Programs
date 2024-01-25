"""
    Assignment 1
        Class: Intro to Data Analysis (CS6850)
        Instructor: Dr. Hamid Karimi
        Date: January 22, 2024
        Student: Paul Semadeni
"""
import numpy as np
import pandas as pd
from openai import OpenAI
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.preprocessing import OneHotEncoder

# TODO: Insert the table into a pandas data frame fed from a file named "students.csv"
with open("./files/vehicle.csv", "r") as file:
    csv = pd.read_csv(file)
    df = pd.DataFrame(csv)
    print(df.head())

    # TODO: Numerically represent each column
    print(df.dtypes)
    classes = set(df["class"])
    print(classes)
    # Integer encode the class column in the dataframe
    class_map = dict()
    i = 0
    for c in classes:
        class_map[c] = i
        i += 1
    print(class_map)
    df["class"] = df["class"].map(class_map)
    print(df.dtypes)
    # TODO: Convert the table content into a numpy array
    np_df = df.to_numpy()
    print(np_df)

with open("./files/wiki_edit.txt", "r") as file:
    txt = pd.read_csv(file, sep=" ", header=None)
    df = pd.DataFrame(txt)
    df = df.rename(columns={ 0: "RevisionId", 1: "ArticleId", 2: "Timestamp", 3: "Editor" })
    print(df)
    # TODO: Find the top 5 articles that have received the highest edits
    top_five_art = df["ArticleId"].value_counts().head()
    print(top_five_art)

    # TODO: Find the top 5 editors who have edited the most number of articles.
    top_five_editor = df["Editor"].value_counts().head()
    print(top_five_editor)

with open("./files/wh.json", "r") as file:
    # TODO: Find the top 15 most frequent terms that appear in the tweet messages
    json = pd.read_json(file, lines=True)
    df = pd.DataFrame(json)
    temp_dict = dict()
    for tweet in df["text"]:
        words = tweet.split(" ")
        for word in words:
            if word not in temp_dict:
                temp_dict[word] = 0
            temp_dict[word] += 1
    sorted_dict = dict(sorted(temp_dict.items(), key=lambda temp_dict: temp_dict[1], reverse=True))
    print(sorted_dict)

    # TODO: Represent the text of tweets using One-hot encoding
    for tweet in df["text"]:
        print(tweet)
        unique_words = set()
        temp_list = tweet.split(" ")
        unique_words = unique_words.union(set(temp_list))
        np_temp_list= np.reshape(list(temp_list), (-1, 1))
        enc = OneHotEncoder(categories=[list(unique_words)])
        one_hot_enc = enc.fit(np_temp_list)
        print(one_hot_enc.transform(np_temp_list).toarray())

    # TODO: Represent the text of tweets using Bag of Words (BOW)
    for tweet in df["text"]:
        print(tweet)
        temp_list = tweet.split(" ")
        vectorizer = CountVectorizer(stop_words=None)
        vectorizer.fit(temp_list)
        print(vectorizer.vocabulary_)
        vector = vectorizer.transform(temp_list)
        print(vector.shape)
        print(vector.toarray())

    # TODO: Represent the text of tweets using TF-IDF
    for tweet in df["text"]:
        print(tweet)
        temp_list = tweet.split(" ")
        tf = TfidfVectorizer()
        fit_tweet = tf.fit(temp_list)
        trans_tweet = fit_tweet.transform([temp_list[0]])
        print(trans_tweet.toarray())
        idf = tf.idf_
        print(dict(zip(fit_tweet.get_feature_names_out(), idf)))

    # TODO: Represent the text of tweets using bigrams
    for tweet in df["text"]:
        print(tweet)
        temp_list = list()
        temp_list.append(tweet)
        bigram_vectorizer = CountVectorizer(analyzer="word", ngram_range=(2,2))
        fit_bigram = bigram_vectorizer.fit_transform(temp_list)
        print(bigram_vectorizer.get_feature_names_out())
        print(fit_bigram.toarray())

# TODO: Show the semantic relations (similarity/dissimilarity) between a couple of words/phrases/sentences
my_api_key = "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"
client = OpenAI(api_key=my_api_key)
def open_ai_embedding(text):
    embedding= client.embeddings.create(input = [text], model="text-embedding-ada-002").data[0].embedding
    return np.array(embedding)

# embedding=open_ai_embedding("hello")
# embedding=open_ai_embedding("hello, my name is bob. Your name is jane")
embedding=open_ai_embedding("bye")
print(embedding)
