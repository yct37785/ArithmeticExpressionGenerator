import random
import time
universal_str = []
operators = ['+', '-']


class Node:
    def __init__(self, value):
        self.left = None
        self.right = None
        self.value = value


def gen_subtree(depth, max_depth):
    if depth == max_depth - 1:
        return Node(random.randint(1, 9)), Node(random.randint(1, 9))
    # either 1 or both are operators
    children = []
    at_least_1_operator = False
    for i in range(2):
        is_operator = random.randint(0, 1) or (i == 1 and not at_least_1_operator)
        if is_operator:
            at_least_1_operator = True
            children.append(Node(operators[random.randint(0, len(operators)) - 1]))
            children[-1].left, children[-1].right = gen_subtree(depth + 1, max_depth)
        else:
            children.append(Node(random.randint(1, 9)))
    return children[0], children[1]


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


def flatten_subtree(bp1, bp2, swap_op):
    global universal_str
    if bp1 != -1 and bp2 != -2:
        universal_str[bp1] = ' '
        universal_str[bp2] = ' '
    if swap_op:
        for i in range(bp1 + 1, bp2):
            if universal_str[i] == '-':
                universal_str[i] = '+'
            elif universal_str[i] == '+':
                universal_str[i] = '-'


# returns: sum, can_flatten, left_brace_pos, right_brace_pos
def tree_to_str(root):
    # in order traversal
    global universal_str
    if not root.left:
        universal_str.append(str(root.value))
        return root.value, True, -1, -1
    # left
    left_brace_pos = len(universal_str)
    universal_str.append('(')
    total_sum, left_can_flatten, lbp1, lbp2 = tree_to_str(root.left)
    # operator
    universal_str.append(root.value)
    # right
    v, right_can_flatten, rbp1, rbp2 = tree_to_str(root.right)
    total_sum = apply_value(total_sum, v, root.value)
    right_brace_pos = len(universal_str)
    universal_str.append(')')
    # flatten if is not divisor
    can_flatten = root.value == '+' or root.value == '-'
    # remove braces and flip all addition and subtraction operators if root is -
    if can_flatten:
        flatten_subtree(lbp1, lbp2, False)
        flatten_subtree(rbp1, rbp2, root.value == '-')
    return total_sum, can_flatten, left_brace_pos, right_brace_pos


if __name__ == '__main__':
    random.seed(time.time())
    # random.seed(10)
    root = Node(operators[random.randint(0, len(operators)) - 1])
    max_depth = random.randint(7, 7)
    # recursive to gen children for parent (root in this case)
    root.left, root.right = gen_subtree(0, max_depth)
    # form a string
    sum_value, a, b, c = tree_to_str(root)
    print('Str:', ''.join(universal_str).replace(' ', ''))
    print('Sum:', sum_value)