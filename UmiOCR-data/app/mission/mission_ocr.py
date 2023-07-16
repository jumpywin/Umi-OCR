# ===============================================
# =============== OCR - 任务管理器 ===============
# ===============================================

"""
一种任务管理器为全局单例，不同标签页要执行同一种任务，要访问对应的任务管理器。
任务管理器中有一个引擎API实例，所有任务均使用该API。
标签页可以向任务管理器提交一组任务队列，其中包含了每一项任务的信息，及总体的参数和回调。

添加任务队列的格式
    mission = {
        "onStart": 任务开始回调函数 ,
        "onGet": 获取一项结果回调函数 ,
        "onFinish": 全部完成回调函数 ,
        "onFailure": 失败退出回调函数 ,
        "argd": api参数字典 ,
        "list": paths,  # 任务队列
    }
    MissionOCR.addMissionList(mission)
"""

from ..api_ocr import getOcrApi
from .mission import Mission
from PySide2.QtCore import QMutex, QThreadPool, QRunnable
import time
from uuid import uuid4  # 唯一ID
import threading  # TODO: 测试


class __MissionOcrClass(Mission):
    def __init__(self):
        super().__init__()
        self.__api = getOcrApi()  # 当前引擎api对象

    # ========================= 【重载】 =========================

    def msnPreTask(self, msnInfo):  # 用于更新api和参数
        # TODO: 检查参数更新
        self.__api.start({"exePath": "lib\PaddleOCR-json\PaddleOCR-json.exe"})
        return True

    def msnTask(self, msnInfo, msn):  # 执行msnInfo中第一个任务
        t1 = time.time()
        res = self.__api.runPath(msn)
        t2 = time.time()
        res["time"] = t2 - t1
        return res


# 全局 OCR任务管理器
MissionOCR = __MissionOcrClass()