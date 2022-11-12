from turtle import title
import re
import datetime
from credentials import token, client_secret, client_id, password, user_name, user_agent, keywords
from constants import url_extract_pattern, url_extract_pattern2, url_extract_pattern_no_http, domain_expression, cve_expression
import facebook
import pandas as pd
import csv
import praw
import iocextract
from prawcore.exceptions import Forbidden
from convert import listToString, convertTime
from api import searchCVE, searchDomain

reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    password=password,
    user_agent=user_agent,
    username=user_name,
)
data = []
header = ['id', 'name', 'title', 'content', 'IOC', 'reddit Url',
          'url', 'created_date']
count = 0
count1 = 0


posts = []

selectedMonth = 10
selectedYear = 2021

# help(reddit.subreddit('all').search())
for keys in keywords:
    try:
        for submission in reddit.subreddit('all').search(keys, limit=None, ):

            if any(ele in submission.title for ele in keywords):

                url = list(iocextract.extract_urls(
                    submission.selftext,))
                # print(url)
                url = listToString(list(set(url)))
                url = str.splitlines(url)
                url = listToString(list(set(url)))

                ip = list(iocextract.extract_ips(
                    submission.selftext))
                ip = listToString(list(set(ip)))
                ip = str.splitlines(ip)
                ip = listToString(list(set(ip)))

                ipv4 = list(iocextract.extract_ipv4s(
                    submission.selftext, refang=True))

                ipv4 = listToString(list(set(ipv4)))
                ipv4 = str.splitlines(ipv4)
                ipv4 = listToString(list(set(ipv4)))

                ipv6 = list(iocextract.extract_ipv6s(submission.selftext))
                ipv6 = listToString(list(set(ipv6)))
                ipv6 = str.splitlines(ipv6)
                ipv6 = listToString(list(set(ipv6)))

                hashes = list(iocextract.extract_hashes(submission.selftext))
                hashes = listToString(list(set(hashes)))
                hashes = str.splitlines(hashes)
                hashes = listToString(list(set(hashes)))

                cves = searchCVE(cve_expression, submission.selftext)
                cves = listToString(list(set(cves)))
                cves = str.splitlines(cves)
                cves = listToString(list(set(cves)))

                domains = searchDomain(domain_expression, submission.selftext)
                domains = listToString(list(set(domains)))
                domains = str.splitlines(domains)
                domains = listToString(list(set(domains)))

                total_ioc = list(
                    set([url, ip, ipv4, ipv6, hashes, cves, domains]))
                total_ioc = str.splitlines(listToString(total_ioc))

                month = datetime.datetime.utcfromtimestamp(
                    submission.created).month
                year = datetime.datetime.utcfromtimestamp(
                    submission.created).year
                
                if year == 2021 or year == 2022:
                    data.append([submission.id, submission.name, submission.title, submission.selftext, total_ioc, 'https://reddit.com' +
                                submission.permalink, submission.url, datetime.datetime.utcfromtimestamp(submission.created)])
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
