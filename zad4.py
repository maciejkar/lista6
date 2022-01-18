
from zad1 import Binary_Tree
import re


class Stack:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[len(self.items)-1]

    def size(self):
        return len(self.items)

    def __str__(self):
        return str(self.items)


def not_first_precedence(first_op, second_op, precedence_op, functions):
    """Function check if second operator has to eval first
    @pam first_op:(str) first operator
    @pam second_op:(str) second operator
    @param precedence_op :(dict) dict with precedence of operators
    @pam functions: (dict) dict with functions
    return: (Bool) """
    if second_op == '(':
        return False
    if first_op in functions.values():
        proity_1 = 2.5
    else:
        proity_1 = precedence_op[first_op]
    if second_op in functions.values():
        proity_2 = 2.5
    else:
        proity_2 = precedence_op[second_op]

    return proity_1 <= proity_2


def infix_to_posix(infix, functions):
    """Function convert infix from of expression to posix
    @pam infix:(str) expression
    @param functions:(dict) dict of functions 
    return : (str) expression converted to posix"""
    operators = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
    output = ''
    stack = Stack()
    for ele in infix:

        if ele == '(':
            stack.push(ele)

        elif ele == ')':
            while stack.is_empty() == False and stack.peek() != '(':
                output += stack.pop()
            if stack.is_empty() == False and stack.peek() != '(':
                raise ValueError("Error in expression")
            else:
                stack.pop()
        elif ele not in functions.values() and ele not in operators:  # check if element is number or variable
            output += ele

        else:
            while stack.is_empty() == False and not_first_precedence(ele, stack.peek(), operators, functions):
                output += stack.pop()
            stack.push(ele)

    while stack.is_empty() == False:
        output += stack.pop()

    return output


def make_tree_from_posix(exp, functions):
    """Function convert expression in posix to expression tree
    @param exp:(str) expression in posix format
    return : (Binary_Tree)  tree with expression"""
    operators = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
    exp_list = [char for char in exp]
    tru_func = {y: x for x, y in functions.items()}

    stack = Stack()
    for element in exp_list:
        tree = Binary_Tree(element)
        if element in operators:
            temp_tree = stack.pop()
            temp_tree.set_parent(tree)
            tree.set_right_branch(temp_tree)
            temp_tree = stack.pop()
            temp_tree.set_parent(tree)
            tree.set_left_branch(temp_tree)
            stack.push(tree)
        elif element in tru_func:
            element = tru_func[element]
            tree.set_root(element)
            temp_tree = stack.pop()
            temp_tree.set_parent(tree)
            tree.set_right_branch(temp_tree)
            stack.push(tree)
        else:
            stack.push(tree)

    return stack.peek()


def tree_to_string(tree):
    """Function convert expression tree to string
    @pam tree: (Binary_Tree) tree with expression
    return: (str) expression"""
    operators = ['+', '-', '*', '/', '^']
    functions = ['sin', 'cos', 'tan', 'ln', 'sinh', 'cosh']
    exp_string = ""

    if tree and type(tree) != str:
        if tree.get_root() not in operators and tree.get_root() not in functions and tree.get_root() != None:
            exp_string = tree_to_string(tree.get_left_branch())
            exp_string += str(tree.get_root())
            exp_string += tree_to_string(tree.get_right_branch())
        elif tree.get_root() != None and tree.get_root() in functions:
            exp_string = '(' + tree_to_string(tree.get_left_branch())
            exp_string += str(tree.get_root())
            exp_string += tree_to_string(tree.get_right_branch()) + ')'
        elif tree.get_root() != None:
            exp_string = '(' + tree_to_string(tree.get_left_branch())
            exp_string += str(tree.get_root())
            exp_string += tree_to_string(tree.get_right_branch()) + ')'

        if tree.get_root() in functions:
            exp_string = str(tree.get_root())
            exp_string = '(' + exp_string
            exp_string += tree_to_string(tree.get_right_branch()) + ')'

    return exp_string


