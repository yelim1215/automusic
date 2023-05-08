import os
import shutil
with open(r"C:\Users\zing1\workspace\automusic_model\data_process\dataset\chord_0506.txt", "r") as f:
    for line in f:
        fold, idx = map(int, line.strip().split())
        org = r"C:\Users\zing1\workspace\automusic_model\data_process\POP909\{0:03d}".format(fold)
        if (idx >= 0 and idx <= 2):
            #print(idx)
            dest = r"C:\Users\zing1\workspace\automusic_model\data_process\dataset\0\{0:03d}".format(fold)
            shutil.copytree(org, dest)
        elif (idx >= 3 and idx <= 5):
            #print(idx)
            dest = r"C:\Users\zing1\workspace\automusic_model\data_process\dataset\1\{0:03d}".format(fold)
            shutil.copytree(org, dest)
        elif (idx >= 6 and idx <= 8):
            #print(idx)
            dest = r"C:\Users\zing1\workspace\automusic_model\data_process\dataset\2\{0:03d}".format(fold) 
            shutil.copytree(org, dest)
        elif (idx >= 9 and idx <= 11):
            #print(idx)
            dest = r"C:\Users\zing1\workspace\automusic_model\data_process\dataset\3\{0:03d}".format(fold) 
            shutil.copytree(org, dest)
