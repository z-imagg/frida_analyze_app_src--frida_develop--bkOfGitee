from typing import List, Any


class Util:
    """
    工具
    """
    @staticmethod
    def listLength(ls:List[Any],default:int=0):
        """
        取该数组长度, 若该数组为None 返回该默认长度
        :param ls: 该数组
        :param default: 该默认长度
        :return:
        """
        if ls is None:
            return default
        return len(ls)

    @staticmethod
    def lsIsNotEmpty(ls:List[Any])->bool:
        """
        该数组非空？
        :param ls:
        :return:
        """
        return not Util.lsIsEmpty(ls)

    @staticmethod
    def lsIsEmpty(ls:List[Any])->bool:
        """
        该数组空？
        :param ls:
        :return:
        """
        return \
            ls is None \
            or (isinstance(ls,(list,tuple,set))
                and len(ls)==0 )