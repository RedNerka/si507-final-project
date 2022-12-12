import getTwitterInfo
from kdtree import kdTree
from kdtree import Node

def main():
    print("Hi! Welcome to Shiyu Wu's SI507 final project!")
    index={'Band of Brothers':0,'Saving Private Ryan':1,'BraveHeart':2,'Mad Max: Fury Road':3,'Good Will Hunting':4} # Construct a mapping between every TV work and an index.
    treeList=[[kdTree(keySize=2),kdTree(keySize=2)],[kdTree(keySize=2),kdTree(keySize=2)],\
        [kdTree(keySize=2),kdTree(keySize=2)],[kdTree(keySize=2),kdTree(keySize=2)],[kdTree(keySize=2),kdTree(keySize=2)]] 
        # Construct all ten trees for the five TV works.
        # Every TV work has two trees. The first one stores all nodes that carry the information of TV work contributors. Every node has an extra attribute in its value: 'following'.
        # The second one stores all nodes that carry the information of the users who are followed by the TV work contributors.
        # The 'following' field in the first tree works as a foreigh key that links to the second tree.
        # Since the elements are lists, I cannot use [[kdTree(keySize=2)]*2]*5, otherwise the addresses of the elements will be the same.
    # ----------------------------------------------------------------------------------------------------------------------------
    # This part of codes is to import data from JSON cache file.
    print("Importing data...")
    data=[None,None,None,None,None]
    data[0]=getTwitterInfo.getTwitterInfo(getTwitterInfo.getTwitterUsername('https://en.wikipedia.org/wiki/Band_of_Brothers_(miniseries)','band of brothers'))
    data[1]=getTwitterInfo.getTwitterInfo(getTwitterInfo.getTwitterUsername('https://en.wikipedia.org/wiki/Saving_Private_Ryan','saving private ryan'))
    data[2]=getTwitterInfo.getTwitterInfo(getTwitterInfo.getTwitterUsername('https://en.wikipedia.org/wiki/Braveheart','braveheart'))
    data[3]=getTwitterInfo.getTwitterInfo(getTwitterInfo.getTwitterUsername('https://en.wikipedia.org/wiki/Mad_Max:_Fury_Road','mad max'))
    data[4]=getTwitterInfo.getTwitterInfo(getTwitterInfo.getTwitterUsername('https://en.wikipedia.org/wiki/Good_Will_Hunting','good will hunting'))
    print("Done!")
    # ----------------------------------------------------------------------------------------------------------------------------
    # This part of codes is to organize the data into the data structure.
    print("Generating data structures...")
    # These two dictionaries are used in Search by ID and Search by Username functions.
    # Since users will only provide one of the keys, a mapping from one key (ID or username) to the complete key list (ID and username) is necessary
    # because search function needs to take in a complete key to perform a successful search.
    usrnameMap={}
    idMap={}
    for i in range(5):
        for usrname in data[i]:
            dic=data[i][usrname]
            key=['','']
            value={}
            # Iterate through all data and put id and username into key, while all other data into value dict.
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
            # If the current node has 'following' field, add it to the contributor tree (first tree).
            # If the current node has no such field, add it to the following tree (second tree).
            try:
                value['following']
                treeList[i][0].insert(treeNode)
            except:
                treeList[i][1].insert(treeNode)
    print("Done!")
    # ----------------------------------------------------------------------------------------------------------------------------
    # This part of codes is responsible for the whole process of interacting with the user inputs.
    while True:
        # ----------------------------------------------------------------------------------------------------------------------------
        # This part of codes asks users to enter the index(s) of TV work(s) they want to look up.
        print('The database includes some contributors of 5 TV works:')
        for i in index:
            print(str(index[i])+' '+i)
        userInput=' '.join(input("Please enter the index(s) of the TV work(s) that you want to look up and separate them with space. Otherwise enter quit to end the service. ").split())
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
        # ----------------------------------------------------------------------------------------------------------------------------
        # This part of codes introduce the functions to the users. The users need to enter the function they want to perform.
        # The functions are: Search by ID, Search by username, Insert, Range search, Get following, Find common following, Print Tree, Return, Quit.
        # User inputs are not case-sensitive, and white spaces will not influence the if statements.
        while True:
            print('Search by ID, Search by username, Insert, Range search, Get following, Find common following, Print Tree, Return, Quit.')
            userInput=' '.join(input("Enter a function listed above. ").split()).lower()   
            # ----------------------------------------------------------------------------------------------------------------------------
            # Go in this if statement if user enters quit.
            if userInput=='quit':
                print('Bye!')
                exit(0)
            # ----------------------------------------------------------------------------------------------------------------------------
            # Go in this if statement if user enters search by id.
            elif userInput=='search by id':
                searchID=' '.join(input('Please enter the twitter ID you want to search. ').split())
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
            # ----------------------------------------------------------------------------------------------------------------------------
            # Go in this if statement if user enters search by username.
            elif userInput=='search by username':
                searchUsername=' '.join(input('Please enter the twitter username you want to search. ').split())
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
                    res.info()
            # ----------------------------------------------------------------------------------------------------------------------------
            # Go in this statement if user enters insert.
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
                    idMap[insertkey[0]]=insertkey
                    usrnameMap[insertkey[1]]=insertkey
            # ----------------------------------------------------------------------------------------------------------------------------
            # Go in this if statement if user enters range search.
            elif userInput=='range search':
                Range=[[' ','~'],[' ','~']]
                lowerID=input('Please enter the starting first digit of Twitter user ID. Press enter to start from 0. ')
                if len(' '.join(lowerID.split()))==1: Range[0][0]=lowerID
                elif len(' '.join(lowerID.split()))>1: print('Invalid input')
                upperID=input('Please enter the ending first digit of Twitter user ID. Press enter to end with 9. ')
                if len(' '.join(upperID.split()))==1: Range[0][1]=upperID
                elif len(' '.join(upperID.split()))>1: print('Invalid input')
                lowerUsr=input('Please enter the starting first character of Twitter username. Press enter to start from a. ')
                if len(' '.join(lowerUsr.split()))==1: Range[1][0]=lowerUsr
                elif len(' '.join(lowerUsr.split()))>1: print('Invalid input')
                upperUsr=input('Please enter the ending first character of Twitter username. Press enter to end with z. ')
                if len(' '.join(upperUsr.split()))==1: Range[1][1]=upperUsr
                elif len(' '.join(upperUsr.split()))>1: print('Invalid input')
                li=[]
                for i in inputList:
                    li+=list(treeList[i][0].rangeSearch(Range))
                    li+=list(treeList[i][1].rangeSearch(Range))
                res=[]
                [res.append(x) for x in li if x not in res]
                num=input('Please enter the number of results to show. Press enter to show all. ')
                if num=='':
                    for node in res:
                        node.info()
                elif ' '.join(num.split()).isdigit():
                    if int(' '.join(num.split()))<=len(res):
                        for i in range(int(' '.join(num.split()))):
                            res[i].info()
                    else:
                        for node in res:
                            node.info()
                else:
                    print('Invalid input!')
            # ----------------------------------------------------------------------------------------------------------------------------
            # Go in this if statement if user enters get following.
            elif userInput=='get following':
                searchUsername=' '.join(input('Please enter the twitter username you want to search. ').split())
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
                    for i in res.value['following']:
                        print(i)
            # ----------------------------------------------------------------------------------------------------------------------------
            # Go in this if statement if user enters find common following.
            elif userInput=='find common following':
                searchUsername1=' '.join(input('Please enter the first twitter username you want to search. ').split())
                searchUsername2=' '.join(input('Please enter the second twitter username you want to search. ').split())
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
                        for i in res:
                            print(i)
                    else:
                        print('No common following users! ')
            # ----------------------------------------------------------------------------------------------------------------------------
            # Go in this if statement if user enters return.
            elif userInput=='return':
                break
            # ----------------------------------------------------------------------------------------------------------------------------
            # Go in this if statement if user enters print tree.
            elif userInput=='print tree':
                nodeCount=0
                printChoice=input('Which tree to print? Contributor tree or following tree or Both? ')
                if ' '.join(printChoice.split()).lower()=='contributor tree':
                    for i in inputList:
                        print('Printing contributor tree...')
                        treeList[i][0].printTree()
                        nodeCount+=treeList[i][0].size
                    print(f'There are {nodeCount} nodes in total. ')
                elif ' '.join(printChoice.split()).lower()=='following tree':
                    for i in inputList:
                        print('Printing following tree...')
                        treeList[i][1].printTree()
                        nodeCount+=treeList[i][1].size
                    print(f'There are {nodeCount} nodes in total. ')
                elif ' '.join(printChoice.split()).lower()=='both':
                    for i in inputList:
                        print('Printing both trees...')
                        treeList[i][0].printTree()
                        nodeCount+=treeList[i][0].size
                        treeList[i][1].printTree()
                        nodeCount+=treeList[i][1].size
                    print(f'There are {nodeCount} nodes in total. ')
                else:
                    print('Invalid input! ')
            # ----------------------------------------------------------------------------------------------------------------------------
            # Otherwise the input is not a valid function call.
            else:
                print('Invalid command!')

if __name__=="__main__":
    main()
