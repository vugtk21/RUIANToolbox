# -*- coding: utf-8 -*-
helpStr = """
Builds statistics from vfr2pg.py log file.

Usage: buildstatistics.py [logfilename]
"""

def convertFile(fileName):
    FILE_PREFIX = "Processing "
    FILE_SUFFIX = "..."
    TIME_PREFIX = "Time elapsed: "

    inFile = open(fileName, "r")
    outFileName = fileName[:fileName.rfind(".")] + ".csv"
    outFile = open(outFileName, "w")
    try:
        outFile.write("#,Time [sec],File name\n")
        lineCount = 0
        fileCount = 0
        fileName = ""
        for line in inFile:
            line = line.replace("\n", "")
            line = line.replace("\r", "")
            if line.startswith(FILE_PREFIX) and line.endswith(FILE_SUFFIX):
                fileCount = fileCount + 1
                line = line[len(FILE_PREFIX):]
                fileName = line[:line.find(" ")]
            elif line.startswith(TIME_PREFIX):
                timeSec = line[len(TIME_PREFIX):line.rfind(" ")]
                outFile.write("%d,%s,%s\n" % (fileCount, timeSec, fileName))

            lineCount = lineCount + 1
            pass

        print lineCount, " lines read."
    finally:
        inFile.close()
        outFile.close()

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 1:
        print helpStr
    else:
        convertFile(sys.argv[1])