import ast
import tokenize
import math
from io import BytesIO

def count_loc(source_code: str):
    lines = source_code.split('\n')
    total_lines = len(lines)
    comment_lines = [line for line in lines if line.strip().startswith("#")]
    code_lines = [line for line in lines if line.strip() and not line.strip().startswith("#")]
    code_and_comment_lines = [line for line in lines if line.strip()]

    return {
        "loc_total": total_lines,
        "loc_comments": len(comment_lines),
        "loc_code_and_comment": len(code_and_comment_lines),
        "loc_executable": len(code_lines)  # ✅ Ini sama seperti sebelumnya
    }

class BranchCountVisitor(ast.NodeVisitor):
    def __init__(self):
        self.branch_count = 0

    def visit_If(self, node):
        self.branch_count += 2  # if → true & false
        self.generic_visit(node)

    def visit_For(self, node):
        self.branch_count += 2  # loop & exit
        self.generic_visit(node)

    def visit_While(self, node):
        self.branch_count += 2
        self.generic_visit(node)

    def visit_Try(self, node):
        self.branch_count += 1  # try block
        self.branch_count += len(node.handlers)  # each except
        if node.orelse:
            self.branch_count += 1  # else
        if node.finalbody:
            self.branch_count += 1  # finally
        self.generic_visit(node)


class McCabeVisitor(ast.NodeVisitor):
    def __init__(self):
        self.complexity = 1  # start from 1

    def visit_If(self, node): self.complexity += 1; self.generic_visit(node)
    def visit_For(self, node): self.complexity += 1; self.generic_visit(node)
    def visit_While(self, node): self.complexity += 1; self.generic_visit(node)
    def visit_With(self, node): self.complexity += 1; self.generic_visit(node)
    def visit_IfExp(self, node): self.complexity += 1; self.generic_visit(node)
    def visit_BoolOp(self, node): self.complexity += len(node.values) - 1; self.generic_visit(node)
    def visit_Try(self, node): self.complexity += len(node.handlers); self.generic_visit(node)
    def visit_And(self, node): self.complexity += 1
    def visit_Or(self, node): self.complexity += 1


class DesignComplexityVisitor(ast.NodeVisitor):
    def __init__(self):
        self.edges = 0
        self.nodes = 0

    def _is_decision_node(self, node):
        return isinstance(node, (ast.If, ast.For, ast.While, ast.Try))

    def _contains_call(self, node):
        return any(isinstance(child, ast.Call) for child in ast.walk(node))

    def visit(self, node):
        # Jika node adalah percabangan DAN mengandung function call
        if self._is_decision_node(node) and self._contains_call(node):
            self.nodes += 1
            if isinstance(node, ast.If):
                self.edges += 2  # true/false branch
            elif isinstance(node, ast.While) or isinstance(node, ast.For):
                self.edges += 2  # loop + exit
            elif isinstance(node, ast.Try):
                self.edges += len(node.handlers) + 1  # 1 for try, rest for excepts
        self.generic_visit(node)

    def design_complexity(self):
        # Cyclomatic complexity dari subgraf design:
        # v(G) = E - N + 2
        return self.edges - self.nodes + 2 if self.nodes > 0 else 1


def count_cyclomatic_complexity(source_code: str) -> int:
    tree = ast.parse(source_code)
    visitor = McCabeVisitor()
    visitor.visit(tree)
    return visitor.complexity


def count_design_complexity(source_code: str) -> int:
    tree = ast.parse(source_code)
    visitor = DesignComplexityVisitor()
    visitor.visit(tree)
    return visitor.design_complexity()


