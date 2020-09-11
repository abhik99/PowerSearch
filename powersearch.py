import os
import argparse

parser = argparse.ArgumentParser(description='Command line tool for searching the content of multiple files at once')
parser.add_argument('--path', help='Select a path')
parser.add_argument('--keyword', help='Search for a keyword')
parser.add_argument('--encoding', help='Set an encoding (default=utf8)') # TODO
parser.add_argument('--include-dot-dirs', action='store_true', help='Include directories that only have an extension and no name')
parser.add_argument('--include-dot-files', action='store_true', help='Include files that only have an extension and no name')
parser.add_argument('--include-no-ext', action='store_true', help='Include files with no extension')
parser.add_argument('--ignore-file-encoding-errors', action='store_true', help='Ignore file decoding errors') # TODO
args = parser.parse_args()

def getValidFiles(path):
    if path == "" or path == None:
        path = os.getcwd()
    print(f'PATH = {path}')

    std_ignored_exts = ['.cache', '.pyc', 'toc', '.zip', '.pkg', '.pyz']
    
    skipped_dot_dirs = []
    skipped_dot_files = []
    skipped_noext_files = []
    skipped_stdignored_files = []

    files = []
    
    # r=root, d=directories, f=files
    for r, d, f in os.walk(path):

        # check if dir is a dot dir
        for dir in d:
            if dir.startswith(".") and not args.include_dot_dirs:
                skipped_dot_dirs.append(dir)

        # check if dot dir is in a dot dir
        for dir in d:
            if dir.startswith(".") and not args.include_dot_dirs:
                for dir1 in skipped_dot_dirs:
                    if ("\\" + dir1) in r:
                        try:
                            del skipped_dot_dirs[skipped_dot_dirs.index(dir)]
                        except:
                            pass
       
       # check validity of files
        for filename in f:

            # check if file is in a dot dir
            full_file_path = os.path.join(r, filename)
            in_dot_dir = False
            for dir in skipped_dot_dirs:
                if ("\\" + dir + "\\") in full_file_path:
                    in_dot_dir = True
                    break
            if in_dot_dir:
                continue
            
            # check if the file only has an extension and no name
            if filename.startswith(".") and not args.include_dot_files:
                if filename not in skipped_dot_files:
                    skipped_dot_files.append(filename)
                continue
            
            # check if filename doesn't have an extension
            if "." not in filename and not args.include_no_ext:
                if filename not in skipped_noext_files:
                    skipped_noext_files.append(filename)
                continue
            
            # check if filename has a standard ignored extension
            hide_file_status = False
            for ext in std_ignored_exts:
                if filename.endswith(ext):
                    if filename not in skipped_stdignored_files:
                        hide_file_status = True
                        skipped_stdignored_files.append(filename)
                    break
            
            # output filenames that meet all criteria
            if not hide_file_status:
                if full_file_path not in files:
                    files.append(full_file_path)
                
    # output skipped dirs/files stats
    print(f"SKIPPED DOT DIRS = {len(skipped_dot_dirs)} {skipped_dot_dirs}")
    print(f"SKIPPED DOT FILES = {len(skipped_dot_files)} {skipped_dot_files}")
    print(f"SKIPPED NOEXT FILES = {len(skipped_noext_files)} {skipped_noext_files}")
    print(f"SKIPPED STDIGNORED EXTS = {len(skipped_stdignored_files)} {skipped_stdignored_files}")
    print(f"# FILES = {len(files)}")

    for filepath in files:
        print(f"RECEIVED: {filepath}")

    return files


def scanFiles(files):
    if args.keyword == "" or args.keyword == None:
        print("ERROR: keyword argument missing")
        exit()
    else:
        keyword = args.keyword
        print(f'KEYWORD = {keyword}')
    for filepath in files:
        with open(filepath, "r", encoding="utf8", errors="ignore") as file:
            try:
                file_content = file.read()
                num_occurences = file_content.count(keyword)
                if num_occurences > 0:
                    print(f'RESULT: {num_occurences} in {filepath}')
            except Exception as e:
                print("ERROR:", e)
                continue

scanFiles(getValidFiles(args.path))

k = input("Finished. Press enter to exit.")
