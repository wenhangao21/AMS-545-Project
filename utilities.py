import numpy as np


# this is an implementation of the median of medians algorithm. Code adapted from stackoverflow
def find_i_th_smallest(lst, i):
    # takes in an 1d numeric array, returns the ith element as in sorted(list). However, this is linear by median of medians algorithm.
    items_per_column = 15
    t = len(lst)
    if(t <= items_per_column):
        # if lst is a small list with less than items_per_column items, then just do sorting.
        return sorted(lst)[i]
    else:
        # 1. partition lst into columns of k items each. k is odd, say 5.
        # 2. find the median of every column
        # 3. put all medians in a new list, say, B
        B = [find_i_th_smallest(k, int((len(k) - 1)/2)) for k in [lst[j:(j + items_per_column)] for j in range(0, len(lst), \
             items_per_column)]]
        # 4. find M, the median of B
        M = find_i_th_smallest(B, int((len(B) - 1)/2))
        # 5. split lst into 3 parts by M, { < M }, { == M }, and { > M }
        # 6. find which above set has lst's i-th smallest, recursively.
        P1 = [ j for j in lst if j < M ]
        if i < len(P1):
            return find_i_th_smallest( P1, i)
        P3 = [ j for j in lst if j > M ]
        L3 = len(P3)
        if i < (t - L3):
            return M
        return find_i_th_smallest(P3, i - (t - L3))


def split_value(cd, points):
    # returns the value to do the splitting in the kd tree
    pts = points[:, cd]  # cd: current dimension
    split_val = find_i_th_smallest(pts, int(np.ceil(len(pts)/2))-1)
    return split_val


def split_list(cd, points, split_val):
    # split a list based on the dimension and split val
    select_mask = points[:, cd] <= split_val
    return points[select_mask, :], points[np.invert(select_mask), :]


class Node:
    def __init__(self):
        self.val = None
        self.left = None
        self.right = None


def buildKdTree(node, points, depth=0, k=2):
    if len(points) <= 0:
        return
    if len(points) == 1:
        node.val = points[0]
        return node
    else:
        cd = depth % k
        split_val = split_value(cd, points)
        node.val = split_val
        left_list, right_list = split_list(cd, points, split_val)
        node.left = Node()
        node.right = Node()
        node.left = buildKdTree(node.left, left_list, depth+1, k)
        node.right = buildKdTree(node.right, right_list, depth+1, k)
        return node


# prints a tree, code adapted from stackoverflow
def print_tree(root, point="val", left="left", right="right"):
    def display(root, point=point, left=left, right=right):
        """Returns list of strings, width, height, and horizontal coordinate of the root."""
        # No child.
        if getattr(root, right) is None and getattr(root, left) is None:
            line = '%s' % trunc(getattr(root, point), 2)
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        # Only left child.
        if getattr(root, right) is None:
            lines, n, p, x = display(getattr(root, left))
            s = '%s' % trunc(getattr(root, point), 2)
            u = len(s)
            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
            second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
            shifted_lines = [line + u * ' ' for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        # Only right child.
        if getattr(root, left) is None:
            lines, n, p, x = display(getattr(root, right))
            s = '%s' % trunc(getattr(root, point), 2)
            u = len(s)
            first_line = s + x * '_' + (n - x) * ' '
            second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
            shifted_lines = [u * ' ' + line for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

        # Two children.
        left, n, p, x = display(getattr(root, left))
        right, m, q, y = display(getattr(root, right))
        s = '%s' % trunc(getattr(root, point), 2)
        u = len(s)
        first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s + y * '_' + (m - y) * ' '
        second_line = x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '
        if p < q:
            left += [n * ' '] * (q - p)
        elif q < p:
            right += [m * ' '] * (p - q)
        zipped_lines = zip(left, right)
        lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
        return lines, n + m + u, max(p, q) + 2, n + u // 2

    lines, *_ = display(root, point, left, right)
    for line in lines:
        print(line)


def trunc(values, decs=0):
    # truncates floating numbers, for the purpose of visualizing the kd tree
    return np.trunc(values*10**decs)/(10**decs)


def intersect(node_val, rec0, rec1):
    # if the left/right region of the current node intersects the query box
    left, right = False, False
    if node_val >= rec0:
        left = True
    if node_val <= rec1:
        right = True
    return left, right


def query_rec(node, rectangle, output, depth=0, k=2):
    # recursion to do the query
    if node.val is None:
        return
    if not (node.left or node.right):
        # if leaf node and point in the box, add to output
        x, y = node.val[0], node.val[1]
        x0, y0, x1, y1 = rectangle[0], rectangle[1], rectangle[2], rectangle[3]
        if k == 2:
            if x0 <= x <= x1 and y0 <= y <= y1:
                output.append(node.val)
        if k == 4:
            z, w = node.val[2], node.val[3]
            if x0 <= x <= x1 and y0 <= y <= y1 and x0 <= z <= x1 and y0 <= w <= y1:
                output.append(node.val)
        return
    cd = depth % k
    if cd == 0:
        rec0, rec1 = rectangle[0], rectangle[2]
    else:
        rec0, rec1 = rectangle[1], rectangle[3]
    left, right = intersect(node.val, rec0, rec1)  # left, right are flags, True of False
    # if the left/right region of current node intersects the box, descent.
    if left:
        query_rec(node.left, rectangle, output, depth+1, k)
    if right:
        query_rec(node.right, rectangle, output, depth + 1, k)


def query(node, rectangle, k=2):
    if node is None:
        return
    output = []
    query_rec(node, rectangle, output, k=k)
    return np.array(output)

