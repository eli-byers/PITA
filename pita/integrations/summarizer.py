# Implements the summarize_articles() function to create summaries of the important points in a list of articles.

from typing import List

import openai


def summarize_url(url: str) -> str:
    prompt = f"Please provide a summary of the following webpage: {url}"

    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    )

    summary = response.choices[0].text.strip()
    return summary


def summarize_links(links: List[str]) -> List[str]:
    summaries = []
    for link in links:
        summary = summarize_url(link)
        summaries.append(summary)

    return summaries

# Example usage
# links = [
#     "https://example.com/article1",
#     "https://example.com/article2",
#     "https://example.com/article3",
# ]
# print(summarize_links(links))
