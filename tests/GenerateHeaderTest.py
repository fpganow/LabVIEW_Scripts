import unittest
import patchBitxfile

class GenerateHeaderTest(unittest.TestCase):

    field_1 = [
        0x00, 0x09, 
        0x0f, 0xf0, 0x0f, 0xf0, 0x0f, 0xf0, 0x0f, 0xf0, 0x00
        ]

    field_2 = [
        0x00, 0x01,
        0x61
        ]

    # File name
    field_3 = [
        0x00,  0x69,
        0x50, 0x58, 0x49, 0x65, 0x36, 0x35, 0x39, 0x32, 0x52, 0x5f, 0x54, 0x6f, 0x70, 0x5f, 0x47, 0x65,
        0x6e, 0x32, 0x78, 0x38, 0x3b, 0x45, 0x4e, 0x43, 0x52, 0x59, 0x50, 0x54, 0x3d, 0x4e, 0x4f, 0x3b,
        0x55, 0x73, 0x65, 0x72, 0x49, 0x44, 0x3d, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x3b,
        0x56, 0x65, 0x72, 0x73, 0x69, 0x6f, 0x6e, 0x3d, 0x32, 0x30, 0x31, 0x37, 0x2e, 0x32, 0x2e, 0x31,
        0x5f, 0x41, 0x52, 0x37, 0x31, 0x32, 0x38, 0x39, 0x5f, 0x41, 0x52, 0x37, 0x30, 0x31, 0x37, 0x33,
        0x5f, 0x41, 0x52, 0x37, 0x30, 0x30, 0x36, 0x39, 0x5f, 0x41, 0x52, 0x36, 0x39, 0x36, 0x36, 0x33,
        0x5f, 0x41, 0x52, 0x36, 0x39, 0x34, 0x38, 0x35, 0x00,
        ]

    # Part name
    field_4 = [
        0x62,
        0x00, 0x0d,
        0x37, 0x6b, 0x34, 0x31, 0x30, 0x74, 0x66, 0x66,
        0x67, 0x39, 0x30, 0x30, 0x00
        ]
    # Date
    field_5 = [ 
        0x63,
        0x00, 0x0b,
        0x32, 0x30, 0x31, 0x38, 0x2f, 0x31, 0x32, 0x2f,
        0x32, 0x34, 0x00
        ]
    # Time
    field_6 = [
        0x64,
        0x00, 0x09,
        0x30, 0x38, 0x3a, 0x34, 0x36, 0x3a, 0x30, 0x39, 
        0x00
        ]
    # Device Type
    field_7 = [
        0x65,
        0x00, 0xf2, 0x47, 0x1c
        ]


    def test_field_1_and_2(self):
        # WHEN
        binStream = patchBitxfile.getHeader()

        # THEN
        # Field #1 length
        self.assertEqual(binStream[ 0], 0x00)
        self.assertEqual(binStream[ 1], 0x09)
        # Some sort of header
        self.assertEqual(binStream[ 2], 0x0f)
        self.assertEqual(binStream[ 9], 0xf0)
        self.assertEqual(binStream[10], 0x00)
        # Field #2
        self.assertEqual(binStream[11], 0x00)
        self.assertEqual(binStream[12], 0x01)
        self.assertEqual(binStream[13], 0x61)


    def test_file_name(self):
        # GIVEN
        fileName = "iPXIe6592R_Top_Gen2x8;ENCRYPT=NO;UserID=12345678;Version=2017.2.1_AR71289_AR70173_AR70069_AR69663_AR69485"

        # WHEN
        binStream = patchBitxfile.getHeader(fileName)

        # THEN
        fileNameLen = len(fileName)
        fieldStart = 14
        fieldEnd = fieldStart + fileNameLen + 2

        self.assertEqual(binStream[fieldStart + 0], 0x00)
        self.assertEqual(binStream[fieldStart + 1], fileNameLen)
        self.assertEqual(binStream[fieldStart + 2], ord('i'))
        self.assertEqual(binStream[fieldStart + 3], ord('P'))
        self.assertEqual(binStream[fieldEnd - 3], ord('4'))
        self.assertEqual(binStream[fieldEnd - 2], ord('8'))
        self.assertEqual(binStream[fieldEnd - 1], ord('5'))
        self.assertEqual(binStream[fieldEnd], 0x00)


    def test_short_file_name(self):
        # GIVEN
        fileName = "PXIe6592R_Top_Gen2x8"

        # WHEN
        binStream = patchBitxfile.getHeader(fileName)

        # THEN
        fileNameLen = len(fileName)
        fieldStart = 14
        fieldEnd = fieldStart + fileNameLen + 2

        self.assertEqual(binStream[fieldStart + 0], 0x00)
        self.assertEqual(binStream[fieldStart + 1], fileNameLen)
        self.assertEqual(binStream[fieldStart + 2], ord('P'))
        self.assertEqual(binStream[fieldStart + 3], ord('X'))
        self.assertEqual(binStream[fieldEnd - 3], ord('2'))
        self.assertEqual(binStream[fieldEnd - 2], ord('x'))
        self.assertEqual(binStream[fieldEnd - 1], ord('8'))
        self.assertEqual(binStream[fieldEnd], 0x00)


    def test_part_name(self):
        # GIVEN
        fileName = "PXIe6592R_Top_Gen2x8"
        partName = "7k410tffg900"

        # WHEN
        binStream = patchBitxfile.getHeader(fileName, partName)

        # THEN
        fileNameLen = len(fileName)
        partNameLen = len(partName)
        fieldStart = 14 + fileNameLen + 3
        fieldEnd = fieldStart + partNameLen + 3
        # Part Name Fields
        self.assertEqual(binStream[fieldStart + 0], 0x62)
        self.assertEqual(binStream[fieldStart + 1], 0)
        self.assertEqual(binStream[fieldStart + 2], partNameLen)
        self.assertEqual(binStream[fieldStart + 3], ord('7'))
        self.assertEqual(binStream[fieldEnd - 3], ord('9'))
        self.assertEqual(binStream[fieldEnd - 1], ord('0'))
        self.assertEqual(binStream[fieldEnd - 0], 0x00)


    def test_date(self):
        # GIVEN
        fileName = "PXIe6592R_Top_Gen2x8"
        partName = "7k410tffg900"
        dateString = "2018/12/24"

        # WHEN
        binStream = patchBitxfile.getHeader(fileName, partName, dateString)

        # THEN
        fileNameLen = len(fileName)
        partNameLen = len(partName)
        dateStringLen = len(dateString)
        fieldStart = (14 + fileNameLen + 3) + partNameLen + 4
        fieldEnd = fieldStart + dateStringLen + 3
        # Date String Field Elements
        self.assertEqual(binStream[fieldStart + 0], 0x63)
        self.assertEqual(binStream[fieldStart + 1], 0)
        self.assertEqual(binStream[fieldStart + 2], dateStringLen)
        self.assertEqual(binStream[fieldStart + 3], ord('2'))
        self.assertEqual(binStream[fieldEnd - 3], ord('/'))
        self.assertEqual(binStream[fieldEnd - 2], ord('2'))
        self.assertEqual(binStream[fieldEnd - 1], ord('4'))
        self.assertEqual(binStream[fieldEnd - 0], 0x00)

    def test_time(self):
        # GIVEN
        fileName = "PXIe6592R_Top_Gen2x8"
        partName = "7k410tffg900"
        dateString = "2018/12/24"
        timeString = "08:46:09"

        # WHEN
        binStream = patchBitxfile.getHeader(fileName, partName, dateString, timeString)

        # THEN
        fileNameLen = len(fileName)
        partNameLen = len(partName)
        dateStringLen = len(dateString)
        timeStringLen = len(timeString)
        fieldStart = (14 + fileNameLen + 3) + (partNameLen + 4) + (dateStringLen + 3) + 1
        fieldEnd = fieldStart + timeStringLen + 3
        # Time String Field Elements
        self.assertEqual(binStream[fieldStart + 0], 0x64)
        self.assertEqual(binStream[fieldStart + 1], 0)
        self.assertEqual(binStream[fieldStart + 2], timeStringLen)
        self.assertEqual(binStream[fieldStart + 3], ord('0'))
        self.assertEqual(binStream[fieldEnd - 3], ord(':'))
        self.assertEqual(binStream[fieldEnd - 2], ord('0'))
        self.assertEqual(binStream[fieldEnd - 1], ord('9'))
        self.assertEqual(binStream[fieldEnd - 0], 0x00)

    def test_device_type(self):
        # GIVEN
        fileName = "PXIe6592R_Top_Gen2x8"
        partName = "7k410tffg900"
        dateString = "2018/12/24"
        timeString = "08:46:09"
        deviceType = [0x00, 0xf2, 0x47, 0x1c]

        # WHEN
        binStream = patchBitxfile.getHeader(fileName, partName, dateString, timeString, deviceType)

        # THEN
        fileNameLen = len(fileName)
        partNameLen = len(partName)
        dateStringLen = len(dateString)
        timeStringLen = len(timeString)
        fieldStart = (14 + fileNameLen + 3) + (partNameLen + 4) + (dateStringLen + 3) + (timeStringLen + 3) + 2
        fieldEnd = fieldStart + timeStringLen + 3
        # Device Type Field Elements
        self.assertEqual(binStream[fieldStart + 0], 0x65)
        self.assertEqual(binStream[fieldStart + 1], deviceType[0])
        self.assertEqual(binStream[fieldStart + 2], deviceType[1])
        self.assertEqual(binStream[fieldStart + 3], deviceType[2])
        self.assertEqual(binStream[fieldStart + 4], deviceType[3])


if __name__ == '__main__':
    unittest.main()