def count_essential_complexity(source_code: str, cyclomatic_complexity: int) -> int:
    tree = ast.parse(source_code)

    def is_reducible_function(node):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            return False

        # Cek apakah ada nested branching (if dalam if, try dalam for, dll)
        branching_nodes = (ast.If, ast.For, ast.While, ast.Try)
        for child in ast.walk(node):
            if isinstance(child, branching_nodes):
                for grandchild in ast.iter_child_nodes(child):
                    if isinstance(grandchild, branching_nodes):
                        return False  # tangled
        return True  # hanya branching level 1 → modular

    # m = jumlah fungsi yang terstruktur (tidak tangled)
    m = sum(1 for node in ast.walk(tree) if is_reducible_function(node))
    ev = cyclomatic_complexity - m
    return max(ev, 1)

def count_branch_count(source_code: str) -> int:
    tree = ast.parse(source_code)
    visitor = BranchCountVisitor()
    visitor.visit(tree)
    return visitor.branch_count


def count_halstead_metrics(source_code: str):
    tokens = tokenize.tokenize(BytesIO(source_code.encode('utf-8')).readline)
    operators = []
    operands = []

    keywords = set([
        'def', 'return', 'if', 'else', 'elif', 'for', 'while', 'try', 'except', 'with',
        'import', 'from', 'as', 'class', 'pass', 'break', 'continue', 'and', 'or', 'not',
        'in', 'is', 'lambda', 'yield', 'assert', 'raise', 'global', 'nonlocal'
    ])

    for toknum, tokval, *_ in tokens:
        if toknum == tokenize.OP or tokval in ['+=', '-=', '*=', '/=']:
            operators.append(tokval)
        elif toknum == tokenize.NAME:
            if tokval in keywords:
                operators.append(tokval)
            else:
                operands.append(tokval)

    n1 = len(set(operators))
    n2 = len(set(operands))
    N1 = len(operators)
    N2 = len(operands)

    vocabulary = n1 + n2
    length = N1 + N2
    volume = length * math.log2(vocabulary) if vocabulary > 0 else 0
    difficulty = (n1 / 2) * (N2 / n2) if n2 > 0 else 0
    effort = volume * difficulty
    level = (2 * n2) / (n1 * N2) if (n1 * N2) > 0 else 0
    content = level * volume
    stroud_number = 18
    time = effort / stroud_number
    error_estimate = volume / 3000

    return {
        "num_unique_operators": n1,
        "num_unique_operands": n2,
        "num_operators": N1,
        "num_operands": N2,
        "halstead_vocab": vocabulary,
        "halstead_length": length,
        "halstead_volume": volume,
        "halstead_difficulty": difficulty,
        "halstead_effort": effort,
        "halstead_level": level,
        "halstead_content": content,
        "halstead_prog_time": time,
        "halstead_error_est": error_estimate
    }


def analyze_python_file(file_path: str) -> dict:
    with open(file_path, "r", encoding="utf-8") as f:
        source_code = f.read()

    loc = count_loc(source_code)
    hal = count_halstead_metrics(source_code)

    return {
        "loc_total": loc["loc_total"],
        "halstead_prog_time": hal["halstead_prog_time"],
        "num_operands": hal["num_operands"],
        "loc_code_and_comment": loc["loc_code_and_comment"],
        "num_operators": hal["num_operators"],
        "loc_executable": loc["loc_executable"],
        "halstead_level": hal["halstead_level"],
        "branch_count": count_branch_count(source_code),
        "design_complexity": count_design_complexity(source_code),
        "halstead_length": hal["halstead_length"],
        "essential_complexity": count_essential_complexity(source_code, count_cyclomatic_complexity(source_code)),
        "loc_comments": loc["loc_comments"],
        "halstead_difficulty": hal["halstead_difficulty"],
        "num_unique_operators": hal["num_unique_operators"],
        "halstead_error_est": hal["halstead_error_est"],
        "halstead_content": hal["halstead_content"],
        "num_unique_operands": hal["num_unique_operands"],
        "halstead_effort": hal["halstead_effort"],
        "cyclomatic_complexity": count_cyclomatic_complexity(source_code),
        "halstead_volume": hal["halstead_volume"]
    }

