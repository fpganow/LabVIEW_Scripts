#!/usr/bin/python3.7

def getOnlyBinFile():
    mypath= "."
    from os import listdir
    from os.path import isfile, join
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f)) and f.endswith(".bin")]
    return onlyfiles[0]

def getOnlyBitxFile():
    mypath= "."
    from os import listdir
    from os.path import isfile, join
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f)) and f.endswith(".lvbitx")]
    return onlyfiles[0]

def replaceBitstream(lvbitx, binFile):
    newBitStream = readFile(binFile)

    import hashlib
    m = hashlib.md5()
    m.update(newBitStream)
    calcMd5 = m.digest()
    newMd5_str = m.hexdigest()

    print(f' NEW MD5: {newMd5_str}')

    import base64
    dataHexStr = base64.b64encode(newBitStream).decode('ascii')
    import re
    dataHexStrSplit = re.sub("(.{76})", "\\1\n", dataHexStr, 0, re.DOTALL)

    import xml.etree.ElementTree as ET
    tree = ET.parse(lvbitx)
    root = tree.getroot()
    root.find('BitstreamMD5').text = newMd5_str
    root.find('Bitstream').text = dataHexStrSplit
    tree.write(lvbitx)

def saveToFile(fileName, binData):
    binDataArray = bytearray(binData)
    with open(fileName, "wb") as fout:
        fout.write(binDataArray)

def readFile(fileName):
    byteArray = open(fileName, "rb").read()
    return byteArray

def main():
    print('+----------------------------------------+')
    print('|  patchBitfile.py                       |')
    print('|                                        |')
    print('|  Patch lvbitx file with new .bin file  |')
    print('+----------------------------------------+')
    print('')

    import argparse
    parser = argparse.ArgumentParser(description='Patch .lvbitx file with new .bin file')
    parser.add_argument('lvbitx', default=None, nargs='?',
                                  help="Full path to LabVIEW lvbitx file")
    parser.add_argument('bin', default=None, nargs='?',
                                  help="Full path to Vivado bin file")
    parser.add_argument('--no-confirmation', dest='noConfirmation',
                                  action='store_true',
                                  help="Assume answer is yes")
    args = parser.parse_args()


    if args.lvbitx:
        lvbitx = args.lvbitx
    else:
        print('- No .lvbitx file specified, checking current directory for one')
        lvbitx = getOnlyBitxFile()
        if lvbitx:
            print(f'  + Found a lvbitx file in the current directory: {lvbitx}')
    if args.bin:
        binFile = args.bin
    else:
        print('- No .bin file speciied, checking current directory for one')
        binFile = getOnlyBinFile()
        if binFile:
            print(f'  + Found a bin file in the current directory: {binFile}')

    print('')
    if args.noConfirmation:
        response = 'Y'
    else:
        print(f'Patch {lvbitx} file with {binFile}?')
        response = input('Proceed? (Y/n)')

    if response.upper().strip() != "Y":
        print('Exiting...')
        import sys
        sys.exit(0)

    print('')
    print('------------------------------------------')

    replaceBitstream(lvbitx, binFile)

    # updatemem -data lwip_exercisor2.elf -bit unpacked.bit -proc d_microblaze_i/microblaze -out patched.bit

if __name__ == '__main__':
    main()

