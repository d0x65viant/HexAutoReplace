#!/usr/bin/python3
import os
import re
from random import randbytes
class OffSetsGenerator:
    '''
    Generates datasets, in the form of two tuples, 
    where the first tuple is a set of offsets, 
    and the second tuple is the replacement bytes.
    '''
    def offsets_gen(self, file_hex, source_replace_offsets):
        self.surc_off=source_replace_offsets
        self.size_file_hex=os.stat(file_hex).st_size
        self.gen_non_stop=True

        with open(self.surc_off, 'r', encoding='utf-8') as r_file:
            for line in r_file:

                line=line.lower()

                line_list=[re.findall(r'\w+', i.strip()) for i in line.split('-')]
                
                if len(line_list)<2 or len(line_list)>2:
                    print('ERROR: The wrong format was used!')
                    return
                
                if len(line[0]) != len(line[1]):
                    print('ERROR: The number of offsets does not '
                          'correspond to the number of bytes!')
                    return

                list_ofst, list_byte = tuple(line_list[0]), tuple(line_list[1])

                if "rand" in list_ofst:
                    print("ERROR: Offsets cannot be specified as random bytes!")
                    return
                
                list_byte = tuple([f'0x{randbytes(1).hex()}' if el=="rand" else el for el in list_byte])

                for _list in list_ofst, list_byte:
                    for hexnum in _list:

                        two_num=set([ True  if  i in "0123456789abcdef" 
                                               else 
                                      False for i in hexnum.lstrip('0x')
                                    ])

                        if  not re.match(r'0x', hexnum):
                            print('ERROR: The hexadecimal number format is incorrect, '
                                  '\nthe prefix [0x..] is missing!')
                            return
                        
                        if  (len(hexnum.lstrip('0x'))<1 or len(hexnum.lstrip('0x'))>2 and _list==list_byte or len(two_num)!=1 or False in two_num):
                            print('ERROR: Incorrect byte writing format, each byte must '
                                  '\nbe written as a two-digit number in '
                                  '\nhexadecimal notation with the prefix [0x]!')
                            return
                    
                    if _list==list_ofst:
                        repl_list=[]
                        for hex_num in list_ofst:
                            int_num=int(hex_num, base=16)
                            if  int_num > self.size_file_hex-1:
                                print("ERROR: The specified offset byte cannot exceed the file size!")
                                return
                            repl_list.append(int_num)
                        list_ofst=tuple(repl_list)

                    if _list==list_byte:
                        repl_list=[]
                        for hex_num in list_byte:
                            int_num=int(hex_num, base=16)
                            hex_num="{:02x}".format(int_num)
                            byte=bytes.fromhex(hex_num)
                            repl_list.append(byte)
                        list_byte=tuple(repl_list)
                
                yield (list_ofst, list_byte)

        self.gen_non_stop=False
