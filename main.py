from flask import Flask, jsonify, request
import csv
from demographic_filter import output
from content_filter import get_recommendations
from storage import all_articles, liked_articles, unliked_articles

app = Flask(__name__)

@app.route("/get-article")
def get_article():
    article_data = {
        "title" : all_articles[0]["title"],
        "contentId" : all_articles[0]["contentId"],
        "total_events" : all_articles[0]["total_events"]
    }
    return jsonify({
        "data" : article_data,
        "status" : "success"
    })

@app.route("/liked-article", methods=["POST"])
def liked_article():
    article = all_articles["title"]
    liked_articles.append(article)
    all_articles.pop(0)
    return jsonify({
        "status" : "success"
    }), 201

@app.route("/unliked-article", methods=["POST"])
def unliked_article():
    article = all_articles["title"]
    unliked_articles.append(article)
    all_articles.pop(0)
    return jsonify({
        "status" : "success"
    }), 201

@app.route("/popular-articles", methods=["POST"])
def popular_articles():
    article_data = []
    for article in output:
        _d = {
            "title" : article["title"],
            "contentId" : article["contentId"],
            "total_events" : article["total_events"]
        }
        article_data.append(_d)
    return jsonify({
      "status" : "success"
    }), 200

@app.route("/recommended-articles", methods=["POST"])
def recommended_articles():
    all_recommended = []
    for liked_article in liked_articles:
        output = get_recommendations(liked_articles[19])
        for data in output:
            all_recommended.append(data)
    import itertools 
    all_recommended.sort()
    all_recommended = list(all_recommended for all_recommended, _ in itertools.groupby(all_recommended))
    article_data = []    
    for recommended in all_recommended:
        _d = {
            "title" : recommended["title"],
            "contentId" : recommended["events"],
            "total_events" : recommended["total_events"]
        }
        article_data.append(_d)
    return jsonify({
        "data" : article_data,
        "status" : "success"
    }), 200

if __name__ == "__main__":
    app.run()