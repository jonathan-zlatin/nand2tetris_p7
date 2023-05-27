"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing

STACK = 256

commands_dict = {
    "1_arg":
        "@SP\n"
        "M=M-1\n"
        "A=M // gets the arg location\n",

    "2_arguments":
        "// SP--:\n"
        "@SP\n"
        "M=M-1\n"
        "A=M\n"
        "D=M // D=first var in the stack\n"
        "@SP\n"
        "M=M-1\n"
        "A=M\n",

    "advance":
        "// SP++:\n"
        "@SP\n"
        "M=M+1\n",

    "add": "M=D+M\n",
    "sub": "M=M-D\n",
    "and": "M=D&M\n",
    "or": "M=D|M\n",
    "neg": "M=-M\n",
    "not": "M=!M\n",
    "shiftleft": "M=M<<\n",
    "shiftright": "M=M>>\n"
}

stack_dict = {
    "push_D_2_Stack":
        " //now we push constant:\n"
        "@SP\n"
        "A=M\n"
        "M=D\n",
    "advance":
        "// SP++:\n"
        "@SP\n"
        "M=M+1\n",
    "local": "LCL",
    "argument": "ARG",
    "this": "THIS",
    "that": "THAT",
    "temp": "R5"
}


class CodeWriter:
    """Translates VM commands into Hack assembly code."""

    def check_eq(self):
        asm = "// we check if y == x\n"
        asm += "@SP   // SP-- (x)\n"
        asm += "M=M-1\n"
        asm += "A=M\n"
        asm += "D=M // D = SP[TOP] D=x\n"

        asm += "@xIsNegative" + str(self.__inner_counter) + "// SP = x\n"
        asm += "D;JLT\n"

        asm += "// x is positive, lets check y:\n"

        asm += "@SP   // SP-- (y)\n"
        asm += "M=M-1\n"
        asm += "A=M\n"
        asm += "D=M // D = SP[TOP] D=y\n"

        asm += "@yIsNegative" + str(self.__inner_counter) + "\n"
        asm += "D;JLT\n"

        asm += "// if you got here - they both non Negatives: (D=y, SP=y)\n"

        asm += "@SP   // SP++ (x)\n"
        asm += "M=M+1\n"
        asm += "A=M\n"
        asm += "D=D-M // D = y-x\n"

        asm += "@true" + str(self.__inner_counter) + "\n"
        asm += "D;JEQ\n"

        asm += "// x != y:\n"
        asm += "D=0\n"
        asm += "@end" + str(self.__inner_counter) + "\n"
        asm += "0;JMP\n"

        asm += "(yIsNegative" + str(self.__inner_counter) + ") // (SP = y)\n"
        asm += "// x is not negative and y is negative - they are not equal\n"
        asm += "D=0\n"

        asm += "@SP\n"
        asm += "M=M+1 // (SP = x)\n"

        asm += "@end" + str(self.__inner_counter) + "\n"
        asm += "0;JMP\n"

        asm += "(xIsNegative" + str(self.__inner_counter) + ") // SP = x\n"
        asm += "// we know that x is negative. lets check if y is negative:\n"

        asm += "@SP   // SP-- (SP = y)\n"
        asm += "M=M-1\n"

        asm += "A=M\n"
        asm += "D=M // now D is y\n"

        asm += "@boothNegative" + str(self.__inner_counter) + "\n"
        asm += "D;JLT\n"

        asm += "// y >= 0  and x < 0  so x!=y\n"
        asm += "D=0\n"

        asm += "@SP // SP++ (SP = x)\n"
        asm += "M=M+1\n"

        asm += "@end" + str(self.__inner_counter) + "\n"
        asm += "0;JMP\n"

        asm += "(boothNegative" + str(self.__inner_counter) + ") // (SP=y) \n"

        asm += "@SP   // (y)\n"
        asm += "A=M\n"
        asm += "D=M // now D is y\n"

        asm += "@SP // SP++(x)\n"
        asm += "M=M+1\n"
        asm += "A=M\n"
        asm += "D=D-M // y-x (M=x)\n"

        asm += "@true" + str(self.__inner_counter) + "\n"
        asm += "D;JEQ\n"

        asm += "D=0 // if you got here x != y\n"
        asm += "@end" + str(self.__inner_counter) + "\n"
        asm += "0;JMP\n"

        asm += "(true" + str(self.__inner_counter) + ")\n"
        asm += "D=-1\n"

        asm += "(end" + str(self.__inner_counter) + ") // change y into D  (SP = X)\n"

        asm += "@SP // SP-- (x->y)\n"
        asm += "M=M-1\n"
        asm += "A=M\n"
        asm += "M=D // y = D\n"
        return asm

    def check_lt(self):
        asm = "// we check if y > x\n"
        asm += "@SP   // SP-- (x)\n"
        asm += "M=M-1\n"
        asm += "A=M\n"
        asm += "D=M // D = SP[TOP] D=x\n"

        asm += "@xIsNegative" + str(self.__inner_counter) + "// SP = x\n"
        asm += "D;JLT\n"

        asm += "// x is positive, lets check y:\n"

        asm += "@SP   // SP-- (y)\n"
        asm += "M=M-1\n"
        asm += "A=M\n"
        asm += "D=M // D = SP[TOP] D=y\n"

        asm += "@yIsNegative" + str(self.__inner_counter) + "\n"
        asm += "D;JLT\n"

        asm += "// if you got here - they both non Negatives: (D=y, SP=y)\n"

        asm += "@SP   // SP++ (x)\n"
        asm += "M=M+1\n"
        asm += "A=M\n"
        asm += "D=D-M // D = y-x\n"

        asm += "@true" + str(self.__inner_counter) + "\n"
        asm += "D;JLT\n"

        asm += "// x <= y:\n"
        asm += "D=0\n"
        asm += "@end" + str(self.__inner_counter) + "\n"
        asm += "0;JMP\n"

        asm += "(yIsNegative" + str(self.__inner_counter) + ") // (SP = y)\n"
        asm += "// x is not negative and y is negative - x>y\n"
        asm += "D=-1\n"

        asm += "@SP\n"
        asm += "M=M+1 // (SP = x)\n"

        asm += "@end" + str(self.__inner_counter) + "\n"
        asm += "0;JMP\n"

        asm += "(xIsNegative" + str(self.__inner_counter) + ") // SP = x\n"
        asm += "// we know that x is negative. lets check if y is negative:\n"

        asm += "@SP   // SP-- (SP = y)\n"
        asm += "M=M-1\n"

        asm += "A=M\n"
        asm += "D=M // now D is y\n"

        asm += "@boothNegative" + str(self.__inner_counter) + "\n"
        asm += "D;JLT\n"

        asm += "// y >= 0 > x  so x<y\n"
        asm += "D=0\n"

        asm += "@SP // SP++ (SP = x)\n"
        asm += "M=M+1\n"

        asm += "@end" + str(self.__inner_counter) + "\n"
        asm += "0;JMP\n"

        asm += "(boothNegative" + str(self.__inner_counter) + ") // (SP=y) \n"

        asm += "@SP   // (y)\n"
        asm += "A=M\n"
        asm += "D=M // now D is y\n"

        asm += "@SP // SP++(x)\n"
        asm += "M=M+1\n"
        asm += "A=M\n"
        asm += "D=D-M // y-x (M=x)\n"

        asm += "@true" + str(self.__inner_counter) + "\n"
        asm += "D;JLT\n"

        asm += "D=0 // if you got here x < y\n"
        asm += "@end" + str(self.__inner_counter) + "\n"
        asm += "0;JMP\n"

        asm += "(true" + str(self.__inner_counter) + ")\n"
        asm += "D=-1\n"

        asm += "(end" + str(self.__inner_counter) + ") // change y into D  (SP = X)\n"

        asm += "@SP // SP-- (x->y)\n"
        asm += "M=M-1\n"
        asm += "A=M\n"
        asm += "M=D // y = D\n"
        return asm

    def check_gt(self):
        asm = "// we check if y > x\n"
        asm += "@SP   // SP-- (x)\n"
        asm += "M=M-1\n"
        asm += "A=M\n"
        asm += "D=M // D = SP[TOP] D=x\n"

        asm += "@xIsNegative" + str(self.__inner_counter) + "// SP = x\n"
        asm += "D;JLT\n"

        asm += "// x is positive, lets check y:\n"

        asm += "@SP   // SP-- (y)\n"
        asm += "M=M-1\n"
        asm += "A=M\n"
        asm += "D=M // D = SP[TOP] D=y\n"

        asm += "@yIsNegative" + str(self.__inner_counter) + "\n"
        asm += "D;JLT\n"

        asm += "// if you got here - they both non Negatives: (D=y, SP=y)\n"

        asm += "@SP   // SP++ (x)\n"
        asm += "M=M+1\n"
        asm += "A=M\n"
        asm += "D=D-M // D = y-x\n"

        asm += "@true" + str(self.__inner_counter) + "\n"
        asm += "D;JGT\n"

        asm += "// x >= y:\n"
        asm += "D=0\n"
        asm += "@end" + str(self.__inner_counter) + "\n"
        asm += "0;JMP\n"

        asm += "(yIsNegative" + str(self.__inner_counter) + ") // (SP = y)\n"
        asm += "// x is not negative and y is negative - x>y\n"
        asm += "D=0\n"

        asm += "@SP\n"
        asm += "M=M+1 // (SP = x)\n"

        asm += "@end" + str(self.__inner_counter) + "\n"
        asm += "0;JMP\n"

        asm += "(xIsNegative" + str(self.__inner_counter) + ") // SP = x\n"
        asm += "// we know that x is negative. lets check if y is negative:\n"

        asm += "@SP   // SP-- (SP = y)\n"
        asm += "M=M-1\n"

        asm += "A=M\n"
        asm += "D=M // now D is y\n"

        asm += "@boothNegative" + str(self.__inner_counter) + "\n"
        asm += "D;JLT\n"

        asm += "// y >= 0  and x < 0  so x<y\n"
        asm += "D=-1\n"

        asm += "@SP // SP++ (SP = x)\n"
        asm += "M=M+1\n"

        asm += "@end" + str(self.__inner_counter) + "\n"
        asm += "0;JMP\n"

        asm += "(boothNegative" + str(self.__inner_counter) + ") // (SP=y) \n"

        asm += "@SP   // (y)\n"
        asm += "A=M\n"
        asm += "D=M // now D is y\n"

        asm += "@SP // SP++(x)\n"
        asm += "M=M+1\n"
        asm += "A=M\n"
        asm += "D=D-M // y-x (M=x)\n"

        asm += "@true" + str(self.__inner_counter) + "\n"
        asm += "D;JGT\n"

        asm += "D=0 // if you got here x > y\n"
        asm += "@end" + str(self.__inner_counter) + "\n"
        asm += "0;JMP\n"

        asm += "(true" + str(self.__inner_counter) + ")\n"
        asm += "D=-1\n"

        asm += "(end" + str(self.__inner_counter) + ") // change y into D  (SP = X)\n"

        asm += "@SP // SP-- (x->y)\n"
        asm += "M=M-1\n"
        asm += "A=M\n"
        asm += "M=D // y = D\n"
        return asm

    @staticmethod
    def get_segment_val(index):
        return "@" + index + "\n" + "D=A"

    def push_segment_static(self, indx: int) -> str:
        asm = "//we push from: " + str(self.__inner_name) + "." + str(indx) + "\n"
        asm += "@" + str(self.__inner_name) + "." + str(indx) + "\n"
        asm += "D=M\n"
        asm += "@SP\n"
        asm += "A=M\n"
        asm += "M=D\n"
        return asm

    def pop_segment_static(self, indx: int) -> str:
        asm = "//we pop into: " + str(self.__inner_name) + "." + str(indx) + "\n"
        asm += "@SP\n"
        asm += "M=M-1\n"
        asm += "A=M\n"
        asm += "D=M\n"
        asm += "@" + str(self.__inner_name) + "." + str(indx) + "// the address we will charge to" + "\n"
        asm += "M=D \n"
        return asm

    @staticmethod
    def push_segment(segment: str, indx: int, temp: str) -> str:
        asm = "//we push from: " + str(segment) + " in ind " + str(indx) + "\n"
        asm += "@" + str(segment) + "\n"
        asm += "D=" + temp + "\n"
        asm += "@" + str(indx) + "\n"
        asm += "A=A+D\n"
        asm += "D=M\n"
        asm += "@SP\n"
        asm += "A=M\n"
        asm += "M=D\n"
        return asm

    @staticmethod
    def pop_segment(segment: str, indx: int, temp: str) -> str:
        asm = "//we pop into: " + str(segment) + " in ind " + str(indx) + "\n"
        asm += "@" + str(segment) + "\n"
        asm += "D=" + temp + "\n"
        asm += "@" + str(indx) + "\n"
        asm += "D=A+D // the address we will charge to\n"
        asm += "@R13 // save the address here\n"
        asm += "M=D\n"
        asm += "@SP\n"
        asm += "M=M-1\n"
        asm += "A=M\n"
        asm += "D=M\n"
        asm += "@R13\n"
        asm += "A=M // go to the wanted root\n"
        asm += "M=D \n"
        return asm

    def __init__(self, output_stream: typing.TextIO) -> None:
        """Initializes the CodeWriter.

        Args:
            output_stream (typing.TextIO): output stream.
        """
        # Your code goes here!
        # Note that you can write to output_stream like so:
        # output_stream.write("Hello world! \n")
        self.__output_stream = output_stream
        self.__inner_counter: int = 0
        self.__inner_name: str = ""
        self.__inner_func_name: str = ""

    def set_file_name(self, filename: str) -> None:
        """Informs the code writer that the translation of a new VM file is
        started.

        Args:
            filename (str): The name of the VM file.
        """
        # Your code goes here!
        # This function is useful when translating code that handles the
        # static segment. For example, in order to prevent collisions between two
        # .vm files which push/pop to the static segment, one can use the current
        # file's name in the assembly variable's name and thus differentiate between
        # static variables belonging to different files.
        # To avoid problems with Linux/Windows/MacOS differences with regards
        # to filenames and paths, you are advised to parse the filename in
        # the function "translate_file" in Main.py using python's os library,
        # For example, using code similar to:
        # input_filename, input_extension = os.path.splitext(os.path.basename(input_file.name))
        self.__inner_name = str(filename)

    def write_arithmetic(self, command: str) -> None:
        """Writes assembly code that is the translation of the given
        arithmetic command. For the commands eq, lt, gt, you should correctly
        compare between all numbers our computer supports, and we define the
        value "true" to be -1, and "false" to be 0.

        Args:
            command (str): an arithmetic command.
        """
        # Your code goes here!
        self.__inner_counter += 1

        unary_list = ["neg", "not", "shiftleft", "shiftright"]
        equal_list = ["eq", "lt", "gt"]
        if command in unary_list:
            cmd_asm = commands_dict["1_arg"]
            cmd_asm += commands_dict[command]
        elif command in equal_list:
            if command == "eq":
                cmd_asm = self.check_eq()
            elif command == "gt":
                cmd_asm = self.check_gt()
            else:
                cmd_asm = self.check_lt()
        else:
            cmd_asm = commands_dict["2_arguments"]
            cmd_asm += commands_dict[command]
        cmd_asm += commands_dict["advance"]
        self.__output_stream.write(cmd_asm)

    def write_push_pop(self, command: str, segment: str, index: int) -> None:
        """Writes assembly code that is the translation of the given
        command, where command is either C_PUSH or C_POP.

        Args:
            command (str): "C_PUSH" or "C_POP".
            segment (str): the memory segment to operate on.
            index (int): the index in the memory segment.
        """
        # Your code goes here!
        # Note: each reference to "static i" appearing in the file Xxx.vm should
        # be translated to the assembly symbol "Xxx.i". In the subsequent
        # assembly process, the Hack assembler will allocate these symbolic
        # variables to the RAM, starting at address 16.

        stage2_lst = ["argument", "this", "that", "local"]

        if command == "C_PUSH":
            if segment == "constant":
                cmd_asm = self.get_segment_val(index)
                cmd_asm += stack_dict["push_D_2_Stack"] + stack_dict["advance"]
            elif segment in stage2_lst:
                cmd_asm = self.push_segment(stack_dict[segment], index, "M") + stack_dict["advance"]
            elif segment == "temp":
                cmd_asm = self.push_segment(stack_dict[segment], index, "A") + stack_dict["advance"]
            elif segment == "pointer":
                cmd_asm = self.push_segment("THIS", index, "A") + stack_dict["advance"]
            else:
                cmd_asm = self.push_segment_static(index) + stack_dict["advance"]

        elif command == "C_POP":
            if segment in stage2_lst:
                cmd_asm = self.pop_segment(stack_dict[segment], index, "M")
            elif segment == "temp":
                cmd_asm = self.pop_segment(stack_dict[segment], index, "A")
            elif segment == "pointer":
                cmd_asm = self.pop_segment("THIS", index, "A")
            else:
                cmd_asm = self.pop_segment_static(index)
        self.__output_stream.write(cmd_asm)

    def write_label(self, label: str) -> None:
        """Writes assembly code that affects the label command.
        Let "Xxx.foo" be a function within the file Xxx.vm. The handling of
        each "label bar" command within "Xxx.foo" generates and injects the symbol
        "Xxx.foo$bar" into the assembly code stream.
        When translating "goto bar" and "if-goto bar" commands within "foo",
        the label "Xxx.foo$bar" must be used instead of "bar".

        Args:
            label (str): the label to write.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        cmd: str = "//now we put label: " + label + " " + self.__inner_name + " " + self.__inner_func_name + "\n" \
                   + "(" + self.__inner_name + "$" + label + ")\n"
        self.__output_stream.write(cmd)

    def write_goto(self, label: str) -> None:
        """Writes assembly code that affects the goto command.

        Args:
            label (str): the label to go to.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        cmd: str = "// now we do unconditional jump to " + \
                   self.__inner_name + "." + self.__inner_func_name + "$" + label + "\n" + \
                   "@" + self.__inner_name + "$" + label + "\n" + "0;JMP\n"
        self.__output_stream.write(cmd)

    def write_if(self, label: str) -> None:
        """Writes assembly code that affects the if-goto command.

        Args:
            label (str): the label to go to.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        cmd: str = "// now we do conditional jump to " + \
                   self.__inner_name + "." + self.__inner_func_name + "$" + label + "\n" + \
                   "@SP\n" + \
                   "M=M-1\n" + \
                   "A=M\n" + \
                   "D=M\n" + \
                   "@" + self.__inner_name + "$" + label + "\n" + \
                   "D;JMP\n"
        self.__output_stream.write(cmd)


def write_function(self, function_name: str, n_vars: int) -> None:
    """Writes assembly code that affects the function command.
    The handling of each "function Xxx.foo" command within the file Xxx.vm
    generates and injects a symbol "Xxx.foo" into the assembly code stream,
    that labels the entry-point to the function's code.
    In the subsequent assembly process, the assembler translates this
    symbol into the physical address where the function code starts.

    Args:
        function_name (str): the name of the function.
        n_vars (int): the number of local variables of the function.
    """
    # This is irrelevant for project 7,
    # you will implement this in project 8!
    # The pseudo-code of "function function_name n_vars" is:
    # (function_name)       // injects a function entry label into the code
    # repeat n_vars times:  // n_vars = number of local variables
    #   push constant 0     // initializes the local variables to 0
    pass


def write_call(self, function_name: str, n_args: int) -> None:
    """Writes assembly code that affects the call command.
    Let "Xxx.foo" be a function within the file Xxx.vm.
    The handling of each "call" command within Xxx.foo's code generates and
    injects a symbol "Xxx.foo$ret.i" into the assembly code stream, where
    "i" is a running integer (one such symbol is generated for each "call"
    command within "Xxx.foo").
    This symbol is used to mark the return address within the caller's
    code. In the subsequent assembly process, the assembler translates this
    symbol into the physical memory address of the command immediately
    following the "call" command.

    Args:
        function_name (str): the name of the function to call.
        n_args (int): the number of arguments of the function.
    """
    # This is irrelevant for project 7,
    # you will implement this in project 8!
    # The pseudo-code of "call function_name n_args" is:
    # push return_address   // generates a label and pushes it to the stack
    # push LCL              // saves LCL of the caller
    # push ARG              // saves ARG of the caller
    # push THIS             // saves THIS of the caller
    # push THAT             // saves THAT of the caller
    # ARG = SP-5-n_args     // repositions ARG
    # LCL = SP              // repositions LCL
    # goto function_name    // transfers control to the callee
    # (return_address)      // injects the return address label into the code
    pass


def write_return(self) -> None:
    """Writes assembly code that affects the return command."""
    # This is irrelevant for project 7,
    # you will implement this in project 8!
    # The pseudo-code of "return" is:
    # frame = LCL                   // frame is a temporary variable
    # return_address = *(frame-5)   // puts the return address in a temp var
    # *ARG = pop()                  // repositions the return value for the caller
    # SP = ARG + 1                  // repositions SP for the caller
    # THAT = *(frame-1)             // restores THAT for the caller
    # THIS = *(frame-2)             // restores THIS for the caller
    # ARG = *(frame-3)              // restores ARG for the caller
    # LCL = *(frame-4)              // restores LCL for the caller
    # goto return_address           // go to the return address
    pass
