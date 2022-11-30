import requests
import TwitterSecrets
import caching
from bs4 import BeautifulSoup
import re

bearer_token = TwitterSecrets.Bearer_token
PAGECACHE=caching.openCache('pages.json')
USERCACHE=caching.openCache('username.json')
INFOCACHE=caching.openCache('twitter.json')

def getTwitterUsername(url,name):
    wikiLinkList=[]
    username=[]
    if name in PAGECACHE:
        html_text=PAGECACHE[name]
    else:
        html_text=requests.get(url).text
        PAGECACHE[name]=html_text
        caching.writeCache(PAGECACHE,'pages.json')
    soup1=BeautifulSoup(html_text,'html.parser')
    castList=soup1.find_all('div',class_='div-col')
    for item in castList:
        text=str(item)
        soup2=BeautifulSoup(text,'html.parser')
        for link in soup2.find_all('a',href=True):
            personName=link.contents[0]
            if personName in USERCACHE and USERCACHE[personName] is not None:
                username.append([personName,USERCACHE[personName]])
            elif personName in USERCACHE and USERCACHE[personName] is None:
                continue
            else:
                wikiLinkList.append([personName,'https://en.wikipedia.org'+str(link['href'])])
    for link in wikiLinkList:
        flag=0
        newpage=requests.get(link[1]).text
        soup3=BeautifulSoup(newpage,'html.parser')
        listofa=soup3.find_all('a',recursive=True)
        for item in listofa:
            text=str(item)
            if re.search('https://twitter.com/',text):
                twitterUrl=item['href']
                if re.search('^https://twitter.com/',twitterUrl):
                    twitterPage=twitterUrl.split('/')
                    twitterUsername=twitterPage[twitterPage.index('twitter.com')+1]
                    username.append([str(link[0]),twitterUsername])
                    USERCACHE[str(link[0])]=twitterUsername
                    caching.writeCache(USERCACHE,'username.json')
                    flag=1
                    break
        if flag==0:
            USERCACHE[str(link[0])]=None
            caching.writeCache(USERCACHE,'username.json')
    return username

def create_url(username):
    names = "usernames="+username
    user_fields = "user.fields=description,created_at,id,location,name,profile_image_url"
    # User fields are adjustable, options include:
    # created_at, description, entities, id, location, name,
    # pinned_tweet_id, profile_image_url, protected,
    # public_metrics, url, username, verified, and withheld
    url = "https://api.twitter.com/2/users/by?{}&{}".format(names, user_fields)
    return url

def bearer_oauth(r):
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2UserLookupPython"
    return r

def connect_to_endpoint(url):
    response = requests.request("GET", url, auth=bearer_oauth,)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()

def getFollowing(userID,infoDict):
    print('called')
    nameList=[]
    if userID in INFOCACHE:
        nameList=INFOCACHE[userID].copy()
        for username in nameList:
            if username in INFOCACHE:
                infoDict[username]=INFOCACHE[username]
            else:
                url = create_url(username)
                json_response = connect_to_endpoint(url)
                infoDict[username]=json_response['data'][0]
                INFOCACHE[username]=json_response['data'][0]
                caching.writeCache(INFOCACHE,'twitter.json')
    else:
        url="https://api.twitter.com/2/users/{}/following".format(userID)
        params={"user.fields": "description,created_at,id,location,name,profile_image_url"}
        response = requests.request("GET", url, auth=bearer_oauth, params=params)
        if response.status_code != 200:
            raise Exception(
                "Request returned an error: {} {}".format(
                    response.status_code, response.text
                )
            )
        json_response=response.json()
        for following in json_response['data']:
            nameList.append(following['username'])
            infoDict[following['username']]=following
            INFOCACHE[following['username']]=following
            caching.writeCache(INFOCACHE,'twitter.json')
        INFOCACHE[userID]=nameList.copy()
        caching.writeCache(INFOCACHE,'twitter.json')
    return nameList

def getTwitterInfo(usernames):
    infoDict={}
    for username in usernames:
        if username[1] in INFOCACHE:
            infoDict[username[1]]=INFOCACHE[username[1]]
            try:
                INFOCACHE[username[1]]['following']==None
            except KeyError:
                infoDict[username[1]]['following']=getFollowing(int(infoDict[username[1]]['id']),infoDict)
                INFOCACHE[username[1]]=infoDict[username[1]]
                caching.writeCache(INFOCACHE,'twitter.json')
            for name in infoDict[username[1]]['following']:
                if name in INFOCACHE:
                    infoDict[name]=INFOCACHE[name]
                else:
                    url = create_url(name)
                    json_response = connect_to_endpoint(url)
                    infoDict[name]=json_response['data'][0]
                    INFOCACHE[name]=json_response['data'][0]
                    caching.writeCache(INFOCACHE,'twitter.json')
        else:
            url = create_url(username[1])
            json_response = connect_to_endpoint(url)
            json_response['data'][0]['following']=getFollowing(int(json_response['data'][0]['id']),infoDict)
            infoDict[username[1]]=json_response['data'][0]
            INFOCACHE[username[1]]=json_response['data'][0]
            caching.writeCache(INFOCACHE,'twitter.json')
    return infoDict

def main():
    BoB=getTwitterUsername('https://en.wikipedia.org/wiki/Band_of_Brothers_(miniseries)','band of brothers')
    SPR=getTwitterUsername('https://en.wikipedia.org/wiki/Saving_Private_Ryan','saving private ryan')
    BH=getTwitterUsername('https://en.wikipedia.org/wiki/Braveheart','braveheart')
    MM=getTwitterUsername('https://en.wikipedia.org/wiki/Mad_Max:_Fury_Road','mad max')
    GWH=getTwitterUsername('https://en.wikipedia.org/wiki/Good_Will_Hunting','good will hunting')
    res1=getTwitterInfo(BoB)
    res2=getTwitterInfo(SPR)
    res3=getTwitterInfo(BH)
    res4=getTwitterInfo(MM)
    res5=getTwitterInfo(GWH)
    print(res1)
    

if __name__ == "__main__":
    main()