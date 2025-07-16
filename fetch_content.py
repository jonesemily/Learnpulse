import feedparser
import requests
from bs4 import BeautifulSoup

# RSS sources
RSS_FEEDS = [
    "https://ai.googleblog.com/feeds/posts/default?alt=rss",
    "https://www.latent.space/feed.xml"
]

def get_articles_from_rss(url, max_items=3):
    feed = feedparser.parse(url)
    articles = []

    for entry in feed.entries[:max_items]:
        articles.append({
            "title": entry.title,
            "content": entry.summary,
            "link": entry.link
        })

    return articles

def get_articles_from_arxiv(max_items=3):
    url = "https://arxiv.org/list/cs.AI/recent"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    titles = soup.select("dd > div.list-title")
    abstracts = soup.select("dd > p.mathjax")
    links = soup.select("dt > span.list-identifier > a[title='Abstract']")

    articles = []
    for i in range(min(max_items, len(titles))):
        title = titles[i].text.replace("Title:", "").strip()
        content = abstracts[i].text.strip() if i < len(abstracts) else "No abstract available."
        link = "https://arxiv.org" + links[i]['href'] if i < len(links) else ""
        articles.append({
            "title": title,
            "content": content,
            "link": link
        })

    return articles

def get_latest_articles():
    all_articles = []

    # Get RSS feed articles
    for feed_url in RSS_FEEDS:
        all_articles.extend(get_articles_from_rss(feed_url))

    # Get arXiv articles
    all_articles.extend(get_articles_from_arxiv())

    return all_articles
