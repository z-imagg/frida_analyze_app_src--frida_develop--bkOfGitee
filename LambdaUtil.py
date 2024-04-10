from typing import List, Any, Set, Tuple, Dict

from Util import Util


class LambdaUtil:
    """
    lambda工具（遍历工具）
    """
    @staticmethod
    def ls2ls(inLs:List[Any], funcOnEleK)->List[Any]:
        """
        列表转列表
        :param inLs: 输入列表
        :param funcOnEleK: 转换函数: 转换 单个输入元素 为 单个输出元素
        :return: 转换后的列表
        """
        outLs:List[Any]=list(map(funcOnEleK, inLs))
        return outLs

    @staticmethod
    def newInstance(cls,*initArgs):
        """
        构造函数: 构造指定类cls的实例
        :param cls: 指定类
        :param initArgs: 构造函数的参数
        :return: 返回实例
        """
        # cls:LineText
        # LineText.__init__(LineText.__new__(LineText),None,1,None)
        thiz=cls.__new__(cls)
        cls.__init__(thiz, *initArgs)
        return thiz

    @staticmethod
    def ls2lsFxParmSDelNulElem(inLs:List[Any], funcOnEleK, *fixedParamLs)->List[Any]:
        """
        列表转列表, 带固定参数列表, 转完后 丢弃空元素
        :param inLs: 输入列表
        :param funcOnEleK: 转换函数: 转换 单个输入元素 为 单个输出元素
        :param fixedParamLs: 提供给转换函数的 固定参数列表
        :return:
        """
        outLs:List[Any]=LambdaUtil.ls2lsFxParmS(inLs, funcOnEleK, *fixedParamLs)
        outLs=LambdaUtil.ls2lsDelNulEle(outLs)
        return outLs

    @staticmethod
    def ls2lsFxParmSDelIfEleIsEmptyLs(inLs:List[Any], funcOnEleK, *fixedParamLs)->List[Any]:
        """
        列表转列表, 带固定参数, 转完后 若元素为数组且为空数组 则删除该元素
        :param inLs:
        :param funcOnEleK:
        :param fixedParamLs:
        :return:
        """
        outLs:List[Any]=LambdaUtil.ls2lsFxParmS(inLs, funcOnEleK, *fixedParamLs)
        outLs = LambdaUtil.lsFilter(outLs, lambda eleK: not Util.lsIsEmpty( eleK))
        return outLs
    @staticmethod
    def ls2lsFxParmS(inLs:List[Any], funcOnEleK, *fixedParamLs)->List[Any]:
        """
        列表转列表, 带固定参数
        :param inLs: 输入列表
        :param funcOnEleK: 转换函数: 转换 单个输入元素 为 单个输出元素
        :param fixedParamLs: 提供给转换函数的 固定参数列表
        :return: 转换后的列表
        """
        if Util.lsIsEmpty(inLs):
            return None
        #cls:LineText
        # LineText.__init__(LineText.__new__(LineText),None,1,None)
        outLs:List[Any]=[
            funcOnEleK(eleK, *fixedParamLs) if len(fixedParamLs) > 0 else funcOnEleK(eleK)
            for k,eleK in enumerate(inLs)
        ]
        return outLs

    @staticmethod
    def groupBy(inLs:List[Any], nameFunc)->Dict[str,List[Any]]:
        if Util.lsIsEmpty(inLs):
            return None

        grpByDict:Dict[str,List[Any]]={}
        for k, eleK in enumerate(inLs):
            nameValue:str=nameFunc(eleK)
            if not grpByDict.__contains__(nameValue):
                grpByDict.__setitem__(nameValue,[])
            grpByDict.__getitem__(nameValue).append(eleK)
        return grpByDict
    #从指定下标开始 连续满足给定条件 的子列表
    def subLs_continuousSatisfy_fixedParamLs(inLs:List[Any],startIdxIncluded:int,endIdxExcluded:int,funcWithIndex,*fixedParamLs)->List[Any]:
        if Util.lsIsEmpty(inLs):
            return None

        # previousSatisfy:bool=None
        currentSatisfy:bool=False
        absK:int=-1
        for k, eleK in enumerate(inLs[startIdxIncluded:endIdxExcluded]):
            absK=k+startIdxIncluded
            currentSatisfy=funcWithIndex(absK,eleK,*fixedParamLs) if len(fixedParamLs)>0 \
                else funcWithIndex(absK,eleK)
            ###
            if currentSatisfy is None or not currentSatisfy:
                break
            # if previousSatisfy is None:
            #     previousSatisfy=currentSatisfy
            #     continue

        return (inLs[startIdxIncluded:absK],absK)


    @staticmethod
    def ls2lsFxParmSEleIdx(inLs:List[Any], funcOnKEleK, *fixedParamLs)->List[Any]:
        """
        列表转列表, 带固定参数, 转换函数能看到元素下标
        :param inLs: 输入列表
        :param funcOnKEleK: 函数: 转换<元素下标,单个输入元素> 为 单个输出元素
        :param fixedParamLs: 提供给转换函数的 固定参数列表
        :return:
        """
        if Util.lsIsEmpty(inLs):
            return None
        #cls:LineText
        # LineText.__init__(LineText.__new__(LineText),None,1,None)
        outLs:List[Any]=[
            funcOnKEleK(k, eleK, *fixedParamLs) if len(fixedParamLs) > 0 else funcOnKEleK(k, eleK)
            for k,eleK in enumerate(inLs)
        ]
        return outLs
    @staticmethod
    def ls2lsNewInst(inLs:List[Any], cls, *fixedParamLs)->List[Any]:
        """
        列表转列表，带固定参数，单元素转换函数 为 指定类cls的构造函数
        :param inLs: 输入列表
        :param cls: 指定类
        :param fixedParamLs: 带固定参数
        :return: 返回构造好的实列列表
        """
        #cls:LineText
        # LineText.__init__(LineText.__new__(LineText),None,1,None)
        outLs:List[Any]=[
            LambdaUtil.newInstance(cls,eleK,k,*fixedParamLs)
            for k,eleK in enumerate(inLs)#,start=1
        ]
        return outLs

    @staticmethod
    def ls2lsDelNulEle(inLs:List[Any])->List[Any]:
        """
        列表转列表, 删除列表中的空元素
        :param inLs: 输入列表
        :return: 删掉空元素后的列表
        """
        return LambdaUtil.lsFilter(inLs,lambda eleK:eleK is not None)

    @staticmethod
    def lsFilter(inLs:List[Any], funcOnEleK, *fixedParamLs)->List[Any]:
        """
        列表过滤
        :param inLs: 输入列表
        :param funcOnEleK: 转换函数: 转换 单个输入元素 为 单个输出元素
        :param fixedParamLs: 提供给转换函数的 固定参数列表
        :return:
        """
        outLs:List[Any]=list(filter(
            lambda eleK:funcOnEleK(eleK, *fixedParamLs) if len(fixedParamLs) > 0
                else funcOnEleK(eleK),
            inLs))
        return outLs


    @staticmethod
    def lsAllTrue(inLs:List[Any], funcOnEleK, *fixedParamLs)->bool:
        """
        对该输入列表应用该函数, 是否每个元素都返回True
        :param inLs: 输入列表
        :param funcOnEleK: 转换函数: 转换 单个输入元素 为 bool
        :param fixedParamLs: 提供给转换函数的 固定参数列表
        :return: 单bool值
        """
        ls_bool:List[bool]=list(map(
            lambda eleK:funcOnEleK(eleK, *fixedParamLs) if len(fixedParamLs) > 0
                else funcOnEleK(eleK),
            inLs))
        allTrue=all(ls_bool)
        return allTrue

    @staticmethod
    def lsDeduplicate(inLs:List[Any], funcOnEleK, *fixedParamLs)->List[Any]:
        """存虑: 相当于 groupBy后取每组的第0个元素?
        列表转列表,去重
            转换函数将单输入元素转换为key, 该单输入元素作为value, 以此<key:value>对构造字典, 返回该字典的valueLs
        :param inLs: 输入列表
        :param funcOnEleK: 转换函数: 转换 单个输入元素 为 key
        :param fixedParamLs: 提供给转换函数的 固定参数列表
        :return:
        """
        dct:Dict=dict([
            (funcOnEleK(eleK, *fixedParamLs) if len(fixedParamLs) > 0
                else funcOnEleK(eleK),
             eleK)
            for k,eleK in enumerate(inLs)
        ])
        return list(dct.values())
    @staticmethod
    def lsFilterKEleK(inLs:List[Any], funcOnEleK)->List[Tuple[int, Any]]:
        """
        列表过滤, 返回符合要求的<元素下标,元素>列表
        :param inLs: 输入列表
        :param funcOnEleK: 转换函数: 转换 单个输入元素 为 bool
        :return:符合要求的<元素下标,元素>列表
        """
        ls_fit_k_eleK:List[Tuple[bool,int,Any]]=[
            (funcOnEleK(eleK), k, eleK)
            for k,eleK in enumerate(inLs)
        ]
        ls_fitTrue_k_eleK:List[Tuple[bool,int,Any]]=list(filter(lambda t:t[0],ls_fit_k_eleK))
        trueLs_k_eleK:List[Tuple[int,Any]]=list(map(lambda t:(t[1:-1]), ls_fitTrue_k_eleK))
        return trueLs_k_eleK

    @staticmethod
    def getField(inLs:List[Any],fieldName)->List[Any]:
        """
        列表转列表, 取元素的指定字段
        :param inLs: 输入列表
        :param fieldName: 指定字段名
        :return: 指定字段值列表
        """
        outLs:Set[Any]=set(map(lambda eleK:getattr(eleK,fieldName),inLs))
        return list(outLs)