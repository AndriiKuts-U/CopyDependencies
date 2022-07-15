import os
import shutil
from difflib import SequenceMatcher


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def check_occurrence(source_list, destination):
    for i in source_list:
        if i in destination:
            return True


class CopyDependencies:
    def __init__(self, search_path, destination_path, stop_rows=100, print_dependencies=True):
        self.search_path = search_path
        self.destination_path = destination_path
        self.exception_files = ["cmsis_os2.h"]
        self.exception_dirs = [".git", '.vscode', '.idea']
        self.search_formats = ['.h', '.hpp', '.c', '.cpp', '']
        self.paths_dict = {}
        self.all_libs = []
        self.print_dependencies = print_dependencies
        self.stop_rows = stop_rows

    def get_libs(self, filename, prev_path):
        if self.print_dependencies:
            print(filename)

        file = open(filename, "r", encoding="utf-8", errors='ignore')
        current_file_libs = []
        count = 0
        for row in file.readlines():
            words = row.split(" ")

            if count >= self.stop_rows:
                break
            if "#include" in words:
                lib_name = words[words.index("#include") + 1][1:-1]
                if '/' in words[words.index("#include") + 1]:
                    lib_name = words[words.index("#include") + 1].split('/')
                if '<' in lib_name:
                    lib_name = lib_name.replace('<', '')
                if '>' in lib_name:
                    lib_name = lib_name.replace('>', '')

                if lib_name not in self.all_libs:
                    current_file_libs.append(lib_name)
                    self.all_libs.append(lib_name)
                count = 0
            else:
                count += 1

        for lib in current_file_libs:
            for root, _, files in os.walk(self.search_path):
                if check_occurance(self.exception_dirs, root):
                    continue

                if type(lib) is not list:
                    split_lib = lib.split('.')
                    for search_format in self.search_formats:
                        if split_lib[0] + search_format in files and split_lib[0] + search_format not in self.exception_files:
                            if split_lib[0] + search_format not in self.paths_dict.keys():
                                self.paths_dict[split_lib[0] + search_format] = root
                                self.get_libs(os.path.join(root, split_lib[0] + search_format), root)
                            else:
                                if similar(root, prev_path) > similar(self.paths_dict[split_lib[0] + search_format], prev_path):
                                    self.paths_dict[split_lib[0] + search_format] = root
                                    self.get_libs(os.path.join(root, split_lib[0] + search_format), root)
                else:
                    split_lib = lib[-1].split('.')
                    for search_format in self.search_formats:
                        if split_lib[0] + search_format in files and split_lib[0] + search_format not in self.exception_files:
                            new_lib = lib.copy()
                            new_lib[-1] = split_lib[0] + search_format
                            if tuple(new_lib) not in self.paths_dict.keys():
                                self.paths_dict[tuple(new_lib)] = root
                                self.get_libs(os.path.join(root, split_lib[0] + search_format), root)
                            else:
                                if similar(root, prev_path) > similar(self.paths_dict[tuple(new_lib)], prev_path):
                                    self.paths_dict[tuple(new_lib)] = root
                                    self.get_libs(os.path.join(root, split_lib[0] + search_format), root)

    def copy_files(self):

        for lib, root in self.paths_dict.items():
            if type(lib) is tuple:
                lib = list(lib)
                new_root = self.destination_path[:]
                for i in range(len(lib) - 1):
                    if '.' not in lib[i]:
                        if '"' in lib[i]:
                            lib[i] = lib[i].replace('"', '')
                        if '<' in lib[i]:
                            lib[i] = lib[i].replace('<', '')
                        new_root += '\\' + lib[i]
                os.makedirs(os.path.dirname(os.path.join(new_root, lib[-1])), exist_ok=True)
                shutil.copyfile(os.path.join(root, lib[-1]), os.path.join(new_root, lib[-1]))
            else:
                os.makedirs(os.path.dirname(os.path.join(self.destination_path, lib)), exist_ok=True)
                shutil.copyfile(os.path.join(root, lib), os.path.join(self.destination_path, lib))


if __name__ == '__main__':

    copy_cl = CopyDependencies(r"C:\Project1", r"C:\Destination1")
    copy_cl.get_libs(r"C:\Project1\folder1\folder2\source_file.cpp", r"C:\Project1\folder1\folder2")
    copy_cl.copy_files()
