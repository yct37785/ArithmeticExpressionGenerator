import random
universal_str = ''
operators = ['+', '-']

class Node:
    def __init__(self, value):
        self.left_children = []
        self.right_children = []
        self.value = value


def gen_subtree(depth, max_depth, max_children):
    children = []
    if depth == max_depth:
        return children
    num_children = random.randint(2, max_children)
    # each parent will have 2-n children
    for i in range(num_children):
        # leaf nodes cannot be operators
        is_operator = random.randint(0, 1) and depth < max_depth - 1
        # if is operator
        if is_operator:
            children.append(Node(operators[random.randint(0, len(operators)) - 1]))
            children[-1].left_children = gen_subtree(depth + 1, max_depth, max_children)
            children[-1].right_children = gen_subtree(depth + 1, max_depth, max_children)
        # if is number, no children will be present
        else:
            number = random.randint(1, 9)
            children.append(Node(number))
    return children


def apply_value(sum, number, operator):
    if operator == '+':
        sum += number
    elif operator == '-':
        sum -= number
    return sum


def tree_to_str(root):
    global universal_str
    sum_value = 0
    if len(root.left_children) > 0:
        universal_str += '('
    # do an in-order traversal of left children
    for i in range(len(root.left_children)):
        v = tree_to_str(root.left_children[i])
        if i < len(root.left_children) - 1:
            universal_str += str(root.value)
    # if root.value == '+':
    #     universal_str += '|' + root.value + '|'
    # else:
    #     universal_str += str(root.value)
    universal_str += str(root.value)
    # do an in-order traversal of right children
    for i in range(len(root.right_children)):
        v = tree_to_str(root.right_children[i])
        if i < len(root.right_children) - 1:
            universal_str += str(root.value)
    if len(root.right_children) > 0:
        universal_str += ')'
    return sum_value

if __name__ == '__main__':
    root = Node('+')
    max_depth = random.randint(2, 2)
    max_children = random.randint(2, 2)
    # recursive to gen children for parent (root in this case)
    root.left_children = gen_subtree(0, max_depth, max_children)
    root.right_children = gen_subtree(0, max_depth, max_children)
    # form a string
    sum_value = tree_to_str(root)
    print('Str:', universal_str)
    print('Sum:', sum_value)
