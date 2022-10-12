from turtle import title
from credentials import token, client_secret, client_id, password, user_name, user_agent, keywords
import facebook
import csv
import praw
from prawcore.exceptions import Forbidden
from convert import listToString

reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    password=password,
    user_agent=user_agent,
    username=user_name,
)
data = []
header = ['id', 'name', 'title', 'score', 'url', 'created_time']
count = 0

for keys in keywords:
    try:
        for submission in reddit.subreddit("all").search(listToString(keys), limit=None):

            data.append([submission.id, submission.name, submission.title,
                        submission.score, submission.url,  submission.created_utc])
            count += 1
            print(count)
    except Forbidden:
        print("We\'ve been banned on "+listToString(keys))



with open('reddit.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)

    # write the header
    writer.writerow(header)

    # write the data
    writer.writerows(data)
 






# print(len(titles))
# postIds = ['5302983239800416', '1178170342746546']
# fetchedDescriptions = []
# graph = facebook.GraphAPI(access_token=token, version=2.0)


# for posts in postIds:
#     res = graph.request("/5302983239800416")
#     fetchedDescriptions.append(res)

# print(fetchedDescriptions[0]['description'])


# events = graph.request('search', {'q': 'aquafresh', 'type': 'page'})
# data = facebook.GraphAPI(access_token=token, version=2.0).bare_request(url="https://www.facebook.com/")
# print(data)
# # eventList = events["data"]
# # eventid = eventList[1]["id"]
# # print(eventid)
# res=requests.get("https://graph.facebook.com/search?access_token=" +token + "&q=" + query + "&type=page")
# res = requests.get(
#     "https://developers.facebook.com/tools/explorer/?method=GET&path=5302983239800416&fields=description&version=v15.0")

# print(res.content)
