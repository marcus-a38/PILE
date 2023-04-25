# W.I.P

class Node():

    def __init__(self, data: list, parent=None, index=None):

        self.parent = parent
        self.data = data
        self.children = []
        self.index = index

    def add_child(self, child):

        self.children.append(child)

    
    def examine_data(self):

        self.raw = self.data[0]
        self.type = self.data[1]
        self.location = self.data[2]

        return {'raw': self.raw, 'type': self.type, 'loc': self.location}


class AST():

    def __init__(self):

        self.root = None
        self.size = 0
        self.index = 0


    def add_node(self, data: list, parent: Node=None):
        
        node_ = Node(data, index = self.size)

        if parent is None and self.root is None:
            self.root = node_

        elif parent is None and self.root is not None:
            raise Exception("non-root node must have a parent")

        else:
            parent.add_child(node_)

        self.size += 1
        return node_
    

    def render_tree(self, export=False):

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

    
    def searchone(self, data: list = None, index: int =None):

        if data is None and index is not None:
            if not isinstance(index, int): print("index must be type 'int'.")
        elif index is None and data is not None:
            if not isinstance(data, list): print("data must be type 'list'.")
        else:
            print("You must provide either an index or some data.")

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
    

    def searchall(self):

        pass


    def replace_node(self, *args, location: int = None):

        if location is not None and isinstance(location, int):
            res = self.searchone(index=location)
            if res is not None:
                res.data = list(args)

        else:
            print("Invalid value for parameter 'index'. Try an integer.")
