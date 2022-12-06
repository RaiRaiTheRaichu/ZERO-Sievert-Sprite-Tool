import sys
import os
import mmap
import shutil


def gs_unpack(file):
    
    #Create output directory
    if not os.path.exists('output'):
        os.mkdir('output')
    else:
        print("Output folder detected, contents may be overwritten!")
    relativepath = os.path.join(os.getcwd(), 'output\\')

    #Opening file, memory mapping
    gsfile = open(file, "rb+")
    mmfile = mmap.mmap(gsfile.fileno(), 0)

    #Getting texture chunk data
    textureOffset = mmfile.find(b'\x54\x58\x54\x52')
    gsfile.seek(textureOffset + 4)
    textureLength = int.from_bytes(gsfile.read(4), 'little') + 8    #Accounting for the header
    textureFiles = int.from_bytes(gsfile.read(4), 'little')
    
    gsfile.seek(4 * textureFiles, 1) #Skip the initial pointers

    
    #Building list of addresses for each PNG
    texturePointerList = []
    i = 0
    while i < textureFiles:
        gsfile.seek(8, 1)
        texturePointer = gsfile.read(4)
        texturePointerList.append(int.from_bytes(texturePointer, 'little'))
        i += 1

    #Iterating through the list
    currentPNG = 0
    totalWritten = 0

    #Writing out info required to repack the file
    repackInfo = open(relativepath + "repackinfo", "w")
    repackInfo.write(str(textureOffset) + "\n")
    repackInfo.write(str(textureLength) + "\n")
    repackInfo.write(str(textureFiles) + "\n")

    while currentPNG < len(texturePointerList)-1:
        gsfile.seek(texturePointerList[currentPNG], 0)      #Seek to the offset (absolute offset)
        textureSize = texturePointerList[currentPNG+1] - texturePointerList[currentPNG]     #Calculate PNG filesize by deducting offsets

        PNG = gsfile.read(textureSize)
        outputFile = open(relativepath + str(currentPNG) + ".png", "wb+")
        outputFile.write(PNG)   #Write the PNG
        outputFile.close()

        repackInfo.write(str(textureSize) + "\n")

        totalWritten += textureSize     #Tracking texture size written - used to calculate the file size of the final PNG
        currentPNG += 1

    #Handling the final PNG (prevent the index out of bounds when doing `texturePointerList[currentPNG+1]` above)
    lengthOfFinalPNG = (textureLength - 256) - totalWritten
    PNG = gsfile.read(lengthOfFinalPNG)
    outputFile = open(relativepath + str(currentPNG) + ".png", "wb+")
    outputFile.write(PNG)
    outputFile.close()

    repackInfo.write(str(lengthOfFinalPNG))
    repackInfo.close()
    print("PNGs successfully dumped!")

def gs_repack():

    #Backing up old file
    if not os.path.exists("data.backup"):
        shutil.copy("data.win", "data.backup")
    
    #Opening the original file, our output file, and our generated repackinfo
    gsfile = open("data.backup", "rb+")
    outputgsfile = open("data.win", "wb+")
    gssettings = open("output/repackinfo", "r")

    textureOffset = int(gssettings.readline().rstrip())
    textureLength = int(gssettings.readline().rstrip())
    textureFileAmount = int(gssettings.readline().rstrip())

    #Write all of the original file's data until we reach textures
    currentChunk = 0
    while currentChunk < textureOffset:
        outputgsfile.write(gsfile.read(4))
        currentChunk += 4

    #Write all of the pointer data
    while True:
        bytebuffer = gsfile.read(4)
        if bytebuffer != b'\x89\x50\x4E\x47':
            outputgsfile.write(bytebuffer)
        else:
            break

    #Begin iterating through our textures
    i = 0
    while i < textureFileAmount:
        print(f'Adding PNG number: {i}')
        originalSize = int(gssettings.readline().rstrip())
        currentPNG = open("output/" + str(i) + ".png", "rb")
        moddedSize = os.path.getsize("output/" + str(i) + ".png")

        if moddedSize > originalSize:
            print (f'Modded PNG size is too large! Please make sure the PNG is compressed to a smaller file size.')
            return Exception

        paddingLength = 0
        if originalSize > moddedSize:
            paddingLength = originalSize - moddedSize
        
        bytesWritten = 0
        while bytesWritten < moddedSize:
            bytebuffer = currentPNG.read(8)
            outputgsfile.write(bytebuffer)
            bytesWritten += 8

        currentPNG.close()

        outputgsfile.write(bytes(paddingLength))
        i += 1

    #Write the rest of the file
    gsfile.seek(textureLength - 260, 1)
    while True:
        writeBuffer = gsfile.read(4)
        if len(writeBuffer) == 0:
            break
        outputgsfile.write(writeBuffer)
    
    gsfile.close()
    outputgsfile.close()
    print (f'Repacking complete!')
        

    #Main initial function below

if os.path.isdir(sys.argv[1]):
    expectedFiles = ['0.png', '1.png', '10.png', '11.png', '12.png', '2.png', '3.png', '4.png', '5.png', '6.png', '7.png', '8.png', '9.png', 'repackinfo']
    fileList = os.listdir(sys.argv[1])
    if set(expectedFiles).issubset(fileList):
        if os.path.exists("data.win"):
            gs_repack()
        else:
            print(f'Missing data.win! Make sure the file is within the same folder as the program.')
    else:
        print(f'Missing files within the folder!\nMake sure all the following files are inside: {expectedFiles}')


elif os.path.isfile(sys.argv[1]) and os.path.basename(sys.argv[1]) == "data.win":
    print (f'Extracting PNGs from file: {os.path.basename(sys.argv[1])}')
    gs_unpack(sys.argv[1])

else:
    print (f'This is not a valid data.win file!')

print("Press enter to close the program.")
input()