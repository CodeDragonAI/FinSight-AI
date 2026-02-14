import requests

def get_crypto_news():
    url = "https://min-api.cryptocompare.com/data/v2/news/?lang=EN"
    response = requests.get(url)
    data = response.json()

    articles = data.get("Data", [])[:3]

    news_summary = "\n".join(
        f"- {article['title']}" for article in articles
    )

    return news_summary
