import random
operators = ['+', '-', '*']


class Node:
    def __init__(self, value):
        self.left = None
        self.right = None
        self.value = value


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


class StrGenerator:
    def __init__(self, seed, max_depth):
        random.seed(seed)
        self.max_depth = max_depth
        self.root = Node(operators[random.randint(0, len(operators)) - 1])
        self.universal_str = []

    def gen_subtree(self, depth, max_depth):
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
                children[-1].left, children[-1].right = self.gen_subtree(depth + 1, max_depth)
            else:
                children.append(Node(random.randint(1, 9)))
        return children[0], children[1]

    def flatten_subtree(self, bp1, bp2, swap_op):
        if bp1 != -1 and bp2 != -2:
            self.universal_str[bp1] = ' '
            self.universal_str[bp2] = ' '
        if swap_op:
            for i in range(bp1 + 1, bp2):
                if self.universal_str[i] == '-':
                    self.universal_str[i] = '+'
                elif self.universal_str[i] == '+':
                    self.universal_str[i] = '-'

    # returns: sum, can_flatten, left_brace_pos, right_brace_pos
    def tree_to_str(self, root):
        # in order traversal
        if not root.left:
            self.universal_str.append(str(root.value))
            return root.value, True, -1, -1
        # left
        left_brace_pos = len(self.universal_str)
        self.universal_str.append('(')
        total_sum, left_can_flatten, lbp1, lbp2 = self.tree_to_str(root.left)
        # operator
        self.universal_str.append(root.value)
        # right
        v, right_can_flatten, rbp1, rbp2 = self.tree_to_str(root.right)
        total_sum = apply_value(total_sum, v, root.value)
        right_brace_pos = len(self.universal_str)
        self.universal_str.append(')')
        # flatten if is not divisor
        can_flatten = root.value == '+' or root.value == '-'
        # remove braces and flip all addition and subtraction operators if root is -
        if can_flatten:
            if left_can_flatten:
                self.flatten_subtree(lbp1, lbp2, False)
            if right_can_flatten:
                self.flatten_subtree(rbp1, rbp2, root.value == '-')
        return total_sum, can_flatten and left_can_flatten and right_can_flatten, left_brace_pos, right_brace_pos

    def run(self, print_values):
        self.root.left, self.root.right = self.gen_subtree(0, self.max_depth)
        # form a string
        sum_value, a, b, c = self.tree_to_str(self.root)
        str_value = ''.join(self.universal_str).replace(' ', '')
        if print_values:
            print('Str:', str_value)
            print('Sum:', sum_value)
        return str_value, sum_value