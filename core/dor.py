# import difflib
import json
import Levenshtein


class Dor:
    def __init__(self, source_resp, modify_resp,source_flow = None) -> None:
        self.sr = source_resp
        self.mr = modify_resp
        self.sf = source_flow

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
    
    def __public_api(self) -> bool:
        if not self.sf:
            return False
        
        method = self.sf.request.method
        query = self.sf.request.query

        # 判断为GET请求
        if method != 'GET':
            return False
        # 判断是否有参数
        if not query:
            return True
        
        # 有参数 清空重放
        self.sf.request.query = []
        from .replay import Replay # 避免循环引用
        no_query_paramater_resp = Replay.replay(self.sf)

        # 如果重放后相似，说明是公共接口
        return (
            self.__similarity(self.sr, no_query_paramater_resp) > 0.87
            and self.__similarity(self.mr, no_query_paramater_resp) > 0.87
            and self.__similarity(self.sr, self.mr) > 0.87
        )

    def detect_vuln(self) -> bool:
        # Detect vuln here.  
        # 检测逻辑：  1. 公共接口排除 2. 判断请求长度 3. 小长度请求只看关键字 4. 大长度请求看关键字&相似度
        src_len = len(self.sr)
        mod_len = len(self.mr)

        # 排除公共接口
        if self.__public_api():
            # print(f"[-] 排除公共接口: {self.sf.request.url}")
            return False
        
        # 长度卡点
        if src_len >= 100 and mod_len >= 100:
            return self.__similarity(self.sr, self.mr) > 0.87

        # 长度过短，进行关键字检查
        if self.__is_json(self.mr):
            l = self.__traverse_json(json.loads(self.mr))
            if self.__key_words(" ".join(l)):
                return True
        elif self.__key_words(self.mr):
            return True

    
    def __key_words(self, resp) -> bool:
        keywords = ['success', 'ok', 'true', '成功' , '完成', '查询成功', 'yes', '已修改', '已存在' , '已添加' , 'exists', 'already']
        keywords_copy = keywords[:]# 复制关键词列表
        for word in keywords_copy:
            if word.isalpha():  # 仅处理完全由字母组成的单词
                keywords.extend((word.capitalize(), word.upper())) # 添加英文单词的首字母大写形式和全部大写形式
        return any(keyword in resp for keyword in keywords)
    
    def __similarity(self, str1, str2) -> float:
        # sourcery skip: inline-immediately-returned-variable
        distance = Levenshtein.distance(str1, str2)
        max_length = max(len(str1), len(str2))
        similarity = (max_length - distance) / max_length 
        return similarity
        # return difflib.SequenceMatcher(None, str1, str2).quick_ratio()
        
        