from datetime import datetime


def generateImageFilepath(file):
    uniqueFileName = str(datetime.now().timestamp()).replace(".", "") # generate unique image name
    fileNameSplit = file.filename.split(".")
    fileExt = fileNameSplit[len(fileNameSplit)-1]
    filePath = f"uploads/{uniqueFileName}.{fileExt}"

    return filePath




