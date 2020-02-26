"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.sp = 7 # SP is R7

    def load(self):
        """Load a program into memory."""

        if len(sys.argv) != 2: 
            print("Need file name!")
            sys.exit(1)  
        try: 
            address = 0
            with open(sys.argv[1]) as f:
                for line in f: 
                    comment_split = line.split("#")
                    value = comment_split[0].strip()
                    if value == "":
                        continue
                    num = int(value, 2)
                    #print(f"{num:08b}: {num}")
                    #print(value)
                    self.ram[address] = num
                    #print(address)
                    address += 1

        except FileNotFoundError: 
            print("File not found!")  
            sys.exit(2)      

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def ram_read(self, mar):
        return self.ram[mar]   

    def ram_write(self, mdr, mar):
        self.ram[mar] = mdr

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
        # Halt CPU and exit emulator
        HLT = 0b00000001 
        # Set value of register to integer
        LDI = 0b10000010
        # Print numeric value stored in register
        PRN = 0b01000111
        # Multiply the values in two registers together and store the result in registerA
        MUL = 0b10100010
        # Push the value in the given register on the stack
        PUSH = 0b01000101
        # Pop the value at the top of the stack into the given register
        POP = 0b01000110
        

        running = True

        while running: 
            
            ir = self.ram_read(self.pc)
            #print(ir)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            if ir == PRN: 
                print(self.reg[operand_a])
                self.pc += 2
            elif ir == LDI:
                self.reg[operand_a] = operand_b
                self.pc += 3
            elif ir == MUL:
                self.alu("MUL", operand_a, operand_b)
                self.pc += 3    
            elif ir == HLT:
                running = False
                sys.exit(1)       
            elif ir == PUSH:
                #Decrement the sp.
                self.reg[self.sp] -= 1
                # Copy the value in the given register to the address pointed to by sp
                val = self.reg[operand_a]
                self.ram[self.reg[self.sp]] = val
                self.pc += 2

            elif ir == POP:
                # Grab value from the top of the stack
                reg = self.ram[self.pc + 1]
                val = self.ram[self.reg[self.sp]]    
                # Copy the value from the address pointed to by sp to the given register
                self.reg[reg] = val
                # Increment sp
                self.reg[self.sp] += 1
                self.pc += 2
                       


