# You must provide several options such as search by string, hashtag,  and user at the minimum.
from pymongo import MongoClient
import mysql.connector
print("Please enter a search term in string, hashtag, and user: ")
search_term = input()
if search_term == "string":
    print("Please enter a string: ")
    string = input()
    
    client = MongoClient('localhost', 27017)
    db = client['tweet']
    collection_currency = db['tweet']
    myquery = { "text": string }
    mydoc = collection_currency.find(myquery)
    for x in mydoc:
        print(x)
elif search_term == "hashtag":
    print("Please enter a hashtag: ")
    hashtag = input()
    client = MongoClient('localhost', 27017)
    db = client['tweet']
    collection_currency = db['tweet']
    myquery = {"entities.hashtags":{$exists: true,"$not":{"$size":0}}}
    mydoc = collection_currency.find(myquery)
    if is.empty(mydoc):
        print("there are no hashtag in the dataset so we do not search.")
    else:
        for x in mydoc:
            print(x)
elif search_term == "user":
    print("Please enter a user name: ")
    user = input()
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="135790"
    )

    mycursor = mydb.cursor()
    mycursor.execute('SELECT * FROM pqr_user.tusers WHERE name = "'+user+'"')
    myresult = mycursor.fetchall()
    for x in myresult:
        print(x)
