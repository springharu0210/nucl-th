#!/usr/bin/env python3
"""
過去1時間以内の arXiv nucl-th 論文を Discord に通知する。
"""
import os, datetime, textwrap, requests, feedparser

ARXIV = ("http://export.arxiv.org/api/query?"
         "search_query=cat:nucl-th"
         "&sortBy=submittedDate&sortOrder=descending"
         "&max_results=20")

WEBHOOK = os.environ["DISCORD"]

utc_now = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
#one_hour_ago = utc_now - datetime.timedelta(hours=1)
one_hour_ago = utc_now - datetime.timedelta(hours=12)  # ← ここを1→12に変更

feed = feedparser.parse(ARXIV)
for entry in feed.entries:
    updated = datetime.datetime.strptime(
        entry.updated, "%Y-%m-%dT%H:%M:%SZ"
    ).replace(tzinfo=datetime.timezone.utc)

    if updated < one_hour_ago:
        break

    embed = {
        "title": entry.title.strip(),
        "url": entry.id,
        "description": textwrap.shorten(
            " ".join(entry.summary.split()), width=180, placeholder="…"),
        "footer": {"text": updated.strftime("%Y-%m-%d %H:%M UTC")}
    }
    requests.post(WEBHOOK, json={"embeds": [embed]})

