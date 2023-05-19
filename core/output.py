import sys 
import os
import shutil
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib.pathutil import path_join
from lib.requestutil import get_raw, resp_htmlencode

class Output():
    def __init__(self, api, src_flow, mod_flow, src_resp, mod_resp, pretty_host) -> None:
        self.api = api 
        self.src_flow = src_flow
        self.mod_flow = mod_flow
        self.src_resp = src_resp
        self.mod_resp = mod_resp
        self.pretty_host = pretty_host
        self.__init_output_file()

    def __init_output_file(self) -> None:
        if not os.path.exists(path_join('report/result.html')):
            shutil.copyfile(path_join('report/report.tpl'), path_join('report/result.html'))
            
    def output(self) -> None:
        crlf = "\n"
        tr = f'''
<tr>
    <td>{self.api}</td>
    <td>length: {len(get_raw(self.src_flow, self.pretty_host))}</td>
    <td>length: {len(self.src_resp)}</td>
    <td>length: {len(get_raw(self.mod_flow, self.pretty_host))}</td>
    <td>length: {len(self.mod_resp)}</td>
</tr>
<tr>
    <td>
        <div class="extra-info">{self.src_flow.request.path}</div>
    </td>
    <td>
        <div class="extra-info">{get_raw(self.src_flow, self.pretty_host).replace(crlf, "<br>")}</div>
    </td>
    <td>
        <div class="extra-info">{resp_htmlencode(self.src_resp)}</div>
    </td>
    <td>
        <div class="extra-info">{get_raw(self.mod_flow, self.pretty_host).replace(crlf, "<br>")}</div>
    </td>
    <td>
        <div class="extra-info">{resp_htmlencode(self.mod_resp)}</div>
    </td>
</tr>
'''
        with open(path_join('report/result.html'), 'r') as f:
            content = f.read()
        with open(path_join('report/result.html'), 'w') as f:
            f.write(content.replace('<!-- TRTRTR -->', f'{tr}<!-- TRTRTR -->'))

            