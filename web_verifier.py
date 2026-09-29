import os
import requests
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")


# ============================================================
# NEWS API SEARCH
# ============================================================

def search_news_api(query):

    if not NEWS_API_KEY:
        return []

    try:

        url = "https://newsapi.org/v2/everything"

        headers = {
            "X-Api-Key": NEWS_API_KEY
        }

        params = {
            "q": query,
            "language": "en",
            "sortBy": "relevancy",
            "pageSize": 5
        }

        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=15
        )

        if response.status_code != 200:
            print(
                "NewsAPI error:",
                response.text
            )
            return []

        data = response.json()

        articles = []

        for article in data.get(
            "articles",
            []
        ):

            articles.append({
                "title": article.get(
                    "title",
                    ""
                ),
                "url": article.get(
                    "url",
                    ""
                ),
                "source": article.get(
                    "source",
                    {}
                ).get(
                    "name",
                    ""
                ),
                "description": article.get(
                    "description",
                    ""
                )
            })

        return articles

    except Exception as error:

        print(
            "NewsAPI exception:",
            error
        )

        return []


# ============================================================
# PERPLEXITY SEARCH
# ============================================================

def search_perplexity(claim):

    if not PERPLEXITY_API_KEY:
        return {
            "answer": "",
            "sources": []
        }

    try:

        url = "https://api.perplexity.ai/v1/sonar"

        headers = {
            "Authorization":
                f"Bearer {PERPLEXITY_API_KEY}",

            "Content-Type":
                "application/json"
        }

        payload = {

            "model": "sonar",

            "messages": [

                {
                    "role": "system",

                    "content":
                        "You are a factual verification "
                        "research assistant. "
                        "Use current web evidence. "
                        "Do not guess. "
                        "If reliable evidence is insufficient, "
                        "say so explicitly."
                },

                {
                    "role": "user",

                    "content":
                        f"Verify this factual claim:\n\n"
                        f"{claim}\n\n"

                        "Find reliable and recent evidence. "
                        "Explain whether the claim is supported, "
                        "contradicted, or cannot be established. "
                        "Prefer official sources and reputable "
                        "news organizations."
                }

            ]
        }

        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=30
        )

        if response.status_code != 200:

            print(
                "Perplexity error:",
                response.text
            )

            return {
                "answer": "",
                "sources": []
            }

        data = response.json()

        answer = ""

        choices = data.get(
            "choices",
            []
        )

        if choices:

            answer = choices[0].get(
                "message",
                {}
            ).get(
                "content",
                ""
            )

        sources = []

        for item in data.get(
            "search_results",
            []
        ):

            sources.append({
                "title": item.get(
                    "title",
                    "Source"
                ),
                "url": item.get(
                    "url",
                    ""
                ),
                "date": item.get(
                    "date",
                    ""
                )
            })

        return {
            "answer": answer,
            "sources": sources
        }

    except Exception as error:

        print(
            "Perplexity exception:",
            error
        )

        return {
            "answer": "",
            "sources": []
        }


# ============================================================
# COMBINED WEB VERIFICATION
# ============================================================

def verify_claim_online(claim):

    print(
        "\n🌐 Searching online evidence..."
    )

    news_results = search_news_api(
        claim
    )

    print(
        "📰 NewsAPI results:",
        len(news_results)
    )

    perplexity_result = search_perplexity(
        claim
    )

    print(
        "🔎 Perplexity search completed."
    )

    # Combine sources

    sources = []

    for article in news_results:

        if article.get("url"):

            sources.append({
                "title":
                    article.get(
                        "title",
                        "News Article"
                    ),

                "url":
                    article.get(
                        "url",
                        ""
                    )
            })

    for source in perplexity_result.get(
        "sources",
        []
    ):

        if source.get("url"):

            sources.append({
                "title":
                    source.get(
                        "title",
                        "Web Source"
                    ),

                "url":
                    source.get(
                        "url",
                        ""
                    )
            })

    # Remove duplicate URLs

    unique_sources = []

    seen_urls = set()

    for source in sources:

        url = source.get(
            "url",
            ""
        )

        if (
            url
            and url not in seen_urls
        ):

            seen_urls.add(url)

            unique_sources.append(
                source
            )

    return {

        "news_articles":
            news_results,

        "perplexity_answer":
            perplexity_result.get(
                "answer",
                ""
            ),

        "sources":
            unique_sources[:10]
    }
if __name__ == "__main__":

    result = verify_claim_online(
        "The Supreme Court of India banned NCERT textbooks."
    )

    print("\n==============================")
    print("PERPLEXITY ANSWER")
    print("==============================")

    print(
        result["perplexity_answer"]
    )

    print("\n==============================")
    print("SOURCES")
    print("==============================")

    for source in result["sources"]:

        print(
            source["title"]
        )

        print(
            source["url"]
        )

        print()
