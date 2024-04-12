# 定義 FuzzData 類別
class FuzzData:
    def __init__(self, relativeTime: int, cycleDone: int, corpusCount: int, mapSize: int, savedCrashes: int, maxDepth: int, execsPerSec: int, totalExecs: int, edgesFound: int):
        self.relativeTime = relativeTime
        self.cycleDone = cycleDone
        self.corpusCount = corpusCount
        self.mapSize = mapSize
        self.savedCrashes = savedCrashes
        self.maxDepth = maxDepth
        self.execsPerSec = execsPerSec
        self.totalExecs = totalExecs
        self.edgesFound = edgesFound
    
    