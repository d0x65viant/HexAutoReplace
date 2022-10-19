#!/usr/bin/python3
import os

class CheckExistFiles:
    def __new__(cls, filehex, sourceoffsets):
        file_hex=filehex
        surc_off=sourceoffsets

        ERRORS={not file_hex:"ERROR: The original, editable file  is not specified!",
                not surc_off:"ERROR: The config-file with offsets is not specified!",
                not os.path.exists(file_hex):"ERROR: The editable file that you specified does not exist!",
                not os.path.exists(surc_off):"ERROR: The specified file with offsets does not exist!",
                os.path.isdir(file_hex):"ERROR: The specified hexadecimal file must not be a directory!",
                os.path.isdir(surc_off):"ERROR: The specified file with offsets must not be a directory"}

        for err in ERRORS:
            if err:
                print(ERRORS[err])
                return False
            
        return True
