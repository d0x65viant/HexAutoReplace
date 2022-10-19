# HexAutoReplace
A small script created for personal use.
The purpose of this program is to automatically edit (replace) bytes using a file with offsets and bytes (in hexadecimal form).

### The following parameters are available for passing arguments to the input:
```
optional arguments:
  -h, --help   show this help message and exit
  -hx HX       The file we want to edit in hexadecimal format.
  -of OF       A file with offsets and bytes in hexadecimal format:
               [offsets... - bytes...], where n(offsets)=n(bytes), n is the
               number
  --nm NM      The name or path to the file to which we want to save the
               changes, because it will be safer to change a copy of the
               original.
  --no_output  Do not output the data of the copy of the edited file.

example: autohexrepl.py -hx name_editable_file -of offsets_bytes.txt
```
After autocorrect of the specified bytes, the data will be output in hexadecimal format, 
where the replaced bytes will be highlighted on a purple background:
![hex-data](https://github.com/d0x65viant/Images/blob/main/hex.png)

To cancel the output of the edited copy, you must use the parameter: **--no_output**.


For byte autocorrect, a file with offsets and bytes separated by a hyphen is used, the number of offsets must be equal to the number of bytes:

![offsets-bytes file](https://github.com/d0x65viant/Images/blob/main/offsets.png)

**rand** - means that a random byte will be generated and replaced with the specified one.
