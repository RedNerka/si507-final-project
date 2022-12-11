class Node:
    def __init__(self,key,value,parent=None,left=None,right=None,dim=0):
        self.key=key
        self.value=value
        self.parent=parent
        self.left=left
        self.right=right
        self.dim=dim

    def info(self):
        print(f'key is {self.key}')
        print(f'value is {self.value}')
        if self.parent:
            print(f'parent is {self.parent.key}')
        else:
            print('no parent')
        if self.left:
            print(f'left child is {self.left.key}')
        else:
            print('no left')
        if self.right:
            print(f'right child is {self.right.key}')
        else:
            print('no right')
        print(f'dimension is {self.dim}')

class kdTree:
    def __init__(self,keySize):
        self.root=None
        self.size=0
        self.keySize=keySize

    def search(self,key):
        return self.searchHelper(key,self.root,self.root.dim)
    
    def searchHelper(self,key,node,Dim):
        if node==None:
            return None
        if node.key==key:
            return node
        if node.key[Dim]<key[Dim]:
            return self.searchHelper(key,node.right,(Dim+1)%self.keySize)
        else:
            return self.searchHelper(key,node.left,(Dim+1)%self.keySize)
    
    def insert(self,node):
        if self.root:
            self.insertHelper(node,self.root,self.root.dim)
        else:
            self.root=Node(node.key,node.value)
        self.size+=1

    def insertHelper(self,node,currNode,Dim):
        if node.key==currNode.key:
            currNode.value=node.value
        if node.key[Dim]<currNode.key[Dim]:
            if currNode.left is not None:
                self.insertHelper(node,currNode.left,(Dim+1)%self.keySize)
            else:
                currNode.left=Node(node.key,node.value,parent=currNode,dim=(Dim+1)%self.keySize)
        else:
            if currNode.right is not None:
                self.insertHelper(node,currNode.right,(Dim+1)%self.keySize)
            else:
                currNode.right=Node(node.key,node.value,parent=currNode,dim=(Dim+1)%self.keySize)

    def overlap(self,searchRange,treeRange):
        for i in range(self.keySize):
            if not (treeRange[i][0]>=searchRange[i][0] and treeRange[i][1]<=searchRange[i][1]):
                if treeRange[i][0]>searchRange[i][1] or treeRange[i][1]<searchRange[i][0]:
                    return 'none'
                else:
                    return 'overlap'
        return 'subset'

    def getAllNodes(self,currNode,nodeSet):
        if currNode is not None:
            self.getAllNodes(currNode.left,nodeSet)
            nodeSet.add(currNode)
            self.getAllNodes(currNode.right,nodeSet)

    def rangeSearch(self,searchRange):
        treeRange=[]
        for i in range(self.keySize):
                treeRange.append([' ','~'])
        return self.rangeSearchHelper(searchRange,treeRange,self.root,set(),self.root.dim)
    
    def rangeSearchHelper(self,searchRange,treeRange,currNode,res,Dim):
        if currNode is None:
            return set()
        # print(currNode.key)
        if self.overlap(searchRange,treeRange)=='none':
            # print('none')
            return set()
        if self.overlap(searchRange,treeRange)=='subset':
            # print('subset')
            self.getAllNodes(currNode,res)
            return res
        # print('overlap')
        flag=1
        for i in range(self.keySize):
            if currNode.key[i][0].lower()<searchRange[i][0] or currNode.key[i][0].lower()>searchRange[i][1]:
                flag=0
                # print(treeRange)
                # print(searchRange)
                # print('curr not add')
                break
        if flag==1: res.add(currNode)
        treeRange_left=[]
        treeRange_right=[]
        for li in treeRange:
            temp1=li.copy()
            temp2=li.copy()
            treeRange_left.append(temp1)
            treeRange_right.append(temp2)
        treeRange_left[Dim][1]=currNode.key[Dim].lower()
        treeRange_right[Dim][0]=currNode.key[Dim].lower()
        # print(treeRange_left)
        # print(treeRange_right)
        res=res.union(self.rangeSearchHelper(searchRange,treeRange_left,currNode.left,res,(Dim+1)%self.keySize))
        res=res.union(self.rangeSearchHelper(searchRange,treeRange_right,currNode.right,res,(Dim+1)%self.keySize))
        return res

    # def printTree(self):
    #     self.printTreeHelper(self.root)
    
    # def printTreeHelper(self,node):
    #     if node is not None:
    #         if node.left is not None:
    #             self.printTreeHelper(node.left)
    #         print(node.key)
    #         if node.right is not None:
    #             self.printTreeHelper(node.right)
