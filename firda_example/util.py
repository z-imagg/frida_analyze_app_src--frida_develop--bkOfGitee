from typing import List


class Util:
    @staticmethod
    def read_text(fpath:str):
        with open(fpath,"r",encoding='utf-8') as f:
            return f.read()
