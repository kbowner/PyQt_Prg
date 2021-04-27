import os, mmap

output_dir = "d:\Work\Test_Bin"
txt_input = "test1_uft8_ru.txt"

with open('d:/Work/Test_Bin/test1_uft8_ru.txt', 'r',encoding="utf-8") as f:
    # memory-map the file, size 0 means whole file
    mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
    for b in mm:
        print(b)
    mm.close()

f = open('d:/Work/Test_Bin/test1_uft8_ru.txt', 'rb')
content = f.read()
print (content)