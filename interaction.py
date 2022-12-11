import getTwitterInfo
from kdtree import kdTree
from kdtree import Node

def main():
    print("Hi! Welcome to Shiyu Wu's SI507 final project!")
    index={'Band of Brothers':0,'Saving Private Ryan':1,'BraveHeart':2,'Mad Max: Fury Road':3,'Good Will Hunting':4}
    treeList=[[kdTree(keySize=2),kdTree(keySize=2)],[kdTree(keySize=2),kdTree(keySize=2)],[kdTree(keySize=2),kdTree(keySize=2)],[kdTree(keySize=2),kdTree(keySize=2)],[kdTree(keySize=2),kdTree(keySize=2)]]
    print("Importing data...")
    data=[None,None,None,None,None]
    data[0]=getTwitterInfo.getTwitterInfo(getTwitterInfo.getTwitterUsername('https://en.wikipedia.org/wiki/Band_of_Brothers_(miniseries)','band of brothers'))
    data[1]=getTwitterInfo.getTwitterInfo(getTwitterInfo.getTwitterUsername('https://en.wikipedia.org/wiki/Saving_Private_Ryan','saving private ryan'))
    data[2]=getTwitterInfo.getTwitterInfo(getTwitterInfo.getTwitterUsername('https://en.wikipedia.org/wiki/Braveheart','braveheart'))
    data[3]=getTwitterInfo.getTwitterInfo(getTwitterInfo.getTwitterUsername('https://en.wikipedia.org/wiki/Mad_Max:_Fury_Road','mad max'))
    data[4]=getTwitterInfo.getTwitterInfo(getTwitterInfo.getTwitterUsername('https://en.wikipedia.org/wiki/Good_Will_Hunting','good will hunting'))
    print("Done!")
    print("Generating data structures...")
    usrnameMap={}
    idMap={}
    for i in range(5):
        for usrname in data[i]:
            dic=data[i][usrname]
            key=['','']
            value={}
            for j in dic:
                if j=='id':
                    key[0]=dic[j]
                elif j=='username':
                    key[1]=dic[j]
                else:
                    value[j]=dic[j]
            treeNode=Node(key,value)
            idMap[key[0]]=key
            usrnameMap[key[1]]=key
            try:
                value['following']
                treeList[i][0].insert(treeNode)
            except:
                treeList[i][1].insert(treeNode)
    print("Done!")
    while True:
        print('The database includes some contributors of 5 TV works:')
        for i in index:
            print(str(index[i])+' '+i)
        userInput=input("Please enter the index(s) of the TV work(s) that you want to look up. Separate them with space. ").strip()
        if userInput.lower()=='quit':
            print('Bye!')
            exit(0)
        try:
            inputList=list(map(int,userInput.split()))
        except:
            print("Invalid input!")
            continue
        flag=1
        for i in inputList:
            if i<0 or i>4:
                print('Index out of range!')
                flag=0
                break
        if flag==0: continue
        while True:
            print('Search by ID, Search by username, Insert, Range search, Get following, Find common following, Return, Quit.')
            userInput=input("Enter a function listed above. ").strip().lower()
            if userInput=='quit':
                print('Bye!')
                exit(0)
            elif userInput=='search by id':
                searchID=input('Please enter the twitter ID you want to search. ').strip()
                print('Searching...')
                res=None
                try:
                    KEY=idMap[searchID]
                except:
                    print("ID doesn't exist in database!")
                    continue
                for i in inputList:
                    temp0=treeList[i][0].search(KEY)
                    temp1=treeList[i][1].search(KEY)
                    if temp0 is not None:
                        res=temp0
                        break
                    if temp1 is not None:
                        res=temp1
                        break
                if res is None:
                    print('Twitter user not found!')
                else:
                    res.info()
            elif userInput=='search by username':
                searchUsername=input('Please enter the twitter username you want to search. ').strip()
                print('Searching...')
                res=None
                try:
                    KEY=usrnameMap[searchUsername]
                except:
                    print("Username doesn't exist in database!")
                    continue
                for i in inputList:
                    temp0=treeList[i][0].search(KEY)
                    temp1=treeList[i][1].search(KEY)
                    if temp0 is not None:
                        res=temp0
                        break
                    if temp1 is not None:
                        res=temp1
                        break
                if res is None:
                    print('Twitter user not found!')
                else:
                    print(res.key)
                    print(res.value)
            elif userInput=='insert':
                if len(inputList)>1:
                    print('Number of selected tree > 1, cannot insert!')
                else:
                    insertkey=['','']
                    insertvalue={}
                    temp1=input('Please enter Twitter user ID. ')
                    try:
                        int(temp1)
                        insertkey[0]=temp1
                    except ValueError:
                        print('Invalid ID number!')
                        continue
                    insertkey[1]=input('Please enter Twitter username. ')
                    anInput=''
                    while anInput.lower()!='no':
                        valueVal=input('Please enter the value. ')
                        valueKey=input('Please enter the key for the entered value. ')
                        insertvalue[valueKey]=valueVal
                        anInput=input('Add more? ')
                    treeList[inputList[0]][1].insert(Node(insertkey,insertvalue))
                    treeList[inputList[0]][1].search(insertkey).info()
            elif userInput=='range search':
                Range=[[' ','~'],[' ','~']]
                lowerID=input('Please enter the starting first digit of Twitter user ID. Press enter to start from 0. ')
                if len(lowerID.strip())==1: Range[0][0]=lowerID
                elif len(lowerID.strip())>1: print('Invalid input')
                upperID=input('Please enter the ending first digit of Twitter user ID. Press enter to end with 9. ')
                if len(upperID.strip())==1: Range[0][1]=upperID
                elif len(upperID.strip())>1: print('Invalid input')
                lowerUsr=input('Please enter the starting first character of Twitter username. Press enter to start from a. ')
                if len(lowerUsr.strip())==1: Range[1][0]=lowerUsr
                elif len(lowerUsr.strip())>1: print('Invalid input')
                upperUsr=input('Please enter the ending first character of Twitter username. Press enter to end with z. ')
                if len(upperUsr.strip())==1: Range[1][1]=upperUsr
                elif len(upperUsr.strip())>1: print('Invalid input')
                li=[]
                for i in inputList:
                    li+=list(treeList[i][0].rangeSearch(Range))
                    li+=list(treeList[i][1].rangeSearch(Range))
                res=[]
                [res.append(x) for x in li if x not in res]
                num=input('Please enter the number of results to show. Press enter to show all. ')
                if num=='':
                    for node in res:
                        print(node.key)
                        print(node.value)
                elif num.strip().isdigit():
                    if int(num.strip())<=len(res):
                        for i in range(int(num.strip())):
                            print(res[i].key)
                            print(res[i].value)
                    else:
                        for node in res:
                            print(node.key)
                            print(node.value)
                else:
                    print('Invalid input!')
            elif userInput=='get following':
                searchUsername=input('Please enter the twitter username you want to search. ').strip()
                print('Searching...')
                res=None
                try:
                    KEY=usrnameMap[searchUsername]
                except:
                    print("Username doesn't exist in database!")
                    continue
                for i in inputList:
                    temp=treeList[i][0].search(KEY)
                    if temp is not None:
                        res=temp
                        break
                if res is None:
                    print('Twitter user not found!')
                else:
                    print(res.value['following'])
            elif userInput=='find common following':
                searchUsername1=input('Please enter the first twitter username you want to search. ').strip()
                searchUsername2=input('Please enter the second twitter username you want to search. ').strip()
                res1=None
                res2=None
                res=[]
                try:
                    KEY1=usrnameMap[searchUsername1]
                    KEY2=usrnameMap[searchUsername2]
                except:
                    print("Username doesn't exist in database!")
                    continue
                for i in inputList:
                    temp1=treeList[i][0].search(KEY1)
                    if temp1 is not None:
                        res1=temp1
                        break
                for i in inputList:
                    temp2=treeList[i][0].search(KEY2)
                    if temp2 is not None:
                        res2=temp2
                        break
                if res1 is None or res2 is None:
                    print('Twitter user not found!')
                else:
                    for i in res1.value['following']:
                        if i in res2.value['following']:
                            res.append(i)
                    if len(res)>0:
                        print(res)
                    else:
                        print('No common following users! ')
            elif userInput=='return':
                break
            else:
                print('Invalid command!')

if __name__=="__main__":
    main()
