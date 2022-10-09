import json

hashdict=dict()
data=[]
reader = open("output#0.jsonl", 'r', encoding='utf-8')
for line in reader:
    data.append(json.loads(line))

for tweet in data:
    if tweet["hashtags"] == "null" or tweet["hashtags"] is None:
        continue
    for hashtag in tweet["hashtags"]:
        if hashtag in hashdict:
            hashdict[hashtag]+=1
        else:
            hashdict[hashtag]=1

hashdict= sorted(hashdict.items(), key=lambda x: x[1], reverse=True)
iterator = iter(hashdict)
for i in range(10):
    print(next(iterator))
