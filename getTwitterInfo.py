import requests
import TwitterSecrets
import caching
from bs4 import BeautifulSoup
import re

bearer_token = TwitterSecrets.Bearer_token #bearer token used in Twitter API.
PAGECACHE=caching.openCache('pages.json') # Data cache that stores the html scripts from the wikipedia pages. Save time in requests.get
USERCACHE=caching.openCache('username.json') # Data cache that stores the Twitter usernames of the TV work contributors. Save time in requests.get
INFOCACHE=caching.openCache('twitter.json') # Data cache that stores the retrieved data using Twitter API. At the same time, store the data to be inserted into the data structure. Save time in API data lookup.

def getTwitterUsername(url,name):
    '''
    inputs: the url of the wikipedia pages of TV works (string); the name of the TV work (string).
    output: a list of lists. For each element, which is a list, has a shape of [<Full name of contributor>,<Twitter Username>].
    The function will use the url to retrieve the html scripts of the TV work wiki page. If already retrieved before, data will be read from cache.
    Beautifulsoup will find the cast list and extract the full names of contributors and the links to their personal wiki pages.
    If the person has been extracted before, data will be read from cache.
    The links to their personal wiki pages will be used again to retrieve the html scripts of the contributor wiki page. If already retrieved before, data will be read from cache.
    Beautifulsoup will find all links in the page.
    re library and regular expressions are used to find all the links starting with Twitter urls.
    The usernames can be found after "https://www.twitter.com/". In this way, the username of the contributor is found.
    Given the full names (obtained with BeautifulSoup) and the usernames (obtained with re), the output list can be generated.
    '''
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
    '''
    Input: Twitter username (string)
    output: a URL to look up with Twitter API (string).
    The function is used to generate a look-up URL for Twitter API.
    All the attributes in user_fields will be obtained with Twitter API.
    '''
    names = "usernames="+username
    user_fields = "user.fields=description,created_at,id,location,name,profile_image_url"
    # User fields are adjustable, options include:
    # created_at, description, entities, id, location, name,
    # pinned_tweet_id, profile_image_url, protected,
    # public_metrics, url, username, verified, and withheld
    url = "https://api.twitter.com/2/users/by?{}&{}".format(names, user_fields)
    return url

def bearer_oauth(r):
    '''
    The function is used to pass the Twitter API v2 with OAuth authorization. Bearer token is used.
    '''
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2UserLookupPython"
    return r

def connect_to_endpoint(url):
    '''
    Input: URL to be used in Twitter API (string).
    Output: a dictionary that includes the data retrived with Twitter API.
    '''
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
    '''
    Input: the Twitter User ID to be used in following lookup with Twitter API (string). A dictionary that includes all the data to be inserted into the data structure.
    In the dictionary, the key is the username of a Twitter user. The value is a dictionary that includes all information of that user.
    Output: A list that includes 100 (max) usernames that the user with userID (input) follows.
    The function is an integration of several functions: create_url, bearer_oauth, connect_to_endpoint, and the main body of getFollowing.
    The function will use Twitter API to look up the users that a user is following. If the userID has already been looked up before, the data will be read from cache.
    The retrieved following list will be added as a value with a key of: "followinig" in the value dictionary with the key of the target username.
    (With the userID, a list containing at most 100 following users will be retrieved with Twitter API and added into infoDict. The input userID corresponds to a unique
    username. This username is found. Then, infoDict[username], which is a dictionary, will have one more key-value pair: 'following': [a following list].)
    '''
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
    '''
    Input: a list of usernames. This is the output of getTwitterUsername(url, name) function.
    Output: A dictionary of all data to be inserted into the data structure. The keys are Twitter usernames. The values are dictionaries of all user information.
    The function uses Twitter API to retrieve data of users. If data has already been looked up before, data will be read from cache.
    If the data does not have the key: "following", getFollowing function will be called and cache will be updated.
    '''
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
