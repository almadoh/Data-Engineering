from twitter import TwitterSearchScraper

tweets_list = []
f = open("output#3.json", "a")
try:
    for i, tweet in enumerate(
            TwitterSearchScraper('Artificial Intelligence since:2022-01-01 until:2022-06-11').get_items()):
        if i > 10000000:
            break
        if i % 1000 == 0:
            print(i)
        tweets_list.append(tweet.json())
        if len(tweets_list) == 10000:
            for record in tweets_list:
                f.write(record + "\n")
            tweets_list = []
finally:
    f.close()