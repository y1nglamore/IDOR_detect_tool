import difflib
import json

class Dor:
    def __init__(self, source_resp, modify_resp) -> None:
        self.sr = source_resp
        self.mr = modify_resp

    def __is_json(self, resp) -> bool:
        try:
            json.loads(resp)
            return True
        except Exception:
            return False
    
    def __traverse_json(self, json_obj, l=None) -> list:
        # 遍历json每一个元素
        if l is None:
            l = []
        for key, value in json_obj.items():
            if isinstance(value, dict):
                self.__traverse_json(value, l)
            elif type(value) == str:
                l.append(value)
        return list(set(l))

    def detect_vuln(self) -> bool:
        # Detect vuln here.  
        # 检测逻辑：  1. 判断请求长度 2. 小长度请求只看关键字 3. 大长度请求看关键字&相似度
        src_len = len(self.sr)
        mod_len = len(self.mr)

        if self.__is_json(self.sr) and self.__is_json(self.mr):
            l = self.__traverse_json(json.loads(self.mr))
            if self.__key_words(" ".join(l)):
                return True
            
        return (
            src_len > 100
            and mod_len > 100
            and self.__similarity(self.sr, self.mr) > 0.8
        )
    
    def __key_words(self, resp) -> bool:
        keywords = ['succ', 'success', 'ok', 'true', '成功' , '完成', '查询成功', 'OK', 'SUCC', 'yes', 'YES', 'Yes', 'True', 'TRUE', 'true', '已修改', '已存在' , '已添加' , 'exists', 'already']
        return any(keyword in resp for keyword in keywords)
    
    
    def __similarity(self, str1, str2) -> float:
        return difflib.SequenceMatcher(None, str1, str2).quick_ratio()