from operator import itemgetter

import requests

import plotly.express as px

# Make an API call and check the response.
url = 'https://hacker-news.firebaseio.com/v0/topstories.json'
r = requests.get(url)
print(f"Status code: {r.status_code}")

# Process information about each submission.
submission_ids = r.json()

submission_dicts = []
for submission_id in submission_ids[:5]:
    # Make a new API call for each submission.
    url = f"https://hacker-news.firebaseio.com/v0/item/{submission_id}.json"
    r = requests.get(url)
    print(f"id: {submission_id}\tstatus: {r.status_code}")
    response_dict = r.json()
    
    # Build a dictionary for each article.
    submission_dict = {
        'title': response_dict['title'],
        'hn_link': f"https://news.ycombinator.com/item?id={submission_id}",
        'comments': response_dict['descendants'],
    }
    submission_dicts.append(submission_dict)

submission_dicts = sorted(submission_dicts, key=itemgetter('comments'),
                            reverse=True)

for submission_dict in submission_dicts:
    print(f"\nTitle: {submission_dict['title']}")
    print(f"Discussion link: {submission_dict['hn_link']}")
    print(f"Comments: {submission_dict['comments']}")


article_link, comments, hover_texts = [], [], []
for s_dict in submission_dicts:
    a = s_dict["title"]
    b = s_dict["comments"]
    c = s_dict["hn_link"]
    d = f"<a href='{c}'>{a}</a>"
    article_link.append(d)
    comments.append(b)
    hover_texts.append(a)



# Make visualization.
title = "Most Active Discussions on Hacker News"
labels = {'x': 'Article', 'y': 'Comments'}
fig = px.bar(x=article_link, y=comments, title=title, 
             labels=labels, hover_name=hover_texts)

fig.update_layout(title_font_size=28, xaxis_title_font_size=20,
        yaxis_title_font_size=20)

fig.update_traces(marker_color='LightGoldenRodYellow', marker_opacity=0.5)

fig.show()