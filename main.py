class UecBasic:
    def __init__(self):
        self.code: dict = {}

    def parse(self, code: str):
        self.code = {}
        lines: list[str] = code.split("\n")
        for line in lines:
            tokens: list[str] = line.split(" ")
            self.code[int(tokens[0].strip())] = " ".join(tokens[1:])

    def run(self, code: str):
        self.parse(code)
        sequence = sorted(self.code.keys())
        index: int = -1
        is_goto = False

        while True:
            if is_goto == False:
                index += 1
                try:
                    pc = sequence[index]
                except IndexError:
                    return
                line: str = self.code[pc]
                line: str = line.lower()

            if "print" in line:
                print(eval(line.replace("print", "", 1)))
            elif "goto" in line:
                pc = line.replace("goto", "", 1).strip()
                line = self.code[int(pc)].lower()
                is_goto = True
                continue
            elif "exit" in line:
                exit(0)
            else:
                exec(line)

def console():
    print("UEC Basic")
    print("(c) 2024 Kajizuka Taichi. All rights reserved")
    print("Create by student of UEC programming class")

    interpreter = UecBasic()
    code: list = []
    while True: 
        inputed = input(">>> ")
        if inputed == "RUN":
            try:
                interpreter.run("\n".join(code))
            except Exception as e:
                print(f"ERRPR: {e}")
            else:
                print("OK")
            finally:
                code = []
        else:
            code.append(inputed)

console()
