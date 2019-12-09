#!/usr/bin/env python3


op_priority = {
    '+': 1,
    '-': 1,
    '*': 2,
    '/': 2,
    '%': 2,
    '^': 3,
}

op_handler = {
    '+': lambda x, y: x+y,
    '-': lambda x, y: x-y,
    '*': lambda x, y: x*y,
    '/': lambda x, y: x/y,
    '%': lambda x, y: x % y,
    '^': lambda x, y: x**y,
}


def is_operator(op):
    return op in op_priority


def is_parenthesis(op):
    return op == '(' or op == ')'


def tokenizer(expr):
    l = len(expr)
    i = 0
    tokens = []
    while i < l:
        while expr[i] == ' ':
            i += 1
        if is_operator(expr[i]):
            if i + 1 == l:
                return None
            if expr[i] == '-':
                if tokens and (not is_operator(tokens[-1]) and not tokens[-1] == '('):
                    tokens.append(expr[i])
                    i += 1
                else:
                    j = i + 1
                    while j < l and not is_operator(expr[j]) and not is_parenthesis(expr[j]):
                        j += 1
                    tokens.append(expr[i:j])
                    i = j
            else:
                tokens.append(expr[i])
                i += 1
        elif is_parenthesis(expr[i]):
            tokens.append(expr[i])
            i += 1
        else:
            j = i
            while j < l and not is_operator(expr[j]) and not is_parenthesis(expr[j]):
                j += 1
            tokens.append(expr[i:j])
            i = j

    return tokens


def to_polish(tokens):
    # 准备一个栈来存储运算符和 "("
    # 遍历中缀表达式
    #   1. 如果是操作数，直接输出
    #   2. 如果是 "("，直接入栈
    #   3. 如果是 ")"，从栈中弹出元素输出直到遇到 "("
    #   4. 如果是运算符并且栈为空，直接入栈
    #   5. 如果是运算符并且栈不为空，从栈里弹出元素输出，直到栈顶优先级低于当前运算符或者遇到 "("
    # 将栈里剩余的元素一次弹出输出
    polish = []
    stack = []
    for token in tokens:
        if is_operator(token):
            while stack and is_operator(stack[-1]) and op_priority[stack[-1]] >= op_priority[token]:
                polish.append(stack[-1])
                stack.pop()
            stack.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while stack and stack[-1] != '(':
                polish.append(stack[-1])
                stack.pop()
            if not stack:
                return None
            stack.pop()
        else:
            polish.append(token)
    while stack:
        polish.append(stack[-1])
        stack.pop()

    return polish


def calculate(polish):
    # 准备一个栈用来存储中间结果
    # 遍历逆波兰表达式
    #   1. 如果是操作数，直接入栈
    #   2. 如果是运算符，从栈顶取出运算符所需要的操作数个数，计算结果再次入栈
    # 最后栈中只剩下一个元素，即最终结果
    stack = []
    for token in polish:
        if is_operator(token):
            y = stack[-1]
            stack.pop()
            x = stack[-1]
            stack.pop()
            stack.append(op_handler[token](x, y))
        else:
            stack.append(int(token))
    return stack[-1]


class Node:
    def __init__(self, val, left=None, right=None):
        self.left = left
        self.right = right
        self.val = val

    def __str__(self):
        return str(self.left) + ", " + str(self.val) + ", " + str(self.right)


def to_binary_tree(polish):
    # 准备一个栈用来存储中间节点
    # 遍历逆波兰表达式
    #   1. 如果是操作数，构造一个操作数节点入栈
    #   2. 如果是运算符，构造一个新的节点，从栈顶取两个元素作为左右节点，新节点入栈
    # 最后栈中只剩下一个节点，即最终的 root 节点
    stack = []
    for token in polish:
        if is_operator(token):
            right = stack[-1]
            stack.pop()
            left = stack[-1]
            stack.pop()
            stack.append(Node(token, left, right))
        else:
            stack.append(Node(token))
    return stack[-1]


def calculate_binary_tree(node):
    if not is_operator(node.val):
        return int(node.val)
    return op_handler[node.val](calculate_binary_tree(node.left), calculate_binary_tree(node.right))


def main():
    # expr = "1+2*(3+4)"
    expr = "1 + 212 + (-2 + 33) * 2 + (32 * (46 - 45))"
    print(tokenizer(expr))
    print(to_polish(tokenizer(expr)))
    print(calculate(to_polish(tokenizer(expr))))
    print(to_binary_tree(to_polish(tokenizer(expr))))
    print(calculate_binary_tree(to_binary_tree(to_polish(tokenizer(expr)))))


if __name__ == '__main__':
    main()
