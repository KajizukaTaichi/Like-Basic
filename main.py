import shutil
import time
import pyfiglet
import os
import random
import math
import datetime

class LikeBasic:
    """Interpreter of Like Basic"""
    def __init__(self):
        self.code = {}  # Stores the parsed code with line numbers as keys
        
        # Stores variables and their values
        self.vars = {
            "INPUT": input,
            "STR": str,
            "INT": int,
            "FLOAT": float,
            "LIST": list,
            "RAND": random.random,
            "ROUND": round,
            "SIN": math.sin,
            "COS": math.cos,
            "TAN": math.tan,
            "NOW": datetime.datetime.now
        }
        
    def parse(self, code: str):
        self.code = {}
        lines = code.split("\n")  # Split the input code into lines
        for line in lines:
            tokens = line.split()  # Tokenize each line
            if tokens:
                # Store the line number as key and the rest of the line as value
                self.code[int(tokens[0].strip())] = " ".join(tokens[1:])

    def eval_expr(self, expr: str):
        # Evaluate expressions using the stored variables
        return eval(expr, {}, self.vars)

    def run(self, code: str):
        self.parse(code)  # Parse the input code
        sequence = sorted(self.code.keys())  # Sort line numbers
        index = -1 # Index of sequence line
        while_stack = []  # Stack to handle WHILE loops
        on_error_goto = None # Goto number when happen error
        is_success = True # Flag of success to run

        while True:
            try:
                index += 1
                if is_success:
                    if index >= len(sequence):
                        return  # Exit if all lines are executed
                    self.pc = sequence[index]
                else:
                    is_success = True
            
                line = self.code[self.pc]
            
                # Standards outout
                if line.startswith("PRINT"):
                    to_print = line[len("PRINT"):].strip() # Print
                    print("".join(list(map(lambda x: str(self.eval_expr(x)), to_print.split(";")))), end="")

                # Goto Statement
                elif line.startswith("GOTO"):
                    target = self.eval_expr(line[len("GOTO"):].strip())
                    if target in self.code:
                        index = sequence.index(target) - 1
                    else:
                        raise ValueError(f"Line number {target} does not exist")

                # Define variable
                elif line.startswith("LET"):
                    var_assignment = line[len("LET"):].strip()
                    var_name, expr = var_assignment.split("=", 1)
                    var_name = var_name.strip()
                    self.vars[var_name] = self.eval_expr(expr.strip())  # Assign value to variable

                # IF statement 
                elif line.startswith("IF"):
                    condition, _, rest = line[len("IF"):].partition("THEN")
                    if "ELSE" in rest: # Check it there ELSE section
                        true, _, false = rest.partition("ELSE")
                        if self.eval_expr(condition.strip()):
                            target_line = int(self.eval_expr(true.strip()))
                            if target_line in self.code:
                                index = sequence.index(target_line) - 1
                            else:
                                raise ValueError(f"Line number {target_line} does not exist")
                        else:
                            target_line = int(self.eval_expr(false.strip()))
                            if target_line in self.code:
                                index = sequence.index(target_line) - 1
                            else:
                                raise ValueError(f"Line number {target_line} does not exist")
                    else:
                        if self.eval_expr(condition.strip()):
                            target_line = int(self.eval_expr(rest.strip()))
                            if target_line in self.code:
                                index = sequence.index(target_line) - 1
                            else:
                                raise ValueError(f"Line number {target_line} does not exist")

                # WHILE statement
                elif line.startswith("WHILE"):
                    condition = line[len("WHILE"):].strip()
                    if self.eval_expr(condition):
                        while_stack.append((self.pc, condition))  # Push to stack
                    else:
                        while True:
                            index += 1
                            if index >= len(sequence):
                                return
                            self.pc = sequence[index]
                            line = self.code[self.pc]
                            if line.startswith("LOOP"):
                                break  # Exit WHILE loop

                # End of the loop
                elif line.startswith("LOOP"):
                    if while_stack:
                        start_pc, condition = while_stack[-1]
                        if self.eval_expr(condition):
                            index = sequence.index(start_pc) - 1  # Loop back to WHILE
                        else:
                            while_stack.pop()  # Pop from stack

                # IF statement 
                elif line.startswith("ON ERROR"):
                    on_error_goto = int(self.eval_expr(line[len("ON ERROR"):].strip()))

                elif line == "SPQR":
                    print("Senātus Populusque Rōmānus")
                elif line == "CCCP":
                    print("Союз Советских Социалистических Республик")

                # Exit running
                elif line.startswith("EXIT"):
                    return  # Exit the interpreter
                else:
                    raise SyntaxError(f"Unknown command \"{line}\"")

            except Exception as e:
                if isinstance(on_error_goto, int):
                    self.pc = on_error_goto
                    is_success = False
                    continue
                else:
                    raise ValueError(e)
                        

