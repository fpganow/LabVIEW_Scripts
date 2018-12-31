#!/usr/bin/python3.6


def getUpdateMem():
    import os
    updateMem = 'C:\\NIFPGA\\programs\\Vivado2017_2\\bin\\updatemem.bat' if os.name == 'nt' else '/usr/local/natinst/NIFPGA/programs/vivado2017_2/bin/updatemem'
    print(f'Using the following location for updatemem: {updateMem}')
    if not os.path.isfile(updateMem):
        print("updatemem does not exist")
        print('Exiting...')
        import sys
        sys.exit(0)
    return updateMem


def getFile(mypath, expr):
    from os import listdir
    from os.path import isfile, join
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f)) and f.endswith(expr)]
    return onlyfiles[0]


def getOnlyElfFile():
    return getFile('.', '.elf')


def getOnlyBitFile():
    mypath= "."
    from os import listdir
    from os.path import isfile, join
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f)) and f.endswith(".bit")]
    return onlyfiles[0]


# binary file starts with 32 0xFFs
# We can also parse the bitstream header and remove it
def stripBitFileHeader(inBitStream):
    binStartIndex = 0

    for binStartIndex in range(0, len(inBitStream) - 32):
        allEqual = True
        for i in range(binStartIndex, binStartIndex + 31):
            if inBitStream[i] != 0xFF:
                allEqual = False
                break
        if allEqual:
            break
    return inBitStream[binStartIndex:]


def getBinFileFromBitFile(inBitFile):
    print(f'Stripping Bitfile header from {inBitFile}')
    bitStream = readFile(inBitFile)
    outBinFile = inBitFile[:-4] + '.bin'
    fout = open(outBinFile, 'wb')

    bitStream = stripBitFileHeader(bitStream)

    fout.write(bitStream)
    fout.close()
    return outBinFile


def getOnlyBitxFile():
    mypath= "."
    from os import listdir
    from os.path import isfile, join
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f)) and f.endswith(".lvbitx")]
    return onlyfiles[0]


def patch(inElfFile, inBitFile):
    updateMem = getUpdateMem()
    inMmiFile = inBitFile[:-4] + '.mmi'
    outBitFile = inBitFile[:-3] + inElfFile + '.bit'

    print("Updatemem command found")
    print(f'Out bit file: {outBitFile}')
    commandArr = [updateMem,
                  "-data", inElfFile,
                  "-bit", inBitFile,
                  "-proc", "PXIe6592RWindow/theCLIPs/UserRTL_microblaze_CLIP1/d_microblaze_i/microblaze_0",
                  '-meminfo', inMmiFile,
                  "-out", outBitFile
                 ]

    print("Running:")
    print("{}".format( " ".join(commandArr)))

    import subprocess
    proc = subprocess.run(commandArr, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT )
    if proc:
        print(f'proc.returncode = {proc.returncode}')
        print('Results')
        print('-------')
        print("proc.stdout = {}".format(proc.stdout.decode('utf-8')))
    return outBitFile


def replaceBinstream(lvbitx, binFile, outLvbitxFile):
    newBitStream = readFile(binFile)

    import hashlib
    m = hashlib.md5()
    m.update(newBitStream)
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
    tree.write(outLvbitxFile)


def saveToFile(fileName, binData):
    binDataArray = bytearray(binData)
    with open(fileName, "wb") as fout:
        fout.write(binDataArray)


def readFile(fileName):
    byteArray = open(fileName, "rb").read()
    return byteArray


def main():
    print('+-----------------------------------------+')
    print('|  patchBitxfile.py                       |')
    print('|                                         |')
    print('|  Patch lvbitx file with new .elf file   |')
    print('+-----------------------------------------+')
    print('')

    import argparse
    parser = argparse.ArgumentParser(
                      description='Patch .lvbitx file with new .elf file')
    parser.add_argument('--lvbitx', default=None, nargs='?',
                                  help="Full or relative path to LabVIEW lvbitx file")
    parser.add_argument('--bit', default=None, nargs='?',
                                  help="Full or relative path to Vivado bit file")
    parser.add_argument('--elf', default=None, nargs='?',
                                  help="Full or relative path to Xilinx SDK elf file")
    parser.add_argument('--no-confirmation', dest='noConfirmation',
                                  action='store_true',
                                  help="Do not ask for a confirmation before running patch")
    args = parser.parse_args()

    if args.lvbitx:
        lvbitxFile = args.lvbitx
    else:
        print('- No .lvbitx file specified, checking current directory for one')
        lvbitxFile = getOnlyBitxFile()
        if lvbitxFile:
            print(f'  + Found a lvbitx file in the current directory: {lvbitxFile}')
    if args.bit:
        bitFile = args.bit
    else:
        print('- No .bin file speciied, checking current directory for one')
        bitFile = getOnlyBitFile()
        if bitFile:
            print(f'  + Found a bit file in the current directory: {bitFile}')
    if args.elf:
        elfFile = args.elf
    else:
        print('- No .elf file speciied, checking current directory for one')
        elfFile = getOnlyElfFile()
        if elfFile:
            print(f'  + Found an elf file in the current directory: {elfFile}')

    print('')
    if args.noConfirmation:
        response = 'Y'
    else:
        print(f'Patch {lvbitxFile} file with {elfFile} via {bitFile}?')
        response = input('Proceed? (Y/n)')

    if response.upper().strip() != "Y":
        print('Exiting...')
        import sys
        sys.exit(0)
    outLvbitxFile = lvbitxFile[:-6] + '.' + elfFile + '.lvbitx'

    print('')
    print('------------------------------------------')
    print(f'Patch {lvbitxFile} with {elfFile} embedded in to {bitFile}')
    print(f'Temporary lvbitxFile {outLvbitxFile}')

    newBitFile = patch(elfFile, bitFile)
    newBinFile = getBinFileFromBitFile(newBitFile)

    replaceBinstream(lvbitxFile, newBinFile, outLvbitxFile)


if __name__ == '__main__':
    main()
