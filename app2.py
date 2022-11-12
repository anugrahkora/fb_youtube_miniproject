from http.client import FORBIDDEN
from psaw import PushshiftAPI
from datetime import datetime, timezone, timedelta
from dateutil.relativedelta import relativedelta
from credentials import keywords
import datetime
import csv
import iocextract
from convert import listToString
from api import searchCVE, searchDomain
from constants import url_extract_pattern, url_extract_pattern2, url_extract_pattern_no_http, domain_expression, cve_expression

years_back = 10
start_epoch = int(datetime.datetime(2022, 1, 1).timestamp())
datetime = datetime.datetime.now()
timestamp = int(datetime.replace(tzinfo=timezone.utc).timestamp())
header = ['id', 'name', 'title', 'content', 'IOC', 'reddit Url',
          'url', 'created_date']
data = []
api = PushshiftAPI()

count = 0
for keys in keywords:

    submissions = api.search_submissions(after=start_epoch,
                                         q=keys,
                                         filter=['url', 'author',
                                                 'title', 'subreddit', 'selftext'],
                                         )

    for post in submissions:
        if any(ele in post.title for ele in keywords):
            month = datetime.utcfromtimestamp(
                post.created).month
            year = datetime.utcfromtimestamp(
                post.created).year
            title = post.title
            try:
                body = post.selftext
                url = list(iocextract.extract_urls(
                    post.selftext,))
                # print(url)
                url = listToString(list(set(url)))
                url = str.splitlines(url)
                url = listToString(list(set(url)))

                ip = list(iocextract.extract_ips(
                    post.selftext))
                ip = listToString(list(set(ip)))
                ip = str.splitlines(ip)
                ip = listToString(list(set(ip)))

                ipv4 = list(iocextract.extract_ipv4s(
                    post.selftext, refang=True))

                ipv4 = listToString(list(set(ipv4)))
                ipv4 = str.splitlines(ipv4)
                ipv4 = listToString(list(set(ipv4)))

                ipv6 = list(iocextract.extract_ipv6s(post.selftext))
                ipv6 = listToString(list(set(ipv6)))
                ipv6 = str.splitlines(ipv6)
                ipv6 = listToString(list(set(ipv6)))

                hashes = list(iocextract.extract_hashes(post.selftext))
                hashes = listToString(list(set(hashes)))
                hashes = str.splitlines(hashes)
                hashes = listToString(list(set(hashes)))

                cves = searchCVE(cve_expression, post.selftext)
                cves = listToString(list(set(cves)))
                cves = str.splitlines(cves)
                cves = listToString(list(set(cves)))

                domains = searchDomain(domain_expression, post.selftext)
                domains = listToString(list(set(domains)))
                domains = str.splitlines(domains)
                domains = listToString(list(set(domains)))

                total_ioc = list(
                    set([url, ip, ipv4, ipv6, hashes, cves, domains]))
                total_ioc = str.splitlines(listToString(total_ioc))

                if year == 2021:
                    data.append([post.id, post.name, title, body, total_ioc, 'https://reddit.com' +
                                post.permalink, post.url, datetime.utcfromtimestamp(post.created)])
                    count += 1
                    print(count)
            except Exception as e:
                body = ''
            subreddit = post.subreddit
            # print(subreddit.selftext)
            # print(f'{c}: {title} - {body} - {subreddit}')
with open('reddit2.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)

    # write the header
    writer.writerow(header)

    # write the data
    writer.writerows(data)