def make_derivative_tree(tree, variable='x'):
    """Function convert expression tree to derivative tree with respect variable
    @param tree:(Binary_Tree)  tree with expression
    @pam variable: (str)  variable which is respect in derivative 
    return : (Binary_Tree)  tree with derivative of expression
    """

    temp_tree = Binary_Tree(tree.get_root())

    if tree.get_root() in ['+', '-'] and variable in tree_to_string(tree):
        temp_tree.set_left_branch(make_derivative_tree(
            tree.get_left_branch(), variable))
        temp_tree.set_right_branch(make_derivative_tree(
            tree.get_right_branch(), variable))

    elif tree.get_root() == '*' and variable in tree_to_string(tree):
        bt1 = Binary_Tree('*', temp_tree)
        bt1.set_left_branch(make_derivative_tree(
            tree.get_left_branch(), variable))
        bt1.set_right_branch(tree.get_right_branch())

        bt2 = Binary_Tree('*', variable)
        bt2.set_right_branch(tree.get_left_branch())
        bt2.set_left_branch(make_derivative_tree(
            tree.get_right_branch(), variable))

        temp_tree.set_right_branch(bt2)
        temp_tree.set_left_branch(bt1)
        temp_tree.set_root('+')

    elif tree.get_root() == '/' and variable in tree_to_string(tree):
        bt1 = Binary_Tree('*')
        bt1.set_left_branch(make_derivative_tree(
            tree.get_left_branch(), variable))
        bt1.set_right_branch(tree.get_right_branch())

        bt2 = Binary_Tree('*')
        bt2.set_right_branch(tree.get_left_branch())
        bt2.set_left_branch(make_derivative_tree(
            tree.get_right_branch(), variable))

        bt3 = Binary_Tree('-', temp_tree)
        bt3.set_left_branch(bt1)
        bt3.set_right_branch(bt2)
        bt1.set_parent(temp_tree)
        bt2.set_parent(temp_tree)

        bt4 = Binary_Tree('', temp_tree)
        denominator = "{}".format(tree_to_string(tree.get_right_branch()))
        bt4.set_right_branch(denominator)

        temp_tree.set_right_branch(bt4)
        temp_tree.set_left_branch(bt3)
        temp_tree.set_root('/')

    elif tree.get_root() == '^' and variable in tree_to_string(tree):
        if variable not in tree_to_string(tree.get_right_branch()):
            temp_tree.set_root('*')
            temp_tree.set_right_branch(tree.get_right_branch())

            bt1 = Binary_Tree("*", temp_tree)
            bt1.set_right_branch(make_derivative_tree(
                tree.get_left_branch(), variable))

            bt2 = Binary_Tree('^', bt1)
            bt2.insert_left(tree_to_string(tree.get_left_branch()))
            bt2.insert_right(str(int(tree.get_right_branch().get_root())-1))

            bt1.set_left_branch(bt2)
            temp_tree.set_left_branch(bt1)
        else:  # sprawdzić
            bt1 = Binary_Tree('*', temp_tree)
            bt1.set_left_branch(tree.get_right_branch())
            bt1.insert_right('ln')
            bt1.get_right_branch().set_right_branch(tree.get_left_branch())

            bt2 = Binary_Tree('^', temp_tree)
            bt2.set_left_branch(tree.get_left_branch())
            bt2.set_right_branch(tree.get_right_branch())

            temp_tree.set_root('*')
            temp_tree.set_left_branch(make_derivative_tree(bt1, variable))
            temp_tree.set_right_branch(bt2)

    elif tree.get_root() == 'sin' and variable in tree_to_string(tree):
        bt1 = Binary_Tree('cos', temp_tree)
        bt1.set_right_branch(tree.get_right_branch())

        temp_tree.set_root('*')
        temp_tree.set_right_branch(bt1)
        temp_tree.set_left_branch(make_derivative_tree(
            tree.get_right_branch(), variable))

    elif tree.get_root() == 'cos' and variable in tree_to_string(tree):
        bt1 = Binary_Tree('-sin', temp_tree)
        bt1.set_right_branch(tree.get_right_branch())

        temp_tree.set_root('*')
        temp_tree.set_right_branch(bt1)
        temp_tree.set_left_branch(make_derivative_tree(
            tree.get_right_branch(), variable))

    elif tree.get_root() == 'ln' and variable in tree_to_string(tree):
        bt1 = Binary_Tree('/', temp_tree)
        bt1.insert_left('1')
        bt1.set_right_branch(tree.get_right_branch())

        temp_tree.set_root('*')
        temp_tree.set_right_branch(bt1)
        temp_tree.set_left_branch(make_derivative_tree(
            tree.get_right_branch(), variable))

    elif tree.get_root() == 'tg' and variable in tree_to_string(tree):
        temp_tree.set_root('/')
        temp_tree.set_left_branch(make_derivative_tree(
            tree.get_right_branch(), variable))

        bt1 = Binary_Tree('^', temp_tree)
        bt1.insert_right('2')

        bt2 = Binary_Tree('cos', bt1)
        bt2.set_right_branch(tree.get_right_branch())

        bt1.set_left_branch(bt2)
        temp_tree.set_right_branch(bt1)

    elif tree.get_root() == 'sh' and variable in tree_to_string(tree):
        bt1 = Binary_Tree('ch', temp_tree)
        bt1.set_right_branch(tree.get_right_branch())

        temp_tree.set_root('*')
        temp_tree.set_right_branch(bt1)
        temp_tree.set_left_branch(make_derivative_tree(
            tree.get_right_branch(), variable))

    elif tree.get_root() == 'ch' and variable in tree_to_string(tree):
        bt1 = Binary_Tree('sh', temp_tree)
        bt1.set_right_branch(tree.get_right_branch())

        temp_tree.set_root('*')
        temp_tree.set_right_branch(bt1)
        temp_tree.set_left_branch(make_derivative_tree(
            tree.get_right_branch(), variable))

    elif tree.get_root() == variable:
        temp_tree.set_root('1')
    else:
        temp_tree.set_root('0')

    return temp_tree


