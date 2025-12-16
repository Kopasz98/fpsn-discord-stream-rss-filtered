import feedparser
import requests
import json
import os
import hashlib

WEBHOOK_URL = os.environ["DISCORD_WEBHOOK"]

RSS_FEEDS = [
"https://www.dexerto.com/feed/",
"https://dotesports.com/feed",
"https://streamerbans.com/rss",
"https://www.theverge.com/creators/rss/index.xml",
"https://www.polygon.com/rss/index.xml",
"https://insider-gaming.com/feed/",
"https://gamerant.com/feed/",
"https://www.pcgamer.com/rss/",
"https://kotaku.com/rss",
"https://www.gamesradar.com/rss/",

"https://twitchtracker.com/blog/rss",
"https://sullygnome.com/articles/rss",
"https://www.twitchmetrics.net/blog/rss",
"https://streamernews.live/rss",
"https://blog.twitch.tv/en/feed/",
"https://www.streamscheme.com/feed/",
"https://nerdordie.com/blog/feed/",
"https://www.own3d.tv/blog/feed/",
"https://blog.streamlabs.com/rss",
"https://golightstream.com/blog/rss",

"https://www.tubefilter.com/feed/",
"https://socialblade.com/blog/feed",
"https://blog.youtube/rss.xml",
"https://www.youtube.com/creatorinsider/rss",
"https://vidiq.com/blog/rss/",
"https://blog.hootsuite.com/feed/",
"https://later.com/blog/rss/",
"https://influencermarketinghub.com/feed/",

"https://blog.kick.com/rss",
"https://streamernews.live/rss",
"https://www.dexerto.com/feed/",
"https://dotesports.com/feed",
"https://afkgaming.com/rss",

"https://esportsinsider.com/feed",
"https://www.esports.net/feed/",
"https://upcomer.com/feed/",
"https://ggrecon.com/feed/",
"https://www.theloadout.com/feed",
"https://win.gg/feed/",
"https://siege.gg/rss",

"https://passionfru.it/feed/",
"https://thepublishpress.com/feed/",
"https://signalfire.com/blog/feed/",
"https://www.morningbrew.com/creator-economy/rss",
"https://influencermarketinghub.com/feed/",
"https://www.businessinsider.com/rss",
"https://www.forbes.com/creators/feed/",

"https://blog.twitch.tv/en/feed/",
"https://blog.youtube/rss.xml",
"https://blog.kick.com/rss",
"https://obsproject.com/blog/rss",
"https://blog.streamlabs.com/rss",
"https://discord.com/blog/rss",

"https://esport1.hu/rss",
"https://www.gamestar.hu/rss",
"https://www.pcguru.hu/rss",
"https://hu.ign.com/rss",
"https://refresher.hu/rss",

]

INCLUDE_KEYWORDS = [k.lower() for k in [
  "Twitch","Youtube","Kik",
]]

EXCLUDE_KEYWORDS = [k.lower() for k in [
    "rumor", "leak", "unconfirmed",
    "giveaway", "free skins",
    "sale", "discount",
    "top 10", "best of",
    "opinion", "editorial","ban","esport",
]]

POSTED_FILE = "posted.json"


def is_relevant(entry):
    text = (
        entry.get("title", "") +
        " " +
        entry.get("summary", "")
    ).lower()

    if not any(keyword in text for keyword in INCLUDE_KEYWORDS):
        return False

    if any(keyword in text for keyword in EXCLUDE_KEYWORDS):
        return False

    return True


def entry_id(entry):
    base = entry.get("id") or entry.get("link") or entry.get("title", "")
    return hashlib.sha256(base.encode("utf-8")).hexdigest()


if os.path.exists(POSTED_FILE):
    with open(POSTED_FILE, "r") as f:
        posted = set(json.load(f))
else:
    posted = set()

new_posts = []

for feed_url in RSS_FEEDS:
    feed = feedparser.parse(feed_url)

    for entry in feed.entries[:5]:
        if not is_relevant(entry):
            continue

        eid = entry_id(entry)
        if eid in posted:
            continue

        new_posts.append({
            "title": entry.title,
            "link": entry.link
        })

        posted.add(eid)

for post in new_posts:
    data = {
        "content": f"🎮 **{post['title']}**\n{post['link']}"
    }
    requests.post(WEBHOOK_URL, json=data)

with open(POSTED_FILE, "w") as f:
    json.dump(list(posted), f)
