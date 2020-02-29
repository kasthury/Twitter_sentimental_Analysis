
# -*- coding: utf-8 -*-


import numpy as np
import pandas as pd
import re
import nltk

nltk.download('stopwords')
from nltk.corpus import stopwords

tweets = pd.read_csv("tweets1.csv")
tweets.head()

tweets.shape

# import seaborn as sns
#
# sns.countplot(x='airline_sentiment', data=tweets)
#
# sns.countplot(x='airline', data=tweets)
#
# sns.countplot(x='airline', hue="airline_sentiment", data=tweets)

X = tweets.iloc[:, 10].values
y = tweets.iloc[:, 1].values

processed_tweets = []

for tweet in range(0, len(X)):
    # Remove all the special characters
    processed_tweet = re.sub(r'\W', ' ', str(X[tweet]))

    # remove all single characters
    processed_tweet = re.sub(r'\s+[a-zA-Z]\s+', ' ', processed_tweet)

    # Remove single characters from the start
    processed_tweet = re.sub(r'\^[a-zA-Z]\s+', ' ', processed_tweet)

    # Substituting multiple spaces with single space
    processed_tweet = re.sub(r'\s+', ' ', processed_tweet, flags=re.I)

    # Removing prefixed 'b'
    processed_tweet = re.sub(r'^b\s+', '', processed_tweet)

    # Converting to Lowercase
    processed_tweet = processed_tweet.lower()


    processed_tweets.append(processed_tweet)


from sklearn.feature_extraction.text import TfidfVectorizer

tfidfconverter = TfidfVectorizer(max_features=2000, min_df=5, max_df=0.7, stop_words=stopwords.words('english'))
X = tfidfconverter.fit_transform(processed_tweets).toarray()
print(X)

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)


from sklearn.ensemble import RandomForestClassifier

text_classifier = RandomForestClassifier(n_estimators=100, random_state=0)
text_classifier.fit(X_train, y_train)


predictions = text_classifier.predict(X_test)


from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

print(confusion_matrix(y_test, predictions))
print(classification_report(y_test, predictions))
print(accuracy_score(y_test, predictions))


# from sklearn.svm import SVC
# from sklearn.metrics import roc_auc_score
# from datetime import date
# clf = SVC(probability=True, kernel='rbf')
# clf.fit(X_train, y_train)
#
# # predict and evaluate predictions
# predictions = clf.predict_proba(X_test)
# print('ROC-AUC yields ' + str(roc_auc_score(y_test, predictions[:,1])))