class bcolors:
    # ANSI escape codes for terminal text colors and styles
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def clear_console():
    command = "clear"
    if os.name in ("nt", "dos"):
        command = "cls"  # Use 'cls' for Windows systems

    os.system(command)  # Clear the console

def get_terminal_size():
    columns, rows = shutil.get_terminal_size(fallback=(80, 20))  # Get terminal size
    return columns, rows

def print_text_at_position(text, start_col):
    columns, rows = get_terminal_size()
    lines = text.split('\n')
    padding_top = (rows - len(lines)) // 2  # Calculate top padding for centering
    padded_text = "\n" * padding_top + "\n".join(
        ' ' * start_col + line for line in lines
    )
    print(f'{bcolors.OKBLUE}{padded_text}{bcolors.ENDC}')  # Print with padding

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear the screen

def anime(text):
    delay = 0.002  # Initial delay
    final_delay = 3  # Delay after animation

    ascii_art = pyfiglet.figlet_format(text)  # Generate ASCII art
    ascii_art_width = max(len(line) for line in ascii_art.split('\n'))

    terminal_width, terminal_height = get_terminal_size()
    start_col = terminal_width - ascii_art_width

    while start_col > (terminal_width - ascii_art_width) // 2:
        clear_screen()
        if start_col < (terminal_width / 2.4):
            delay += terminal_width / 10000 # Increase delay
        
        print_text_at_position(ascii_art, start_col)
        start_col -= 1
        time.sleep(delay)

    clear_screen()
    print_text_at_position(ascii_art, (terminal_width - ascii_art_width) // 2)
    time.sleep(final_delay)
    input(" " * ((terminal_width // 2) - (ascii_art_width // 4)) + "Enter to start REPL")

def repl():
    interpreter = LikeBasic()
    code = []
    while True:
        inputed = input("> ").strip()

        if len(inputed.split(" ")) > 1 and inputed.split(" ")[0].isdigit():
            code.append(inputed)  # Add input to code
        elif inputed == "RUN":
            try:
                interpreter.run("\n".join(code))  # Run the accumulated code
            except Exception as e:
                print(f"{bcolors.FAIL}Error{bcolors.ENDC} at line {interpreter.pc}: {e}")
            else:
                print(f"{bcolors.OKGREEN}Okay{bcolors.ENDC}")
        
        elif inputed.startswith("DEL"):
            try:
                line = int(inputed[len("DEL"):].strip())
                code = [item for item in code if not (item.split(" ")[0] == str(line))]
                print(f"Line {line} is deleted")
            except:
                print("Invalid line number")

        # Clear the code
        elif inputed == "CLEAR":
            code = []
            print("Code is cleared")

        # Show the code
        elif inputed == "CODE":
            print("\n".join([f"{key} {value}" for key, value in sorted(interpreter.code.items())]))

        # Save at the file
        elif inputed == "SAVE":
            try:
                with open(input("File name: "), "w", encoding="utf-8") as f:
                    f.write("\n".join(code))
                    print("Saved")
            except:
                print("Fault save")
        
        # Load from script file
        elif inputed == "LOAD":
            try:
                with open(input("File name: "), "r", encoding="utf-8") as f:
                    code = f.read().split("\n")
                    print("Loaded")
            except:
                print("Not found")
        
        # Exit REPL
        elif inputed == "EXIT":
            exit(0)
        elif inputed != "":
            try:
                interpreter.run(f"10 {inputed}")  # Run the accumulated code
            except Exception as e:
                print(f"{bcolors.FAIL}Error{bcolors.ENDC}: {e}")
            else:
                print(f"{bcolors.OKGREEN}Okay{bcolors.ENDC}")
        
        interpreter.parse("\n".join(code))

if __name__ == "__main__":
    anime("Like Basic") # Show logo anime

    clear_console()
    print(f"{bcolors.BOLD}{bcolors.OKBLUE}Like Basic{bcolors.ENDC}{bcolors.ENDC}")
    print("(c) 2024 Kajizuka Taichi. All rights reserved")
    print("-" * 50)

    repl()  # Start the REPL
