# -*- coding: utf-8 -*-
# data structure: binary search tree


from base.tree import Tree, TreeTest


class BinarySearchTree(Tree):
    def preorder(self):
        def recur(bst):
            if not bst:
                return []
            return [bst] + recur(bst.left) + recur(bst.right)

        return recur(self.root)

    def inorder(self):
        def recur(bst):
            if not bst:
                return []
            return recur(bst.left) + [bst] + recur(bst.right)

        return recur(self.root)

    def postorder(self):
        def recur(bst):
            if not bst:
                return []
            return recur(bst.left) + recur(bst.right) + [bst]

        return recur(self.root)
