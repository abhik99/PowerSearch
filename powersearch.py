import os
import argparse

parser = argparse.ArgumentParser(description='Command line tool for searching the content of multiple files at once')
parser.add_argument('--path', help='Select a path')
parser.add_argument('--include-ext-only-dirs', action='store_true', help='Include files that only have an extension')
parser.add_argument('--include-ext-only-files', action='store_true', help='Include files that only have an extension')
parser.add_argument('--include-no-ext', action='store_true', help='Include files with no extension')
args = parser.parse_args()

std_ignored_exts = [".cache"]

def listfiles(path):
    if path == "" or path == None:
        path = os.getcwd()
    print(f'PATH = {args.path}')
    files = []
    num_skipped_extonly_dirs = 0
    num_skipped_extonly_files = 0
    num_skipped_noext_files = 0
    num_skipped_stdignored_files = 0

    skipped_extonly_dirs = []
    skipped_extonly_files = []
    skipped_noext_files = []
    skipped_stdignored_files = []
    
    # r=root, d=directories, f=files
    for r, d, f in os.walk(path):
        # check if the folder is hidden
        for dir in d:
            if not dir.startswith(".") and not args.include_ext_only_dirs:
                for filename in f:
                    hide_file_status = False
                    # check if the file only has an extension and no name
                    if filename.startswith(".") and not args.include_ext_only_files:
                        num_skipped_extonly_files += 1
                        skipped_extonly_files.append(filename)
                        break
                    # check if filename doesn't have an extension
                    if "." not in filename and not args.include_no_ext:
                        num_skipped_noext_files += 1
                        skipped_noext_files.append(filename)
                        break
                    # check if filename has a standard ignored extension
                    for ext in std_ignored_exts:
                        if filename.endswith(ext):
                            hide_file_status = True
                            num_skipped_stdignored_files += 1
                            skipped_stdignored_files.append(filename)
                            break
                    # output filenames that meet all criteria
                    if not hide_file_status:
                        files.append(os.path.join(r, filename))
                        print(filename)
            else:
                num_skipped_extonly_dirs += 1
                skipped_extonly_dirs.append(dir)
    # output skipped dirs/files stats
    print(f"SKIPPED EXTONLY DIRS = {num_skipped_extonly_dirs} {skipped_extonly_dirs}")
    print(f"SKIPPED EXTONLY FILES = {num_skipped_extonly_files} {skipped_extonly_files}")
    print(f"SKIPPED NOEXT FILES = {num_skipped_noext_files} {skipped_noext_files}")
    print(f"SKIPPED STDIGNORED EXTS = {num_skipped_stdignored_files} {skipped_stdignored_files}")
    

listfiles(args.path)

k = input("Finished.") 
