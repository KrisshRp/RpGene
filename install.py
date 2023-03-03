import os, shutil
os.system("pip3 install -r Bin/Requirements/requirements.txt")
os.system("python3 setup.py build")
os.system("cp build/lib.*/Lib/codon/* Lib/codon/")
shutil.rmtree("build")