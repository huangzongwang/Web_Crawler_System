import math
import os
from time import time
import threadpool
import requests
import urllib.parse


class Download:
    """
    多线程流式下载工具类,支持断点下载
    """

    ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    tempDir = "temp"
    saveDir = "download"

    def __init__(
            self,
            url: str,
            fileName: str = None,
            partSize: int = 1024 * 1024 * 10,
            threadNum: int = 3,
            limitTime=10000,
            outputpath:str=None
    ) -> None:
        """
        初始化
        @url：文件链接
        @fileName：文件名(默认从链接中获取)
        @perPartSize：单线程下载大小(默认10MB)
        @threadNum：线程数(默认3)，并不是越多越好，一是设备自身宽带存在上限，二是部分站点会限制IP的连接数
        @limitTime：线程1%进度限制时间(ms,默认10000) ，非正值则不限时，超时则重启该连接(针对部分站点会出现下载越来越慢的情况)
        """
        self.url = url
        self.partSize = partSize
        self.threadNum = threadNum
        self.limitTime = limitTime
        self.outputpath=outputpath
        if not fileName:
            self.fileName = self.__getFileName__()
        else:
            self.fileName = fileName
        self.__markDir__()

    def __getFileName__(self) -> str:
        """
        从链接中获取文件名
        """
        url = urllib.parse.unquote(self.url)
        return url.split("?")[0].split("/")[-1]

    def __markDir__(self) -> None:
        """
        创建缓存和保存目录
        """
        if not os.path.isdir(self.tempDir):
            os.mkdir(self.tempDir)
        if not os.path.isdir(self.saveDir):
            os.mkdir(self.saveDir)

    def __getTotalSize__(self) -> int:
        """
        获取文件总大小
        """
        headers = {
            "Host": "v3-web.douyinvod.com",
            "Connection": "keep-alive",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            "Accept-Encoding": "identity;q=1, *;q=0",
            "Accept": "*/*",
            "Referer": "http://v3-web.douyinvod.com/89b007e566da1f5024881e2501e2de05/6690fa26/video/tos/cn/tos-cn-ve-15c001-alinc2/o0ohHZT8IWMADdMBs2YzNAz9keAfQzmgzWtlEY/?a=6383\u0026ch=11\u0026cr=3\u0026dr=0\u0026lr=all\u0026cd=0%7C0%7C0%7C3\u0026cv=1\u0026br=1982\u0026bt=1982\u0026cs=0\u0026ds=4\u0026ft=pEaFx4hZffPdEK~-Y1qNvAq-antLjrKZRUm.RkabZbx7ejVhWL6\u0026mime_type=video_mp4\u0026qs=0\u0026rc=Ozw8NTNlaDs2ZTRmZzw8N0BpamZ3OWY6Zmk5bjMzNGkzM0BiNl9eNC1fXmMxNDVhMmAtYSNtNC1fcjQwZm1gLS1kLTBzcw%3D%3D\u0026btag=80000e00028000\u0026cquery=100B_100x_100z_100o_101n\u0026dy_q=1720766240\u0026feature_id=46a7bb47b4fd1280f3d3825bf2b29388\u0026l=20240712143720BEF414070764426033F5",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Range": "bytes=0-"
        }
        res = requests.head(url=self.url, headers=headers)
        size = None

        if  "Content-Length" in res.headers:
            print(res.headers["Content-Length"])
            size = int(res.headers["Content-Length"])
            print(f"文件大小: {size / 1024 / 1024} MB")
        else:
            print(f"status_code：{res.status_code}")
        return size

    def __preDownloadPart__(self, index: int, totalSize: int) -> int:
        """
        检查分块下载进度 返回剩余大小
        """
        fileName = f"temp/{self.fileName}_{index}"
        if os.path.isfile(fileName):
            stat = os.stat(fileName)
            return totalSize - stat.st_size  # 剩余大小
        else:
            return totalSize

    def __downloadPart__(self, index: int, rangeStart: int, rangeEnd: int) -> None:
        """
        下载分块
        @index：分块序号
        @start：分块起始位置
        @end：分块结束位置
        """
        indexTip = f"{index + 1}/{self.partNum}"  # 分块位置提示
        totalSize = rangeEnd - rangeStart + 1  # 分块总大小

        restart = True  # 重新下载标志
        while restart:
            needDownSize = self.__preDownloadPart__(index, totalSize)  # 分块剩余大小

            if needDownSize == 0:  # 分块已下载
                print(f"[{indexTip}]已完成")
                return
            if totalSize != needDownSize:  # 分块已存在,追加模式
                file = open(f"temp/{self.fileName}_{index}", mode="ba")
            else:  # 分块未存在，新建模式
                file = open(f"temp/{self.fileName}_{index}", mode="bw")

            currentSize = 0  # 已经下载大小
            progress = 0  # 下载进度


            headers = {
                "Host": "v3-web.douyinvod.com",
                "Connection": "keep-alive",
                "Pragma": "no-cache",
                "Cache-Control": "no-cache",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
                "Accept-Encoding": "identity;q=1, *;q=0",
                "Accept": "*/*",
                "Referer": "http://v3-web.douyinvod.com/89b007e566da1f5024881e2501e2de05/6690fa26/video/tos/cn/tos-cn-ve-15c001-alinc2/o0ohHZT8IWMADdMBs2YzNAz9keAfQzmgzWtlEY/?a=6383\u0026ch=11\u0026cr=3\u0026dr=0\u0026lr=all\u0026cd=0%7C0%7C0%7C3\u0026cv=1\u0026br=1982\u0026bt=1982\u0026cs=0\u0026ds=4\u0026ft=pEaFx4hZffPdEK~-Y1qNvAq-antLjrKZRUm.RkabZbx7ejVhWL6\u0026mime_type=video_mp4\u0026qs=0\u0026rc=Ozw8NTNlaDs2ZTRmZzw8N0BpamZ3OWY6Zmk5bjMzNGkzM0BiNl9eNC1fXmMxNDVhMmAtYSNtNC1fcjQwZm1gLS1kLTBzcw%3D%3D\u0026btag=80000e00028000\u0026cquery=100B_100x_100z_100o_101n\u0026dy_q=1720766240\u0026feature_id=46a7bb47b4fd1280f3d3825bf2b29388\u0026l=20240712143720BEF414070764426033F5",
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Range":f"bytes={rangeEnd - needDownSize + 1}-{rangeEnd}"
            }

            startTime = int(time() * 1000)  # 下载开始时间
            req = requests.get(url=self.url, stream=True, headers=headers)  # 流式下载
            if req.status_code != 206:
                print(f"[{indexTip}][{req.status_code}]服务异常")
                return

            for content in req.iter_content(chunk_size=2048):  # 读取并保存下载数据
                if content:
                    file.write(content)
                    currentSize += 2048  # 更新已下载大小
                    if currentSize < needDownSize:  # 未完成下载
                        newProgress = int(currentSize * 100 / needDownSize)  # 下载进度
                        if progress != newProgress:
                            progress = newProgress
                            divTime = int(time() * 1000) - startTime  # 1%进度花费时间
                            if self.limitTime and divTime > self.limitTime:  # 超时,重新下载
                                print(f"[{divTime}ms][{indexTip}][{progress}%]超时")
                                file.close()
                                break
                            else:
                                startTime = int(time() * 1000)
                                print(f"[{divTime}ms][{indexTip}][{progress}%]下载中")
            restart = False
            print(f"[{indexTip}][{rangeStart}-{rangeEnd}]下载完成")

    def __checkParts__(self, partList: list) -> bool:
        """
        检查全部分块是否已下载
        """
        for part in partList:
            if self.__preDownloadPart__(part["index"], part["totalSize"]) != 0:
                return False
        return True

    def __checkFile__(self) -> bool:
        """
        检查目标文件是否已下载
        """
        return os.path.isfile(self.outputpath)

    def __mergeParts__(self):
        """
        合并分块
        """
        fileName = self.outputpath
        targetFile = open(fileName, mode="bw")
        for index in range(self.partNum):
            partFile = f"temp/{self.fileName}_{index}"
            file = open(partFile, mode="br")
            targetFile.write(file.read())
            file.close()
            print(f"[{partFile}]合并成功")
        targetFile.close()

    def __deleteParts__(self):
        """
        删除缓存分块
        """
        for index in range(self.partNum):
            partName = f"temp/{self.fileName}_{index}"
            if os.path.isfile(partName):
                os.remove(partName)
                print(f"删除[{partName}]成功")

    def start(self):
        """
        开始下载
        """
        totalSize = self.__getTotalSize__()  # 文件总大小
        if not totalSize:
            print("文件不支持断点下载，任务退出")
            return

        self.partNum = math.ceil((totalSize / self.partSize))  # 计算分块数量

        if self.__checkFile__():
            self.__deleteParts__()
            print("文件已下载，任务退出")
            return

        restart = True  # 重新执行标志
        while restart:
            pool = threadpool.ThreadPool(self.threadNum)  # 创建线程池
            partList = []  # 分块列表(包含序号和大小)
            argsList = []  # 任务参数列表

            for i in range(self.partNum):  # 构建参数
                rangeStart = i * self.partSize
                rangeEnd = (
                    (totalSize - 1)
                    if (i + 1 == self.partNum)
                    else ((i + 1) * self.partSize - 1)
                )
                args = ([i, rangeStart, rangeEnd], None)
                argsList.append(args)
                partList.append({"index": i, "totalSize": args[0][2] - args[0][1] + 1})

            reqs = threadpool.makeRequests(self.__downloadPart__, argsList)  # 构建任务队列
            for req in reqs:  # 提交任务
                pool.putRequest(req)
            pool.wait()  # 等待线程结束

            if self.__checkParts__(partList):  # 检查分块状态
                self.__mergeParts__()
                self.__deleteParts__()
                restart = False
                print("下载结束")
            else:
                print("分块未完全下载，请重新执行程序")


if __name__ == "__main__":
    urls = [
       "http://v3-web.douyinvod.com/ef461411c90f761778b745f0056b5228/6691032b/video/tos/cn/tos-cn-ve-15c001-alinc2/os1BBWqGsEAUfKpfj1oWs2Q8xAHKfCPOLIt7G5/?a=6383&ch=11&cr=3&dr=0&lr=all&cd=0%7C0%7C0%7C3&cv=1&br=929&bt=929&cs=0&ds=3&ft=AJkeU_TLRR0sLGC2Nvg2Nc.xBiGNbLagO8sU_4utml89Nv7TGW&mime_type=video_mp4&qs=0&rc=Mzs6Omg4M2g8Omg6PDxlM0Bpanl1eTw6Zm9kcDMzNGkzM0BgLmM0YS00X2AxLjYxLi0yYSNsMHJfcjRfMmpgLS1kLTBzcw%3D%3D&btag=c0000e00028000&cquery=100B_100x_100z_100o_101n&dy_q=1720768674&feature_id=f0150a16a324336cda5d6dd0b69ed299&l=20240712151753E172A327547DEF880E16"
    ]
    for url in urls:
        Download(url, threadNum=2, limitTime=3000).start()