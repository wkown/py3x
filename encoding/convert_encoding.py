# coding=utf-8
# pip install chardet
import chardet
import os
import os.path
import glob


def convert(filename, dstEncoding="utf-8"):
    """
    Re-encode text file with auto detec current encode. Need chardet Lib.
Input Parameter:
        filename: full path and file name, e.g. c:/dir1/file.txt
        out_enc: new encode. Default as 'utf-8'
Output Parameter
        None
        """
    try:
        f = open(filename, 'rb')
        content = f.read()
        f.close()
        charsetInfo = chardet.detect(content)
        srcEncoding = charsetInfo['encoding']
        if srcEncoding is None or srcEncoding == dstEncoding:
            return
        new_content = content.decode(srcEncoding, 'ignore')
        f = open(filename, 'wb')
        f.write(new_content.encode(dstEncoding, 'ignore'))
        f.close()
        print("Success: " + filename + " converted from " + srcEncoding + " to " + dstEncoding + " !")
    except IOError:
        print("Error: " + filename + " FAIL to converted from " + srcEncoding + " to " + dstEncoding + " !")


def explore(dir, dstEncoding='utf-8', ext=".txt", IsLoopSubDIR=True):
    '''Convert files encoding.
    Input:
        dir         : Current folder
        IsLoopSubDIR:   True -- Include files in sub folder
                        False-- Only include files in current folder
    Output:
        NONE
    '''
    for parent, dirnames, filenames in os.walk(dir):
        # case 1:
        for dirname in dirnames:
            print("parent folder is:" + parent)
            print("dirname is:" + dirname)
        # case 2
        for filename in filenames:
            filename = os.path.join(parent, filename)
            print("parent folder is:" + parent)
            print("filename with full path:" + filename)
            if ext != "*" and not filename.endswith(ext):
                continue
            convert(filename, dstEncoding)

def main():
    dir = input("Dir:")
    ext = input("ext:")
    dstEncoding = input("dstEncoding:")
    explore(dir,  dstEncoding, ext, True)


if __name__ == "__main__":
    main()