#!/usr/bin/python3.7

import sys

def getOnlyBitxfile():
    mypath= "."
    from os import listdir
    from os.path import isfile, join
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f)) and f.endswith(".lvbitx")]
    if len(onlyfiles) > 0:
        return onlyfiles[0]
    return None

def getBitstream(lvbitxFile):
    import xml.etree.ElementTree as ET
    tree = ET.parse(lvbitxFile)
    root = tree.getroot()

    md5 = root.find('BitstreamMD5').text
    uu64 = root.find('Bitstream').text

    import base64
    data = base64.b64decode(uu64)

    return [md5, data]

def saveToBinFile(fileName, binData):
    binDataArray = bytearray(binData)
    with open(fileName, "wb") as fout:
        fout.write(binDataArray)

def saveToTxtFile(fileName, txtData):
    with open(fileName, "wt") as fout:
        fout.write(txtData)

def main():
    print('+-----------------------------------------+')
    print('|  unpackBinfile.py                       |')
    print('|                                         |')
    print('|  Extract .bin file from LabVIEW lvbitx  |')
    print('|  file with new .bin file                |')
    print('+-----------------------------------------+')
    print('')

    import argparse
    parser = argparse.ArgumentParser(
                  description='Unpack .bin file from LabVIEW lvbitx file')
    parser.add_argument('lvbitx', default=None, nargs='?',
                                  help="Full path to LabVIEW lvbitx file")
    args = parser.parse_args()

    if args.lvbitx:
        print(f'Extracting .bin file from {args.lvbitx}')
        lvbitx = args.lvbitx
    else:
        print('No .lvbitx specified, checking current directory for one')
        lvbitx = getOnlyBitxfile()
        if lvbitx:
            print(f'Found a lvbitx file in the current directory: {lvbitx}')
        else:
            print('No lxbitx file found in current directory, exiting')
            import sys
            sys.exit(0)

        print(f'Bitfile detected: {lvbitx}')
        response = input('Use detected bitfile? (Y/n)')

        if response.upper().strip() != "Y":
            print('Exiting...')
            import sys
            sys.exit(0)

    print(f'Opening bitfile {lvbitx}')

    [md5, bitstream] = getBitstream(lvbitx)
    newFile = lvbitx.split('.lvbitx')[0] + '.bin'

    print(f'Saving .bin file to: {newFile}')
    saveToBinFile(newFile, bitstream)

    md5File = newFile + '.md5'
    print(f'Saving MD5 to file: {md5File}')
    saveToTxtFile(md5File, md5)

if __name__ == '__main__':
    main()

