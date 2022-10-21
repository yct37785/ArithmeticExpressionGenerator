import random
import time
universal_str = ''
operators = ['+', '-', '*']


class Node:
    def __init__(self, value):
        self.left = None
        self.right = None
        self.value = value


def gen_subtree(depth, max_depth):
    if depth == max_depth:
        return None
    is_operator = random.randint(0, 1) and depth < max_depth - 1
    if is_operator:
        parent = Node(operators[random.randint(0, len(operators)) - 1])
        parent.left = gen_subtree(depth + 1, max_depth)
        parent.right = gen_subtree(depth + 1, max_depth)
    else:
        parent = Node(random.randint(1, 9))
    return parent


def apply_value(sum, number, operator):
    if operator == '+':
        sum += number
    elif operator == '-':
        sum -= number
    elif operator == '*':
        sum *= number
    elif operator == '/':
        sum /= number
    return sum


def tree_to_str(root):
    # in order traversal
    global universal_str
    if not root.left:
        universal_str += str(root.value)
        return root.value
    # left
    universal_str += '('
    total_sum = tree_to_str(root.left)
    # operator
    universal_str += root.value
    # right
    v = tree_to_str(root.right)
    total_sum = apply_value(total_sum, v, root.value)
    universal_str += ')'
    return total_sum


if __name__ == '__main__':
    random.seed(time.time())
    root = Node(operators[random.randint(0, len(operators)) - 1])
    max_depth = random.randint(2, 4)
    # recursive to gen children for parent (root in this case)
    root.left = gen_subtree(0, max_depth)
    root.right = gen_subtree(0, max_depth)
    # form a string
    sum_value = tree_to_str(root)
    print('Str:', universal_str)
    print('Sum:', sum_value)