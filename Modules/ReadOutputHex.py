#!/usr/bin/python3
import mmap
import re
import string
import shutil
import binascii
import os
from pathlib import PurePath
from Modules.OffSetsGenerator import OffSetsGenerator
from Modules.CheckExistFiles import CheckExistFiles

class ReadOutputHex(OffSetsGenerator):
    def __init__(self, path=None, source_replace_offsets=None):
        # ascii punctuations
        self.ascii_punct=string.punctuation.encode('ascii')
        # define filepath
        self.filepath=path if path else None
        # file with offsets
        self.soreof=source_replace_offsets
        # string in hexadecimal format
        self.hex_line=[]
        # decoded bytes
        self.dec=[]

        if  self.filepath and self.soreof:
            self.read_output_hex_data()
        

    def read_output_hex_data(self):
        # create fileobject using open function call
        with open(self.filepath) as fileobject:
            # create an mmap object using mmap function call
            mmapobject=mmap.mmap(fileobject.fileno(),
                                 length=0,
                                 access=mmap.ACCESS_READ,
                                 offset=0)

            # returns tuples in the format: ((int_num...),(bytes...))
            self.gen_offsets=(self.__genoffsets(self.filepath, self.soreof) 
                              if self.soreof else False )
            # byte indexes are offsets that we want to read
            self.list_offsets=( (lambda ll:[el for lst in ll for el in lst[0]])(self.gen_offsets)  
                                            if self.gen_offsets else False )

            # number of bytes
            len_mapobj=len(mmapobject)
            # row counter
            counter=0

            print(f'\n\033[38;5;82m[HEXADECIMAL DATA "{self.filepath}":]\033[0m\n')
            # read data from mmap object
            try:
                for line in mmapobject:
                    addr=map('{:02x}'.format, line)
                    macAddress = ':'.join(addr).upper()

                    if  self.list_offsets and counter in self.list_offsets:
                        macAddress='\033[48;5;200m'+macAddress+'\033[0m'

                    if  counter%16==0:
                        print('\033[38;5;226m'+format(counter, '08x')+'\033[0m'+'  ', end='')
                    
                    if  ord(line) < 128:
                        line_dec=line.decode('ascii')
                        '''
                        if the string is a: number, letter, space, one of the ascii-punctuations characters.
                        '''
                        if  (line.isdigit() or line.isalpha() 
                            or line==b' '   or line in self.ascii_punct):
                            self.dec.append(line_dec)
                        '''
                        if the string is not a: number, letter, space, one of the ascii-punctuations characters.
                        '''
                        if (not line.isdigit() and not line.isalpha()
                            and not line==b' ' and not line in self.ascii_punct):
                            self.dec.append('.')
                    
                    if  ord(line) >= 128:
                        self.dec.append('.')
                    
                    print('\033[38;5;82m'+macAddress+'\033[0m', end=' ')
                    self.hex_line.append(macAddress)

                    if (counter+1)%16==0:
                        print('  '+'\033[38;5;82m'+''.join(self.dec)+'\033[0m')
                        self.hex_line=[]
                        self.dec=[]

                    counter+=1

                    if  counter==len_mapobj:
                        self.dec='  '+''.join(self.dec)
                        self.dec=' '*(47-len(' '.join(self.hex_line)))+'\033[38;5;82m'+self.dec+'\033[0m'
                        print(self.dec)
                        print('\n')

            except KeyboardInterrupt:
                print('\nStopped')


    def __genoffsets(self, file_hex, source_replace_offsets):
        yield from super().offsets_gen(file_hex, source_replace_offsets)
