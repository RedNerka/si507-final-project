class Node:
    '''
    A data structure to store the data in a tree node.
    '''
    def __init__(self,key,value,parent=None,left=None,right=None,dim=0):
        self.key=key # key of node, in my case, it is a list in the shape of [<user ID>,<username>]
        self.value=value # value of node, it is a dictionary with keys: created_at, location, name, profile_image_url, description. If it is a node in contributor tree, extra key: following.
        self.parent=parent # key of parent node of this node
        self.left=left # key of left node of this node
        self.right=right # key of right node of this node
        self.dim=dim # the dimension of this node.

    def info(self):
        '''
        Print all needed information of the node so as to know the information in this node as well as the location of the node in the tree.
        '''
        print(f'Key is {self.key}, dimension is {self.dim}. ',end='')
        if self.parent:
            print(f'Parent is {self.parent.key}. ',end='')
        else:
            print('No parent node. ',end='')
        if self.left:
            print(f'Left child is {self.left.key}. ',end='')
        else:
            print('No left node. ',end='')
        if self.right:
            print(f'Right child is {self.right.key}. ')
        else:
            print('No right node. ')
        print(f'Value is {self.value}. ')
        print('\n',end='')

class kdTree:
    '''
    A data structure to store all data nodes.
    '''
    def __init__(self,keySize):
        self.root=None # the root node of the tree
        self.size=0 # the number of nodes in the tree
        self.keySize=keySize # the dimension of the tree, in my case, keySize=2

    def search(self,key):
        return self.searchHelper(key,self.root,self.root.dim)
    
    def searchHelper(self,key,node,Dim):
        '''
        Input: Key to search. Key is a list with shape [<User ID>,<Username>]; the current node; the current dimension
        Output: a node if key is found, otherwise None.
        The function is the helper function of search. The function is a recursing function that will call itself when percolating down.
        '''
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
        '''
        Input: a node to insert; the current node; the current dimension
        Output: None
        The function is the helper function of insert. It will update the node value if the key is found.
        The function is a recursing function that will call itself when percolating down.
        '''
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
        '''
        Input: a range to search and the range of current node with shape [[<ID_min,ID_max>],[<username_min>,<username_max>]]
        Output: If the two ranges overlap, return 'overlap'. If the two ranges have no overlap, return 'none'. If one range covers the other, return 'subset'.
        The function judges the relationship between the search range and the current node range.
        '''
        for i in range(self.keySize):
            if not (treeRange[i][0]>=searchRange[i][0] and treeRange[i][1]<=searchRange[i][1]):
                if treeRange[i][0]>searchRange[i][1] or treeRange[i][1]<searchRange[i][0]:
                    return 'none'
                else:
                    return 'overlap'
        return 'subset'

    def getAllNodes(self,currNode,nodeSet):
        '''
        Input: the current node; a set of nodes.
        Output: None
        The function will add the current node and all the nodes in its left and right subtrees into the set of nodes. The order is in-order.
        '''
        if currNode is not None:
            self.getAllNodes(currNode.left,nodeSet)
            nodeSet.add(currNode)
            self.getAllNodes(currNode.right,nodeSet)

    def rangeSearch(self,searchRange):
        treeRange=[]
        for i in range(self.keySize):
                treeRange.append([' ','~']) # For the root node, the range is universe.
        return self.rangeSearchHelper(searchRange,treeRange,self.root,set(),self.root.dim)
    
    def rangeSearchHelper(self,searchRange,treeRange,currNode,res,Dim):
        '''
        Input: the search range; The range of current node; The current node; the result node set; the current dimension.
        Output: a set of nodes that are in the search range.
        The function judges the relationship between the search range and the range of current node.
        If 'none', return empty set.
        If 'subset', add all nodes under the current node into the result set.
        If current node is None, return empty set.
        If 'overlap', judge whether the current node is in the search range. Add it into the result set if it's in range.
        Calculate the range for the left child and the right child.
        Recurse itself when percolating down the left and right subtree.
        '''
        if currNode is None:
            return set()
        if self.overlap(searchRange,treeRange)=='none':
            return set()
        if self.overlap(searchRange,treeRange)=='subset':
            self.getAllNodes(currNode,res)
            return res
        flag=1
        for i in range(self.keySize):
            if currNode.key[i][0].lower()<searchRange[i][0] or currNode.key[i][0].lower()>searchRange[i][1]:
                flag=0
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
        res=res.union(self.rangeSearchHelper(searchRange,treeRange_left,currNode.left,res,(Dim+1)%self.keySize))
        res=res.union(self.rangeSearchHelper(searchRange,treeRange_right,currNode.right,res,(Dim+1)%self.keySize))
        return res

    def printTree(self):
        self.printTreeHelper(self.root)
    
    def printTreeHelper(self,node):
        '''
        Input: current node.
        Output: None
        The function is the helper function of printTree.
        The function will print the node information from the left-most node to the right-most node. Node.info() will be called.
        '''
        if node is not None:
            if node.left is not None:
                self.printTreeHelper(node.left)
            node.info()
            if node.right is not None:
                self.printTreeHelper(node.right)
