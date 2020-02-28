"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.register = [0] * 8
        self.pc = 0
        self.program = []
        self.sp = 7
        self.fl = '00000000'

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value

    def load(self):
        """Load a program into memory."""

        address = 0
        # "./examples/mult.ls8"
        # For now, we've just hardcoded a program:
        commands = open(f'{sys.argv[1]}', "r")
        lines = commands.readlines()
        for i in lines:
            cmd = ''
            if i[0] == '0' or i[0] == '1':
                for j in range(0, len(i) - 1):
                    if (i[j] == '0' or i[j] == '1') and len(cmd) <= 8:
                        cmd += i[j]
                    elif i[j] != '0' or i[j] != '1':
                        break
                self.program += [cmd]


        for instruction in self.program:
            self.ram[address] = instruction
            address += 1

        self.register[7] = len(self.ram) - 5


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""

        # print(self.program)
        running = True
        # operand_a = self.pc + 1
        # operand_b = self.pc + 2
        while running:
            ir = self.ram_read(self.pc)
            
            # LDI
            if ir == '10000010':
                # reg_number = self.ram_read(operand_a)
                # value = self.ram_read(operand_b)
                self.register[int(self.ram_read(self.pc + 1), 2)] = self.ram_read(self.pc + 2)
                self.pc += 3

            # MULT
            if ir == '10100010':
                self.register[0] = int(self.register[int(self.ram_read(self.pc + 1), 2)], 2) * int(self.register[int(self.ram_read(self.pc + 2), 2)], 2)
                self.pc += 3

            # PUSH
            if ir == '01000101':
                print('pushin')
                reg = int(self.ram_read(self.pc + 1), 2)
                val = self.register[reg]
                self.register[7] -= 1
                self.ram_write(int(val, 2), self.register[7])
                self.pc += 2
                print(self.ram)
                print(f'Stack pointer: {self.register[7]}')

            # POP
            if ir == '01000110':
                print('poppin')
                reg = int(self.ram_read(self.pc + 1), 2)
                val = self.ram[self.register[7]]
                self.register[reg] = val
                self.register[7] += 1
                self.pc += 2
                print(self.ram)
                print(f'Stack pointer: {self.register[7]}')

            # CMP
            if ir == '10100111':
                if int(self.register[int(self.ram_read(self.pc + 1))], 2) == int(self.register[int(self.ram_read(self.pc + 2))], 2):
                    self.fl = '00000001'
                elif int(self.register[int(self.ram_read(self.pc + 1))], 2) < int(self.register[int(self.ram_read(self.pc + 2))], 2):
                    self.fl = '00000100'
                elif int(self.register[int(self.ram_read(self.pc + 1))], 2) > int(self.register[int(self.ram_read(self.pc + 2))], 2):
                    self.fl = '00000010'
                self.pc += 3

            # JMP
            if ir == '01010100':
                self.pc = int(self.register[int(self.ram_read(self.pc + 1), 2)], 2)

            # JEQ
            if ir == '01010101':
                if self.fl[len(self.fl) - 1] == '1':
                    self.pc = int(self.register[int(self.ram_read(self.pc + 1), 2)], 2)
                else:
                    self.pc += 2

            # JNE
            if ir == '01010110':
                if self.fl[len(self.fl) - 1] == '0':
                    self.pc = int(self.register[int(self.ram_read(self.pc + 1), 2)], 2)
                else:
                    self.pc += 2

            # PRN
            if ir == '01000111':
                print(int(self.register[int(self.ram_read(self.pc + 1), 2)], 2))
                self.pc += 2

            # HLT
            if ir == '00000001':
                self.pc = 0
                running = False

