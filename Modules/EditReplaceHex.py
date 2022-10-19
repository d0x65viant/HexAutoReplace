#!/usr/bin/python3
import os
import mmap
from pathlib import PurePath
from Modules.OffSetsGenerator import OffSetsGenerator
from Modules.CheckExistFiles import CheckExistFiles
from Modules.ReadOutputHex import ReadOutputHex
'''
The main class replaces the 
bytes according to the 
arguments passed.
'''
class EditReplaceHex(OffSetsGenerator):
    def __init__(self, source_edit_file=None, source_replace_offsets=None, copy_name_file=None):
        self.file_hex=source_edit_file
        self.surc_off=source_replace_offsets
        self.checkfiles=CheckExistFiles(self.file_hex, self.surc_off)
        self.copy_name_file=copy_name_file
        self.copy_file=None
        # returns tuples in the format: ((int_num...),(bytes...))
        self.gen_offsets=self.__genoffsets(self.file_hex, self.surc_off)
        # returns a dictionary containing the key:value
        # is in the following format: key-int(num), value - byte. 
        # {10: b'byte1', 11: b'byte2', 12: b'byte3', 13: b'byte4'...}
        self.repl_bytes=(lambda ll: {
                        lst[0][ind]:lst[1][ind] for lst in ll for ind in range(len(lst[0])) 
        })(self.gen_offsets)
        
        if  self.checkfiles and not self.gen_non_stop:
            self.edit_replace_hex()


    def edit_replace_hex(self):
        self.__copy_file()
    
        counter=0
        with open(self.copy_file, 'wb') as edit_repl_file:

            with open(self.file_hex) as data_editable:
                mmapobject_read=mmap.mmap(data_editable.fileno(),
                                          length=0,
                                          access=mmap.ACCESS_READ,
                                          offset=0)

                for byte in mmapobject_read:
                    if  counter in self.repl_bytes:
                        byte=self.repl_bytes[counter]
                    edit_repl_file.write(byte)
                    counter+=1


    def __copy_file(self):
        abs_path=os.path.abspath(self.file_hex)
        name_file=PurePath(abs_path).stem
        suffix=PurePath(abs_path).suffix
        self.copy_file=self.copy_name_file if self.copy_name_file else name_file+f"_(repl_hex)"+suffix
        with open(self.copy_file, 'wb') as file:
            file.close()

    def __genoffsets(self, file_hex, source_replace_offsets):
        yield from super().offsets_gen(file_hex, source_replace_offsets)
