from pathlib import Path
from utilities import FileInfo
from typing import List
import os

CURRENT_DIR = Path.cwd().resolve()

def read_file(file_path):
    with open(file_path, "r") as f:
        return f.read()
def write_file(file_path, content) -> str:
    requested_path = (CURRENT_DIR / file_path).resolve()

    if CURRENT_DIR not in requested_path.parents and requested_path != CURRENT_DIR:
        raise PermissionError("Cannot write outside the current directory.")
    with open(file_path, "w") as f:
        f.write(content)
    print("text has been replaceddd")
    return "file has been written"
def banner_is():
    print("hiikkkking")
    return "Banner is finished"
def friendly_reminder():
    print("Don't forget to take your umbrella out")
def write_multiple_files(file_infos: List[FileInfo]) -> str:
    for info in file_infos:
        with open(info["file_path"], "w") as f:
            f.write(info["content"])
    print("All files has been written")
    return "All files has been written"
def append_file(file_path, content) -> str:
    with open(file_path, "a") as f:
        f.write("\n" + content)
        print("file has been appended")
        return "Append file"
def get_all_files_name_in_dir(dir_path: str) -> list[str]:
    all_files = os.listdir(dir_path)
    return all_files

available_tools = {
    "read_file": read_file,
    "friendly_reminder": friendly_reminder,
    "banner_is": banner_is,
    "write_file": write_file,
    "write_multiple_files": write_multiple_files,
    "append_file": append_file,
    "get_all_files_name_in_dir": get_all_files_name_in_dir
}