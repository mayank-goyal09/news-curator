# app/core/sources.py
# RSS sources organized by category for the 5 main categories

CATEGORIES = {
    "satire": {
        "label": "Satire",
        "sources": [
            {"id": "theonion", "name": "The Onion", "feed_url": "https://www.theonion.com/rss"},
            {"id": "bbcnews", "name": "BBC News (Odd)", "feed_url": "https://feeds.bbci.co.uk/news/rss.xml"},
        ]
    },
    "ai": {
        "label": "AI Technology",
        "sources": [
            {"id": "ai_news", "name": "AI News", "feed_url": "https://www.artificialintelligence-news.com/feed/"},
            {"id": "techcrunch", "name": "TechCrunch", "feed_url": "https://techcrunch.com/feed/"},
            {"id": "wired", "name": "Wired", "feed_url": "https://www.wired.com/feed/rss"},
        ]
    },
    "worldwide": {
        "label": "Worldwide News",
        "sources": [
            {"id": "bbc_world", "name": "BBC World", "feed_url": "https://feeds.bbci.co.uk/news/world/rss.xml"},
            {"id": "reuters", "name": "Reuters World", "feed_url": "https://www.reutersagency.com/feed/"},
        ]
    },
    "warming": {
        "label": "Warming & Emotions",
        "sources": [
            {"id": "goodnews", "name": "Good News Network", "feed_url": "https://www.goodnewsnetwork.org/feed/"},
            {"id": "positive", "name": "Positive News", "feed_url": "https://www.positive.news/feed/"},
        ]
    },
    "market": {
        "label": "Market News",
        "sources": [
            {"id": "cnbc", "name": "CNBC", "feed_url": "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=100003114"},
            {"id": "marketwatch", "name": "MarketWatch", "feed_url": "https://feeds.marketwatch.com/marketwatch/topstories/"},
        ]
    },
}

# Flat list for backward compatibility
SOURCES = []
for cat_key, cat_data in CATEGORIES.items():
    for src in cat_data["sources"]:
        src_copy = dict(src)
        src_copy["category"] = cat_key
        SOURCES.append(src_copy)
