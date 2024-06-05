import shutil
import time
import pyfiglet
import os
import random
import math
import datetime

class UecBasic:
    """Interpreter of UEC Basic"""
    def __init__(self):
        self.code = {}  # Stores the parsed code with line numbers as keys
        # Stores variables and their values
        self.vars = {
            "math": math, 
            "datetime": datetime, 
            "os": os
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
        try:
            # Evaluate expressions using the stored variables
            return eval(expr, {}, self.vars)
        except Exception as e:
            raise SyntaxError(f"Invalid expression: {expr}") from e

    def run(self, code: str):
        self.parse(code)  # Parse the input code
        sequence = sorted(self.code.keys())  # Sort line numbers
        index = -1 # Index of sequence line
        while_stack = []  # Stack to handle WHILE loops

        while True:
            index += 1
            if index >= len(sequence):
                return  # Exit if all lines are executed
            pc = sequence[index]
            line = self.code[pc]

        
            # Standards outout
            if line.upper().startswith("PRINT"):
                to_print = line[len("PRINT"):].strip() # Print
                print("".join(list(map(lambda x: str(self.eval_expr(x)), to_print.split(",")))))

            # Random value
            elif line.upper().startswith("RAND"):
                variable = line[len("RAND"):].strip()
                self.vars[variable] = random.random()  # Generate a random number

            # Input
            elif line.upper().startswith("INPUT"):
                variable = line[len("INPUT"):].strip()
                self.vars[variable] = input()  # Read input from user

            # Goto Statement
            elif line.upper().startswith("GOTO"):
                target = line[len("GOTO"):].strip()
                if target.isdigit():
                    pc = int(target)
                    if pc in self.code:
                        index = sequence.index(pc) - 1  # Jump to the target line
                    else:
                        raise ValueError(f"Line number {pc} does not exist")
                else:
                    raise ValueError(f"Invalid GOTO target: {target}")

            # Define variable
            elif line.upper().startswith("LET"):
                var_assignment = line[len("LET"):].strip()
                var_name, expr = var_assignment.split("=", 1)
                var_name = var_name.strip()
                self.vars[var_name] = self.eval_expr(expr.strip())  # Assign value to variable

            # IF statement 
            elif line.upper().startswith("IF"):
                condition, _, rest = line[len("IF"):].partition("THEN")
                if "ELSE" in rest: # Check it there ELSE section
                    true, _, false = rest.partition("ELSE")
                    if self.eval_expr(condition.strip()):
                        target_line = int(true.strip())
                        if target_line in self.code:
                            index = sequence.index(target_line) - 1
                        else:
                            raise ValueError(f"Line number {target_line} does not exist")
                    else:
                        target_line = int(false.strip())
                        if target_line in self.code:
                            index = sequence.index(target_line) - 1
                        else:
                            raise ValueError(f"Line number {target_line} does not exist")
                else:
                    if self.eval_expr(condition.strip()):
                        target_line = int(rest.strip())
                        if target_line in self.code:
                            index = sequence.index(target_line) - 1
                        else:
                            raise ValueError(f"Line number {target_line} does not exist")

            # WHILE statement
            elif line.upper().startswith("WHILE"):
                condition = line[len("WHILE"):].strip()
                if self.eval_expr(condition):
                    while_stack.append((pc, condition))  # Push to stack
                else:
                    while True:
                        index += 1
                        if index >= len(sequence):
                            return
                        pc = sequence[index]
                        line = self.code[pc]
                        if line.upper().startswith("LOOP"):
                            break  # Exit WHILE loop

            # End of the loop
            elif line.upper().startswith("LOOP"):
                if while_stack:
                    start_pc, condition = while_stack[-1]
                    if self.eval_expr(condition):
                        index = sequence.index(start_pc) - 1  # Loop back to WHILE
                    else:
                        while_stack.pop()  # Pop from stack

            # Exit running
            elif line.upper().startswith("EXIT"):
                return  # Exit the interpreter
            else:
                raise SyntaxError(f"Unknown command: {line}")

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
    delay = 0.0005  # Initial delay
    final_delay = 2  # Delay after animation

    ascii_art = pyfiglet.figlet_format(text)  # Generate ASCII art
    ascii_art_width = max(len(line) for line in ascii_art.split('\n'))

    terminal_width, terminal_height = get_terminal_size()
    start_col = terminal_width - ascii_art_width

    while start_col > (terminal_width - ascii_art_width) // 2:
        clear_screen()
        delay += terminal_width / 40000  # Increase delay
        print_text_at_position(ascii_art, start_col)
        start_col -= 1
        time.sleep(delay)

    clear_screen()
    print_text_at_position(ascii_art, (terminal_width - ascii_art_width) // 2)
    time.sleep(final_delay)
    input(" " * ((terminal_width // 2) - (ascii_art_width // 4)) + "Enter to start REPL")

def repl():
    interpreter = UecBasic()
    code = []
    while True:
        inputed = input("> ").strip()

        if len(inputed.split(" ")) > 1 and inputed.split(" ")[0].isdigit():
            code.append(inputed)  # Add input to code
        elif inputed.upper() == "RUN":
            try:
                interpreter.run("\n".join(code))  # Run the accumulated code
            except Exception as e:
                print(f"{bcolors.FAIL}Error{bcolors.ENDC}: {e}")
            else:
                print(f"{bcolors.OKGREEN}Okay{bcolors.ENDC}")
        
        elif inputed.upper().startswith("DEL"):
            try:
                line = int(inputed[len("DEL"):].strip())
                code = [item for item in code if not (item.split(" ")[0] == str(line))]
                print(f"Line {line} is deleted")
            except:
                print("Invalid line number")

        # Clear the code after running
        elif inputed.upper() == "CLEAR":
            code = []
            print("Code is cleared")

        # Save at the file
        elif inputed.upper() == "SAVE":
            try:
                with open(input("File name: "), "w", encoding="utf-8") as f:
                    f.write("\n".join(code))
                    print("Saved")
            except:
                print("Fault save")
        
        # Load from script file
        elif inputed.upper() == "LOAD":
            try:
                with open(input("File name: "), "r", encoding="utf-8") as f:
                    code = f.read().split("\n")
                    print("Loaded")
            except:
                print("Not found")
        
        # Exit REPL
        elif inputed.upper() == "EXIT":
            exit(0)
        elif inputed != "":
            try:
                interpreter.run(f"10 {inputed}")  # Run the accumulated code
            except Exception as e:
                print(f"{bcolors.FAIL}Error{bcolors.ENDC}: {e}")
            else:
                print(f"{bcolors.OKGREEN}Okay{bcolors.ENDC}")
        
if __name__ == "__main__":
    anime("UEC Basic") # Show logo anime

    clear_console()
    print(f"{bcolors.BOLD}{bcolors.OKBLUE}UEC Basic{bcolors.ENDC}{bcolors.ENDC}")
    print("(c) 2024 Kajizuka Taichi. All rights reserved")
    print("Created by student of UEC programming class")
    print("-" * 50)

    repl()  # Start the REPL
