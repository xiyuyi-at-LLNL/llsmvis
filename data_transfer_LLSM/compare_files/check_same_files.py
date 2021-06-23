import hashlib
files = ["C:/Users/miao1/Development/data_transfer_LLSM/compare_files/test_data/file_A.txt", 
"C:/Users/miao1/Development/data_transfer_LLSM/compare_files/test_data/file_B.txt"]

digests = []
for filename in files:
    hasher = hashlib.md5()
    with open(filename, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
        a = hasher.hexdigest()
        digests.append(a)
        print(a)

print(digests[0] == digests[1])
