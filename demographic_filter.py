import numpy as np 
import pandas as pd 

df = pd.read_csv("articles.csv")

C = df["total_events"].mean()
m = df["total_events"].quantile(0.9)
q_articles = df.copy().loc[df["total_events"] >= m]

def weighted_rating(x, m=m, C=C):
    v = x["total_events"]
    R = x["total_events"]
    return (v/(v+m) * R) + (m/(m+v) * C)

q_articles['score'] = q_articles.apply(weighted_rating, axis = 1)
q_articles = q_articles.sort_values('score', ascending=False)
output = q_articles[['title', 'total_events']].head(20).values.tolist()

print(output)