def get_derivative(exp, variable='x'):
    """Function convert given expression to derivative of expression
    @pam exp:(str) expression to convert
    @pam variable:(str) variable which is respect in derivative
    return: (str)"""
    exp = exp.lower()
    functions = {'sin': 'S', 'cos': 'C', 'tg': 'T',
                 'ln': 'L', 'sh': 'H', 'ch': 'O'}

    for key, val in functions.items():
        exp = exp.replace(key, val)
    exp = exp.replace(' ', '')
    for case in re.findall('[0-9a-z\)]{1}[a-zA-Z\(]{1}', exp):

        exp = exp.replace(case, case[0] + '*' + case[1])

    posix = infix_to_posix(exp, functions)
    exp_tree = make_tree_from_posix(posix, functions)
    dt_tree = make_derivative_tree(exp_tree, variable)
    dt_exp = tree_to_string(dt_tree)
    dt_exp = dt_exp[1:-1]
    copy_exp = ''
    while copy_exp != dt_exp:
        copy_exp = dt_exp
        dt_exp = dt_exp.replace('*1', '')
        dt_exp = dt_exp.replace('+0', '')
        dt_exp = dt_exp.replace('0+', '')
        dt_exp = dt_exp.replace('1*', '')
        dt_exp = dt_exp.replace('^1', '')
        dt_exp = dt_exp.replace('*-', '*(-1)*')
        dt_exp = dt_exp.replace('-*', '*(-1)*')
        dt_exp = dt_exp.replace('()', '')
        dt_exp = re.sub(
            '[0]{1}[*]{1}[^\(\)(sin)(cos)(ln)(tan)(sh)(ch)]{1}', '0', dt_exp)
        dt_exp = re.sub(
            '[^\(\)(sin)(cos)(ln)(tan)(sh)(ch)]{1}[*]{1}[0]', '0', dt_exp)
        dt_exp = re.sub('[0]{1}[*]{1}[\(]{1}[^\)]+[\)]{1}', '0', dt_exp)
        dt_exp = re.sub('[\(]{1}[^\)\(]+[\)][*]{1}[0]{1}', '0', dt_exp)
        for case in re.findall('\({1}[0-9a-z]{1}\){1}', dt_exp):
            dt_exp = dt_exp.replace(case, case[1])

    return dt_exp


if __name__ == '__main__':
    print(get_derivative("(sin(3(x+2)) + cos( x ^ 2 ) ) * ln( x +1) + 1"))
    print(get_derivative("x + x^2 - 3*x"))
    print(get_derivative("(sin(3*(x+2)) + cos( x ^ 2 ) ) * ln( x +1) + s", 's'))
    print(get_derivative(
        "sin(5x) + cos(4x) + tg(x) + sh(3x) + ln(6x) + ch(7x) + sin(x)^(2x)", 'x'))
