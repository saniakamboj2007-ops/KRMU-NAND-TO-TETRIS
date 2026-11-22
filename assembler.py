
import sys
import re
from pathlib import Path


# --------------------------------------------------
# PREDEFINED HACK SYMBOLS
# --------------------------------------------------

SYMBOLS = {
    "SP": 0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4,
    "SCREEN": 16384,
    "KBD": 24576
}

for i in range(16):
    SYMBOLS[f"R{i}"] = i


# --------------------------------------------------
# COMPUTATION TABLE
# --------------------------------------------------

COMP = {
    "0":   "0101010",
    "1":   "0111111",
    "-1":  "0111010",
    "D":   "0001100",
    "A":   "0110000",
    "!D":  "0001101",
    "!A":  "0110001",
    "-D":  "0001111",
    "-A":  "0110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "D+A": "0000010",
    "D-A": "0010011",
    "A-D": "0000111",
    "D&A": "0000000",
    "D|A": "0010101",

    "M":   "1110000",
    "!M":  "1110001",
    "-M":  "1110011",
    "M+1": "1110111",
    "M-1": "1110010",
    "D+M": "1000010",
    "D-M": "1010011",
    "M-D": "1000111",
    "D&M": "1000000",
    "D|M": "1010101"
}


# --------------------------------------------------
# DESTINATION TABLE
# --------------------------------------------------

DEST = {
    "":    "000",
    "M":   "001",
    "D":   "010",
    "MD":  "011",
    "A":   "100",
    "AM":  "101",
    "AD":  "110",
    "AMD": "111"
}


# --------------------------------------------------
# JUMP TABLE
# --------------------------------------------------

JUMP = {
    "":    "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111"
}


class AssemblyError(Exception):
    """Error containing the original assembly source line."""
    pass


def clean_source(source):
    """Remove comments and blank lines, preserving line numbers."""
    instructions = []

    for line_number, original_line in enumerate(
        source.splitlines(), start=1
    ):
        line = original_line.split("//")[0].strip()

        if line:
            instructions.append((line_number, line))

    return instructions


def valid_symbol(symbol):
    return re.fullmatch(
        r"[A-Za-z_.$:][A-Za-z0-9_.$:]*",
        symbol
    ) is not None


def first_pass(instructions):
    """Find labels and assign ROM addresses."""
    rom_address = 0

    for line_number, instruction in instructions:
        if instruction.startswith("("):
            if not instruction.endswith(")"):
                raise AssemblyError(
                    f"Line {line_number}: invalid label declaration"
                )

            label = instruction[1:-1].strip()

            if not valid_symbol(label):
                raise AssemblyError(
                    f"Line {line_number}: invalid label name"
                )

            if label in SYMBOLS:
                raise AssemblyError(
                    f"Line {line_number}: duplicate or reserved label '{label}'"
                )

            SYMBOLS[label] = rom_address

        else:
            rom_address += 1


def encode_a_instruction(instruction, line_number, next_variable):
    """Convert an A-instruction into 16-bit binary."""
    value = instruction[1:]

    if not value:
        raise AssemblyError(
            f"Line {line_number}: missing A-instruction value"
        )

    if value.isdigit():
        address = int(value)

        if address > 32767:
            raise AssemblyError(
                f"Line {line_number}: address must be between 0 and 32767"
            )

    else:
        if not valid_symbol(value):
            raise AssemblyError(
                f"Line {line_number}: invalid symbol '{value}'"
            )

        if value not in SYMBOLS:
            SYMBOLS[value] = next_variable[0]
            next_variable[0] += 1

        address = SYMBOLS[value]

    return format(address, "016b")


def encode_c_instruction(instruction, line_number):
    """Convert a C-instruction into 16-bit binary."""

    if instruction.count("=") > 1 or instruction.count(";") > 1:
        raise AssemblyError(
            f"Line {line_number}: invalid C-instruction format"
        )

    if ";" in instruction:
        left, jump = instruction.split(";")
    else:
        left, jump = instruction, ""

    if "=" in left:
        dest, comp = left.split("=")
    else:
        dest, comp = "", left

    if not comp or dest not in DEST or jump not in JUMP:
        raise AssemblyError(
            f"Line {line_number}: invalid instruction"
        )

    if comp not in COMP:
        raise AssemblyError(
            f"Line {line_number}: invalid computation '{comp}'"
        )

    return "111" + COMP[comp] + DEST[dest] + JUMP[jump]


def assemble(source):
    """Perform the two-pass assembly process."""

    instructions = clean_source(source)

    # Reset to predefined symbols for each assembly.
    global SYMBOLS
    SYMBOLS = {
        "SP": 0,
        "LCL": 1,
        "ARG": 2,
        "THIS": 3,
        "THAT": 4,
        "SCREEN": 16384,
        "KBD": 24576
    }

    for i in range(16):
        SYMBOLS[f"R{i}"] = i

    # First pass: labels.
    first_pass(instructions)

    # Second pass: machine code.
    machine_code = []
    next_variable = [16]

    for line_number, instruction in instructions:

        # Labels do not generate machine instructions.
        if instruction.startswith("("):
            continue

        if instruction.startswith("@"):
            binary = encode_a_instruction(
                instruction,
                line_number,
                next_variable
            )
        else:
            binary = encode_c_instruction(
                instruction,
                line_number
            )

        machine_code.append(binary)

    return machine_code


def main():
    if len(sys.argv) != 2:
        print("Usage: python assembler.py filename.asm")
        return

    input_file = Path(sys.argv[1])

    if not input_file.exists():
        print(f"Error: file not found: {input_file}")
        return

    try:
        source = input_file.read_text(encoding="utf-8")
        machine_code = assemble(source)

        output_file = input_file.with_suffix(".hack")
        output_file.write_text(
            "\n".join(machine_code) + "\n",
            encoding="utf-8"
        )

        print(f"Assembly successful!")
        print(f"Input:  {input_file}")
        print(f"Output: {output_file}")
        print(f"Instructions: {len(machine_code)}")

    except AssemblyError as error:
        print(error)


if __name__ == "__main__":
    main()
