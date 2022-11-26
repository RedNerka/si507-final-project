class Node:
    def __init__(self,key,value,parent=None,left=None,right=None,dim=0):
        self.key=key
        self.value=value
        self.parent=parent
        self.left=left
        self.right=right
        self.dim=dim

    def info(self):
        print(self.key)
        print(self.value)
        if self.parent:
            print(self.parent.key)
        else:
            print('no parent')
        if self.left:
            print(self.left.key)
        else:
            print('no left')
        if self.right:
            print(self.right.key)
        else:
            print('no right')
        print(self.dim)

class kdTree:
    def __init__(self,keySize):
        self.root=None
        self.size=0
        self.keySize=keySize

    def search(self,key):
        if self.root:
            return self.searchHelper(key,self.root,self.root.dim)
        else:
            return None
    
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
            usrInput=input('Duplicated key! Press y to overwrite. Press n to ignore.')
            if usrInput.lower()=='y':
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
    
a=kdTree(keySize=2)
a.insert(Node(['aa',2],'a'))
a.insert(Node(['ab',3],'b'))
a.insert(Node(['ac',4],'c'))
a.insert(Node(['AA',1],'d'))
a.search(['ab',3]).info()
print(a.size)