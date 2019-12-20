import feedparser

feed = feedparser.parse('https://unity3d.com/unity/lts-releases.xml')

latest = feed.entries[0]['summary_detail']['value']

print(latest)
