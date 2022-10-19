import argparse
from Modules.EditReplaceHex import EditReplaceHex
from Modules.ReadOutputHex  import ReadOutputHex
from sys import platform        

example_text=("example: "
              "\n autohexrepl -hx name_editable_file"
              " -of name_file_offsets.txt")


def arg_parser():
    parser = argparse.ArgumentParser(usage=f"autohexrepl -h", epilog=example_text, description='An automated hex editor designed to replace bytes.')
    parser.add_argument('-hx',    type=str, required=True, help='The file we want to edit in hexadecimal format.')
    parser.add_argument('-of',    type=str, required=True, help='A file with offsets and bytes in hexadecimal format: [offsets... - bytes...], where n(offsets)=n(bytes), n is the number')
    parser.add_argument('--nm',   type=str, help="The name or path to the file to which we want to save the changes, because it will be safer to change a copy of the original." )
    parser.add_argument('--no_output',action='store_true', help='Do not output the data of the copy of the edited file.')
    args = parser.parse_args()
    return args

def main():
    if  platform == "win32":
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    
    args = arg_parser()
    # editable file
    hex_file=args.hx
    # file with offsets and bytes in hexadecimal format
    offst_file=args.of
    '''the name of the file that 
    will be a copy of the original'''
    name_file=args.nm
    '''if this argument is specified, 
    then the output is disabled'''
    no_output=args.no_output
    '''the main object, uses the EditReplaceHex class'''
    edrepl_obj=EditReplaceHex(hex_file, offst_file)

    if not no_output:
        ReadOutputHex(edrepl_obj.copy_file, offst_file)

if __name__=="__main__":
    main()


