class UecBasic:
    def __init__(self):
        self.code = {}
        self.vars = {}

    def parse(self, code: str):
        self.code = {}
        lines = code.split("\n")
        for line in lines:
            tokens = line.split()
            if tokens:
                self.code[int(tokens[0].strip())] = " ".join(tokens[1:])

    def eval_expr(self, expr: str):
        try:
            return eval(expr, {}, self.vars)
        except Exception as e:
            raise SyntaxError(f"Invalid expression: {expr}") from e

    def run(self, code: str):
        self.parse(code)
        sequence = sorted(self.code.keys())
        index = -1
        while_stack = []

        while True:
            index += 1
            if index >= len(sequence):
                return
            pc = sequence[index]
            line = self.code[pc]

            if line.upper().startswith("PRINT"):
                to_print = line[len("PRINT"):].strip()
                print(self.eval_expr(to_print))
            elif line.upper().startswith("GOTO"):
                target = line[len("GOTO"):].strip()
                if target.isdigit():
                    pc = int(target)
                    if pc in self.code:
                        index = sequence.index(pc) - 1
                    else:
                        raise ValueError(f"Line number {pc} does not exist")
                else:
                    raise ValueError(f"Invalid GOTO target: {target}")
            elif line.upper().startswith("LET"):
                var_assignment = line[len("LET"):].strip()
                var_name, expr = var_assignment.split("=", 1)
                var_name = var_name.strip()
                self.vars[var_name] = self.eval_expr(expr.strip())
            elif line.upper().startswith("IF"):
                condition, _, rest = line[len("IF"):].partition("GOTO")
                if self.eval_expr(condition.strip()):
                    target_line = int(rest.strip())
                    if target_line in self.code:
                        index = sequence.index(target_line) - 1
                    else:
                        raise ValueError(f"Line number {target_line} does not exist")
            elif line.upper().startswith("WHILE"):
                condition = line[len("WHILE"):].strip()
                if self.eval_expr(condition):
                    while_stack.append((pc, condition))
                else:
                    while True:
                        index += 1
                        if index >= len(sequence):
                            return
                        pc = sequence[index]
                        line = self.code[pc]
                        if line.upper().startswith("LOOP"):
                            break
            elif line.upper().startswith("LOOP"):
                if while_stack:
                    start_pc, condition = while_stack[-1]
                    if self.eval_expr(condition):
                        index = sequence.index(start_pc) - 1
                    else:
                        while_stack.pop()
            elif line.upper().startswith("EXIT"):
                return
            else:
                raise SyntaxError(f"Unknown command: {line}")

def console():
    print("UEC Basic")
    print("(c) 2024 Kajizuka Taichi. All rights reserved")
    print("Created by student of UEC programming class")

    interpreter = UecBasic()
    code = []
    while True:
        inputed = input(">>> ")
        if inputed.upper() == "RUN":
            try:
                interpreter.run("\n".join(code))
            except Exception as e:
                print(f"Error: {e}")
            else:
                print("Ok")
            finally:
                code = []
        else:
            code.append(inputed)

console()
