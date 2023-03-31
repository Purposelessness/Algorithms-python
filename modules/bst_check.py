import sys


class Node:
    data = -1
    left = None
    right = None


def is_bst_impl(node, n_min, n_max):
    if node.data < n_min or node.data > n_max:
        return False

    l_is_bst = True
    if node.left is not None:
        if node.left.data < node.data:
            l_is_bst = is_bst_impl(node.left, n_min, node.data)
        else:
            l_is_bst = False

    r_is_bst = True
    if node.right is not None:
        if node.right.data > node.data:
            r_is_bst = is_bst_impl(node.right, node.data, n_max)
        else:
            r_is_bst = False
    return l_is_bst and r_is_bst


def is_bst(root):
    if root is None:
        return True
    return is_bst_impl(root, -sys.maxsize - 1, sys.maxsize)
