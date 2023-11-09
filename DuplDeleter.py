import hashlib
import glob
import os

def calculate_hash(FolderPath, algorithm='sha256'):
    # open file in rb mode
    with open(FolderPath, 'rb') as file:
        #init hasing object for algorithm
        hash_object = hashlib.new(algorithm)
        #read the file block by block
        while True:
            block = file.read(4096)
            if not block:
                break
            hash_object.update(block)
    HashValue = hash_object.hexdigest()
    return HashValue

def ArrayFiller(FolderPath):
    HashWebmResultArray = []
    Hashmp4ResultArray = []

    WebmFiles = glob.glob(FolderPath + '/*.webm')
    for FilePath in WebmFiles:
        ResultHashWebm = calculate_hash(FilePath)
        FileName = os.path.basename(FilePath)
        HashWebmResultArray.append((FileName, ResultHashWebm))
    mp4Files = glob.glob(FolderPath + '/*.mp4')
    for FilePath in mp4Files:
        ResultHashmp4 = calculate_hash(FilePath)
        FileName = os.path.basename(FilePath)
        Hashmp4ResultArray.append((FileName, ResultHashmp4))
    return HashWebmResultArray, Hashmp4ResultArray

def MatchHashChecker(HashsumArray):
    HashDict = {}
    duplicates = []

    for filename, hashsum in HashsumArray:
        if hashsum in HashDict:
            HashDict[hashsum].append(filename)
        else:
            HashDict[hashsum] = [filename]

    for hashsum, filenames in HashDict.items():
        if len(filenames) > 1:
            duplicates.append((hashsum, filenames))
    return duplicates

# Пример использования
FolderPath = "/home/username/Videos/truewebm/"
HashWebmResultArray, Hashmp4ResultArray = ArrayFiller(FolderPath)
DuplicateHashWebm = MatchHashChecker(HashWebmResultArray)
DuplicateHashmp4 = MatchHashChecker(Hashmp4ResultArray)

if DuplicateHashWebm or DuplicateHashmp4:
    Checker = True
    DeleteList = []
    if DuplicateHashmp4:
        Checker = False
        print("duplicates for mp4 found: ")
        for hash, FoundDupls in DuplicateHashmp4:
            print("\tfor hash sum", hash, "of file", FoundDupls[0], "found a clone -", ", ".join(FoundDupls[1:]))
            DeleteList.append(FoundDupls[1:])
    else:
        print("duplicates for mp4 not found")
    if DuplicateHashWebm:
        print("duplicates for Webm found: ")
        for hash, FoundDupls in DuplicateHashWebm:
            print("\tfor hash sum", hash, "of file", FoundDupls[0], "found a clone -", ", ".join(FoundDupls[1:]))
            if Checker == True:
                DeleteList.append(FoundDupls[1:])
    else:
        print("duplicates for webm not found")

    DeleteQuestion = input("\nDo you want to REMOVE duplicates? Yes/No: ").lower()
    if DeleteQuestion == "y" or DeleteQuestion == "yes":
        DeleteList1d = sum(DeleteList, [])
        for item in DeleteList1d:
            try:
                os.remove(FolderPath + item)
                print(f"File {FolderPath + item} successfully deleted.")
            except OSError as e:
                print(f"Error deleting file: {e}")
    elif DeleteQuestion != "n" and DeleteQuestion != "no":
        print("Incorrect input")
