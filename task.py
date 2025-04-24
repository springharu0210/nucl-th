# #!/usr/bin/env python3
# """
# 過去1時間以内の arXiv nucl-th 論文を Discord に通知する。
# """
# import os, datetime, textwrap, requests, feedparser

# ARXIV = ("http://export.arxiv.org/api/query?"
#          "search_query=cat:nucl-th"
#          "&sortBy=submittedDate&sortOrder=descending"
#          "&max_results=20")

# WEBHOOK = os.environ["DISCORD"]

# utc_now = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
# #one_hour_ago = utc_now - datetime.timedelta(hours=1)
# one_hour_ago = utc_now - datetime.timedelta(hours=12)  # ← ここを1→12に変更

# feed = feedparser.parse(ARXIV)
# for entry in feed.entries:
#     updated = datetime.datetime.strptime(
#         entry.updated, "%Y-%m-%dT%H:%M:%SZ"
#     ).replace(tzinfo=datetime.timezone.utc)

#     if updated < one_hour_ago:
#         break

#     embed = {
#         "title": entry.title.strip(),
#         "url": entry.id,
#         "description": textwrap.shorten(
#             " ".join(entry.summary.split()), width=180, placeholder="…"),
#         "footer": {"text": updated.strftime("%Y-%m-%d %H:%M UTC")}
#     }
#     requests.post(WEBHOOK, json={"embeds": [embed]})
#!/usr/bin/env python3
"""
nucl-th カテゴリの新着論文（12時間以内）を Discord に通知する。
ログ出力つきデバッグバージョン。
"""

import os, datetime, textwrap, requests, feedparser

# ARXIV = ("http://export.arxiv.org/api/query?"
#          "search_query=cat:nucl-th"
#          "&sortBy=submittedDate&sortOrder=descending"
#          "&max_results=20")
ARXIV = ("http://export.arxiv.org/api/query?"
         "search_query=cat:nucl-th"
         "&sortBy=lastUpdatedDate&sortOrder=descending"
         "&max_results=20")


WEBHOOK = os.environ.get("DISCORD")
if not WEBHOOK:
    print("❌ DISCORD webhook URL が環境変数に設定されていません")
    exit(1)

utc_now = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
one_hour_ago = utc_now - datetime.timedelta(hours=12)
#one_hour_ago = utc_now - datetime.timedelta(days=2)


print(f"🔍 UTC now: {utc_now}")
print(f"⏳ Checking arXiv entries since: {one_hour_ago}")

feed = feedparser.parse(ARXIV)
print(f"📚 Found {len(feed.entries)} entries")

count = 0
for entry in feed.entries:
    updated = datetime.datetime.strptime(
        entry.updated, "%Y-%m-%dT%H:%M:%SZ"
    ).replace(tzinfo=datetime.timezone.utc)

    print(f"📝 {entry.title.strip()} — updated: {updated}")
    if updated < one_hour_ago:
        print("⏭️ too old, skipping")
        break

# 要約（summary）を全文そのまま表示（HTML → プレーンテキスト整形）
    raw_summary = entry.summary
    clean_summary = " ".join(raw_summary.split())  # 改行や連続スペースを除去
    embed = {
    "title": entry.title.strip(),
    "url": entry.id,
    "description": clean_summary,
    "footer": {"text": updated.strftime("%Y-%m-%d %H:%M UTC")}
    }

    # embed = {
    #     "title": entry.title.strip(),
    #     "url": entry.id,
    #     "description": textwrap.shorten(
    #         " ".join(entry.summary.split()), width=180, placeholder="…"),
    #     "footer": {"text": updated.strftime("%Y-%m-%d %H:%M UTC")}
    # }

    #resp = requests.post(WEBHOOK, json={"embeds": [embed]})
    resp = requests.post(WEBHOOK, json={"embeds": [embed]})
    print(f"📤 Sent to Discord → Status code: {resp.status_code}")
    if resp.status_code != 204:
        print(f"❗ Error response: {resp.text}")
    print(f"📤 Sent to Discord → Status code: {resp.status_code}")
    if resp.status_code != 204:
        print(f"❗ Error response: {resp.text}")
    count += 1
print(f"✅ Notification completed. Total sent: {count}")

