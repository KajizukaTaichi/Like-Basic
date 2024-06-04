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
        is_goto = False

        while True:
            if not is_goto:
                index += 1
                if index >= len(sequence):
                    return
                pc = sequence[index]
                line = self.code[pc].lower()

            is_goto = False

            if line.startswith("print"):
                to_print = line[len("print"):].strip()
                print(self.eval_expr(to_print))
            elif line.startswith("goto"):
                target = line[len("goto"):].strip()
                if target.isdigit():
                    pc = int(target)
                    if pc in self.code:
                        index = sequence.index(pc) - 1
                        is_goto = True
                    else:
                        raise ValueError(f"Line number {pc} does not exist")
                else:
                    raise ValueError(f"Invalid GOTO target: {target}")
            elif line.startswith("let"):
                var_assignment = line[len("let"):].strip()
                var_name, expr = var_assignment.split("=", 1)
                var_name = var_name.strip()
                self.vars[var_name] = self.eval_expr(expr.strip())
            elif line.startswith("exit"):
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
                print(f"ERROR: {e}")
            else:
                print("OK")
            finally:
                code = []
        else:
            code.append(inputed)

console()
