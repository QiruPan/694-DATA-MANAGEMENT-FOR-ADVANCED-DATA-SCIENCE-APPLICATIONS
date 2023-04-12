import json

with open('data.json') as f:
    file_data = json.load(f)

# hashmap from id to data
dict={}
for i in file_data:
    dict[i['id']]=i
print("dict len: ", len(dict))
# count retweet number
retweet_count={}
count=0
for i in file_data:
    if "retweeted_status" in i:
        count+=1
        if i["retweeted_status"]["id"] in retweet_count:
            retweet_count[i["retweeted_status"]["id"]]+=1
        else:
            retweet_count[i["retweeted_status"]["id"]]=1

# count like number and add retweet like to parent like
print("retweeted_count len: ", len(retweet_count))
print("count: ", count)
while len(retweet_count)>0:
    for i in file_data:
        if i["id"] not in retweet_count:
            if "retweeted_status" in i:
                parent=i["retweeted_status"]["id"]
                if parent in retweet_count:
                    retweet_count[parent]-=1
                    if retweet_count[parent]==0:
                        del retweet_count[parent]
                    if parent in dict:
                        dict[parent]["favorite_count"]+=i["favorite_count"]

print("Finished")