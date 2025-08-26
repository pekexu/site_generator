import os
import shutil
from functions import *

def copy_src_to_dst(src, dst):
    if os.path.exists(dst):
        #print(f"deleting {dst}/ and all subdirs")
        shutil.rmtree(dst)
        #if not os.path.exists(dst):
            #print(f"{dst}/ is dead")
    
   # print(f"creating new {dst}/ directory")
    os.mkdir(dst)
    copylist = os.listdir(src)
    for copy in copylist:
        if os.path.isfile(os.path.join(src, copy)):
            #print(f"copying {src}/{copy} to {dst}/{copy}")
            shutil.copy(os.path.join(src,copy),os.path.join(dst,copy))
        else:
            #print(f"recursing into {os.path.join(src,copy)}")
            copy_src_to_dst(os.path.join(src,copy), os.path.join(dst, copy))

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path}, to {dest_path} using {template_path}")
    file = open(from_path)
    md_content = file.read()
    file.close()
    file2 = open(template_path)
    template = file2.read()
    file2.close()
    html_string = markdown_to_html_node(md_content).to_html()
    new_title = extract_title(md_content)
    template = template.replace("{{ Title }}",f"{new_title}" )
    template = template.replace("{{ Content }}",f"{html_string}")
    target = open(os.path.join(dest_path, "index.html"), "x")
    target.write(template)
    target.close()

def generate_pages_recursively(dir_path_content, template_path, dest_dir_path):
    contents = os.listdir(dir_path_content)
    dest_path = dest_dir_path
    if not os.path.exists(dest_path):
        
        os.mkdir(dest_path)
    for content in contents:
        src_path = os.path.join(dir_path_content, content)
        if os.path.isdir(src_path):

            generate_pages_recursively(src_path, template_path, os.path.join(dest_path, content))
        else:

            generate_page(src_path, template_path, dest_dir_path)