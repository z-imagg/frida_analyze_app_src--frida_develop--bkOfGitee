from typing import List


class Util:
    @staticmethod
    def read_text(fpath:str):
        with open(fpath,"r",encoding='utf-8') as f:
            return f.read()

    @staticmethod
    def cmd_str_to_list(cmd_str:str)->List[str]:
        if cmd_str is None: return None
        lsRaw:List[str]=cmd_str.split(" ")
        ls:List[str]=list(filter(lambda wordK:len(wordK.strip())>0,lsRaw))
        return ls

"""

dork_run_cmd:str="D:/llvm-home/llvm-project/build/Debug/bin/clang.exe -S    -emit-llvm D:/instrmcpp/dork_simple/User.cpp"
cmd_str_to_list(dork_run_cmd)
"""