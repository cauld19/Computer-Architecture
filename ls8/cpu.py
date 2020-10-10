"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.reg[7] = 0xF4
        self.pc = 0
        
    def ram_read(self, mar):
        return self.ram[mar]
    
    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr
        

    def load(self):
        """Load a program into memory."""
        
        
        
        if (len(sys.argv)) != 2:
            print("remember to pass the second file name")
            print("usage: python3 fileio.py <second_file_name.py>")
            sys.exit()
            
            
        address = 0
        
        
        try:
            with open(sys.argv[1]) as f:
                for line in f:
                    # parse the file to isolate the binary opcodes
                    possible_number = line[:line.find('#')]
                    if possible_number == '':
                        continue # skip to next iteration of loop
                    
                    instruction = int(possible_number, 2)
                    
                    self.ram[address] = instruction
                    address += 1
                    
                    
                    
        except FileNotFoundError:
            print(f'Error from {sys.argv[0]}: {sys.argv[1]} not found')
            sys.exit()


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
        
        
        
        running = True
        
        while running:
            IR = self.ram_read(self.pc)
            
            num_args = IR >> 6
            
            LDI = 0b10000010
            PRN = 0b01000111
            HLT = 0b00000001
            MUL = 0b10100010
            PUSH = 0b01000101
            POP = 0b01000110
            CALL = 0b01010000
            RET = 0b00010001
            ADD = 0b10100000
            
            
            
            
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            
            if IR == LDI:
                self.reg[operand_a] = operand_b
                # self.pc += 3
                
            elif IR == PRN:
                
                print(self.reg[operand_a])
                # self.pc += 2
                
                
            elif IR == HLT:
                running = False
                
            elif IR == MUL:
                print(self.reg[operand_a] * self.reg[operand_b])
                # self.pc += 3
                
            elif IR == PUSH:
                self.reg[7] -= 1 ## go down one for SP
                
                value = self.reg[operand_a] ## value to push is at pc + 1 adress, push this into register
                
                SP = self.reg[7] ## SP is at reg[7]
                
                self.ram_write(SP, value) ## put the value at adress of SP into ram
                
                # self.pc += 2 ## move to next lines of code
                
            elif IR == POP:
                SP = self.reg[7] ## stak pointer
                
                value = self.ram_read(SP) ## value is what is at the ram address of the SP
                
                self.reg[operand_a] = value ## put the value from the adress of pc + 1 into the register
                
                self.reg[7] += 1 ## move the SP pointer up 1
                
                # self.pc += 2 ## move pc pointer to next lines of memory
                
            elif IR == ADD:
                self.alu("ADD", operand_a, operand_b)
                
                
            elif IR == CALL:
                
                return_address = self.pc + 2
                
                self.reg[7] -= 1
                
                SP = self.reg[7]
                
                self.ram_write(SP, return_address)
                
                subroutine_address = self.reg[operand_a]
                
                self.pc = subroutine_address
                
                
                
                
            elif IR == RET:
                SP = self.reg[7]
                
                return_address = self.ram[SP]
                                
                self.pc = return_address
                
                self.reg[7] += 1
                
                
            else: 
                print ('try again')
                
            sets_pc_directly = ((IR >> 4) & 0b0001) == 1
            
            if not sets_pc_directly:
                self.pc += 1 + num_args
                
        
        
