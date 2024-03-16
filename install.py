import os, shutil
os.system("pip3 install -r Bin/Requirements/requirements.txt")
os.system("python setup.py build")
# os.system("cp ./build/lib.*/Lib/codon/* ./Lib/codon/")
for root, direc, files in os.walk("./build"):
    for file in files:
        path = f"{root}\{file}"
        if path.split(".")[-1] in ["pyd", "py"]:
            shutil.move(path, f"./Lib/codon/{file}")
            print(path)
shutil.rmtree("build")