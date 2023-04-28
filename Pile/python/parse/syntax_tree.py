# WORK IN PROGRESS ! FUNCTIONAL BUT EXPERIMENTAL

class Node():

    def __init__(self, data: list, parent=None, index=None):

        self.parent = parent
        self.data = data
        self.index = index
        self.children = []


    def addchild(self, child):

        self.children.append(child)

    
    def findchild(self, data: str = None, index: int = None) -> type["Node"]:

        if data is None and index is None:
            print("You must provide an argument.")
            return

        elif data is not None and isinstance(data, str):

            for child in self.children:
                if child.data == data:
                    print(f"Child located with data: {data}.")
                    return child
                
            print("Child could not be located.")
            return
        
        elif index is not None and isinstance(index, int):
            try:
                child = self.children[index]
                print(f"Child {index} of parent node {self.index} located.")
                return child
            except:
                print(f"No node exists for index {index}.")
            return
        
        print ("Invalid types for arguments.")
        return


    def examine(self):

        self.raw = self.data[0]
        self.type = self.data[1]
        self.location = self.data[2]

        return {'raw': self.raw, 'type': self.type, 'loc': self.location}
    

    def __str__(self):

        if self.parent is not None:
            return f"{self.index}, parent -> {self.parent.index}"
        else:
            return f"{self.index}, no parent."


class AST():

    def __init__(self):

        self.root = None
        self.size = 0


    def addnode(self, data: list, parent: Node=None):
        
        node_ = Node(data, parent = parent, index = self.size)

        if parent is None and self.root is None:
            self.root = node_

        elif parent is None and self.root is not None:
            raise Exception("non-root node must have a parent")

        else:
            parent.addchild(node_)

        self.size += 1
        return node_
    

    def render(self, export=False): # needs to be replaced by a visualization tool for larger I/O cases

        if self.root is None:
            print("Tree is empty.")
            return

        print("---------\nYour AST:\n---------")

        def traverse(node, level=0):
            print("| " * level + "+-" + str(node.data))
            for child in node.children:
                traverse(child, level=level+1)

        traverse(self.root)

        if export:
            pass

    
    def searchone(self, data: list = None, index: int = None): # best case: O(1), average case: O(n), worst case: O(n^2)

        if data is None and index is None:
            raise Exception("You must provide either some data or some index to search for a node.")

        if self.root.data == data:
            print(f"Data: {data} located in root node.")
            return self.root

        def traverse(node):
            if node.index == index:
                print(f"A node was found at index {index}.")
                return node
    
            for child in node.children:

                if child.data == data:
                    print(f"Data: {data} located in node {child.index}.")
                    return child
                res = traverse(child)

                if res is not None:
                    return res
                
            return None

        res = traverse(self.root)

        if res is not None:
            return res

        print("Could not find a node for given arguments.")
        return
    

    def searchall(self): # find all instances matching search arguments (rather than the first instance) TO ADD (possibly): searchseq to find a certain sequence of nodes.

        pass


    def replace_node(self, *args, location: int):

        if isinstance(location, int):
            res = self.searchone(index=location)
            if res is not None:
                res.data = list(args)

        else:
            print("Invalid value for parameter 'index'. Try an integer.")


    def tree_pop(self, location: int):

        if isinstance(location, int):
            traverse(self.root)
        else:
            raise Exception("Argument 'location' must be a valid integer value.")


        def traverse(node):

            if node.index == location:

                node.parent.pop(node)
                del node

            for child in node.children:
                traverse(child)


    def postorder(self): # best case: O(1), worst/average case: O(n) RETURNS A GENERATOR OBJECT.

        current_node = self.searchone(index=(self.size - 1))

        while current_node.parent is not None:

            for child in current_node.parent.children:
                yield child
            
            yield current_node.parent
            current_node = current_node.parent
    

    def isbalanced(self): # may need some tweaking to reduce complexity ... checks an evenly distributed AST to see if the left and right sides are balanced

        if self.root is None:
            print("Tree must at least have a root node.")

        elif self.root.children is None:
            return True

        elif len(self.root.children) % 2 != 0:
            print("Tree must have even number of root children.")
            return      
        
    
        def get_height(node, height=0):

            if not node.children:
                return 1
            
            for child in node.children:
                height += 1
                get_height(child, height)

            return 1 + sum([get_height(child, height) for child in node.children])
        
        left = self.root.children[:len(self.root.children) // 2]
        right = self.root.children[len(self.root.children) // 2:]

        left_height = sum([get_height(child) for child in left]) 
        right_height = sum([get_height(child) for child in right]

        if abs(left_height - right_height) >= 1:
            return False
            
        return True
