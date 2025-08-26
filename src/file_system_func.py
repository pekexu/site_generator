import os
import shutil

def copy_static_to_public(src, dst):
    if os.path.exists(dst):
        print(f"deleting {dst}/ and all subdirs")
        shutil.rmtree(dst)
        if not os.path.exists(dst):
            print(f"{dst}/ is dead")
    
    print(f"creating new {dst}/ directory")
    os.mkdir(dst)
    copylist = os.listdir(src)
    for copy in copylist:
        if os.path.isfile(os.path.join(src, copy)):
            print(f"copying {src}/{copy} to {dst}/{copy}")
            shutil.copy(os.path.join(src,copy),os.path.join(dst,copy))
        else:
            print(f"recursing into {os.path.join(src,copy)}")
            copy_static_to_public(os.path.join(src,copy), os.path.join(dst, copy))