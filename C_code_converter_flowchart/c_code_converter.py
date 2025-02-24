import wx
import re
from graphviz import Digraph
import os
import subprocess
import copy
from dataclasses import dataclass

blue = "#DAE8FC"
red = "#F8CECC"
green = "#75FB94"

def parse_c_comments(c_code):
    lines = c_code.splitlines()

    #if 0 and #ifdef 처리
    if_exclude_code = ['#if 0', '#ifdef WIRECAR']
    if_exclude_code2 = ['#if 1', 'endif']
    if_flag = False

    # comments flag
    comments_flag = False

    # Temp preprocessing line
    preprocessing_lines = []
    temp_line = ""

    for line in lines:
        # 한줄 주석 제거
        line = re.sub(r'//.*', '', line)
        line = re.sub(r'/\*.*?\*/', '', line, flags=re.DOTALL)
        
        # and or
        line = line.replace("&&", "and").replace("||", "or")
        line = line.strip()
        
        
        # #ifdef 0 처리
        if any(e in line for e in if_exclude_code):
            if_flag = True
            continue

        elif any(e in line for e in if_exclude_code2):
            continue
        
        
        if if_flag == True:
            if line == "#endif":
                if_flag = False
            continue

        # 여러 줄 주석 처리
        if '/*' in line:
            comments_flag = True
            continue
        
        if comments_flag:
            if '*/' in line:
                comments_flag = False
            continue


        if not line.startswith("return"):

            # # 변수 선언문 (초기화하지 않은 선언문은 건너뛰기)
            if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*\s+[a-zA-Z_][a-zA-Z0-9_]*\s*;', line):
                continue
            
            # 초기화된 변수 선언문 처리 (자료형 제외, 변수명과 초기값만 포함)
            # elif re.match(r'([a-zA-Z_][a-zA-Z0-9_]*\s+[a-zA-Z_][a-zA-Z0-9_]*\s*=\s*.*);', line):
            #     print(line)
            #     continue


        if line.strip():
            preprocessing_lines.append(line.strip())

    
    
    ###################################################################
    
    statements = []
    temp_line = ""
    for line in preprocessing_lines:
        line = line.strip()
            
        if line:
            temp_line += " " + line
            
        if line.endswith((';')):
            statements.append(temp_line.strip())
            temp_line = ""

        #  스위치 문을 구분하기 위한 : 구분
        if line.endswith((":")):
            statements.append(temp_line.strip())
            temp_line = ""

        
        temp_lines = re.split(r'([{}])', temp_line)
        if(len(temp_lines) > 1):
            for tmp in temp_lines:
                if(tmp == ''): continue
                statements.append(tmp.strip())
                temp_line = ""

    # 마지막 문장이 남은 경우 처리
    if temp_line:
        statements.append(temp_line.strip())

    for i in statements:
        print(i)

    return statements

def convert_c_function(c_code):
    # 간단한 파싱 (if/else, else if, for, printf, 일반문 처리)
    graph = Digraph(format='png')
    graph.attr(
        rankdir='TB',
        dpi='1000',
        # splines='true',
        size='5,5',
        nodesep='0.6',
        ranksep='0.3',
        fontsize='12'
    )  # 해상도 및 크기 조정

    prev_node = None
    exclude_code = ['{', '}']

    # 헤드 노드
    head_node = None
    function_name = ""
    
    label_comment = ""

    FOR_DIVIDE_POINT = []
    IF_DIVIDE_POINT = []
    IF_END_POINT = []

    while_flag = False
    while_node_id = None

    # 스위치 처리
    switch_flag = -1
    SWITCH_NODE_ID = 0
    switch_value = ""

    bracket_lvl = 0
    max_bracket_lvl = 0
    
    for line_num, line in enumerate(c_code,start=1):

        line = line.replace("&&", "and").replace("||", "or")

        if any(e in line for e in exclude_code):
            if '{' in line:                 
                bracket_lvl += 1
                if max_bracket_lvl < bracket_lvl:   
                    max_bracket_lvl = bracket_lvl
            elif '}' in line:
                bracket_lvl -= 1

                if len(IF_DIVIDE_POINT) > 0 and IF_DIVIDE_POINT[-1][1] == bracket_lvl:
                    prev_nove, lvl = IF_DIVIDE_POINT.pop()
                
                # For문 종료 처리
                if len(FOR_DIVIDE_POINT) > 0 and FOR_DIVIDE_POINT[-1][1] == bracket_lvl:
                    for_condition_id, lvl, for_end_id = FOR_DIVIDE_POINT.pop()

                    graph.edge(prev_node, for_end_id)
                    prev_node = for_condition_id
                    
                    label_comment="False"

                # 스위치문 종료 처리
                    
                if switch_flag == bracket_lvl:
                    #스위치문 빠져나옴
                    prev_node = SWITCH_NODE_ID
                    switch_flag = -1
           
            continue
        # 첫 노드인 함수 이름 생성
        if line_num == 1:
            head_node = f'{line_num}_line_{line}'
            head_node_id = line.strip()
            function_name = re.search(r'\b(?:\w+\s*\([^)]*\)\s*)?(\w+)\s*\(', line).group(1)
            
            # 노드 생성 및 연결
            graph.node(head_node, f'{line}', shape='box',style='filled', fillcolor=green)
            prev_node = head_node
            continue

        # IF 조건문 처리
        elif line.startswith("if"):
            if_condition = re.search(r'\((.*)\)', line).group(1)
            if_node_id = f'{line_num}_if_{if_condition}'

            # IF문 노드 생성
            graph.node(if_node_id, f"{if_condition}", shape='diamond',style='filled', fillcolor=red)
                
            # 이전 IF문 분기점 삭제
            # prev_if_node = None
            # while len(IF_DIVIDE_POINT) > 0 and IF_DIVIDE_POINT[-1][1] >= bracket_lvl:
            #     prev_if_node, lvl = IF_DIVIDE_POINT.pop()

            # IF문 분기점 생성
            IF_DIVIDE_POINT.append([if_node_id, bracket_lvl])

            # 이전 분기점 and 이전 노드와 연결
            # if prev_if_node: graph.edge(prev_if_node, if_node_id, label="False")
            graph.edge(prev_node, if_node_id)

            # 이전 노드 갱신
            prev_node = if_node_id

            # 다음 노드의 코멘트를 TRUE로 변경
            label_comment = "True"

        # ELSE IF 조건문 처리
        elif line.startswith("else if"):
            else_if_conditon = re.search(r'\((.*)\)', line).group(1)
            else_if_node_id = f'{line_num}_else_if_{else_if_conditon}'
            
            # ELSE IF문 노드 생성
            graph.node(else_if_node_id, f"{else_if_conditon}", shape='diamond',style='filled', fillcolor=red)


            # 이전 노드와 연결 코멘트는 False
            if if_prev_node, tmp = IF_DIVIDE_POINT.pop()
            graph.edge(if_prev_node, else_if_node_id, label="False")
            
            # IF문 분기점 갱신
            IF_DIVIDE_POINT.append([else_if_node_id, bracket_lvl])

            # 이전 노드 갱신
            prev_node = else_if_node_id

            # 다음 노드의 코멘트를 TRUE로 변경
            label_comment = "True"           
        
        # ELSE 조건문 처리
        elif line.startswith("else"):
            # 노드 생성
            else_node_id = f'{line_num}_else'

            # ELSE문 노드 생성
            graph.node(else_node_id, f'else', shape='diamond',style='filled', fillcolor=red)

            # 이전 노드와 연결 코멘트는 False
            if_prev_node, tmp = IF_DIVIDE_POINT.pop()
            graph.edge(if_prev_node, else_node_id, label="False")
            
            # ELSE IF or ELSE문 분기점 갱신
            IF_DIVIDE_POINT.append([else_node_id, bracket_lvl])

            # 다음 노드의 코멘트를 TRUE로 변경
            label_comment = "True"
            
            # 이전 노드 갱신
            prev_node = else_node_id
        # 반환값
        elif line.startswith("return"):
            node_id = f'{line_num}_line_{line}'
            graph.node(node_id, line, shape='box',style='filled', fillcolor=red)
        
            # 이전 IF문 분기점 삭제
            prev_if_node = None
            while len(IF_DIVIDE_POINT) > 0 and IF_DIVIDE_POINT[-1][1] >= bracket_lvl:
                prev_if_node, lvl = IF_DIVIDE_POINT.pop()
            
            
            if prev_if_node: graph.edge(prev_if_node, node_id, label="False")
            graph.edge(prev_node, node_id, label=label_comment)

            label_comment = ""
            prev_node = node_id 

        # elif len(IF_DIVIDE_POINT) > 0 and IF_DIVIDE_POINT[-1][1] == bracket_lvl - 1:
             
        if line.startswith("switch"):
            switch_condition = re.search(r'switch\s*\((.*?)\)', line).group(1)
            switch_parsing_name = switch_condition.strip()
            
            switch_node_id = f'{line_num}_switch_{switch_parsing_name}'
            switch_value = switch_parsing_name

            #현재 스위치 문 저장
            switch_flag = bracket_lvl
            SWITCH_NODE_ID = switch_node_id

            # 이전 IF문 분기점 삭제
            prev_if_node = None
            while len(IF_DIVIDE_POINT) > 0 and IF_DIVIDE_POINT[-1][1] == bracket_lvl:
                prev_if_node, lvl = IF_DIVIDE_POINT.pop()

            #노드 생성
            graph.node(switch_node_id,f'switch({switch_parsing_name})', shape='box',style='filled', fillcolor=blue)

            if prev_if_node: graph.edge(prev_if_node, switch_node_id, label="False")
            graph.edge(prev_node,switch_node_id)
            prev_node = switch_node_id
   
        elif switch_flag and (line.startswith("case") or line.startswith("default")):
            if "case" in line: case_condition =  re.search(r'case\s+(\w+):', line).group(1) 
            else: case_condition = "defualt"

            node_id = f'{line_num}_switch_case_{case_condition}'

            #이전 노드 변경
            prev_node = SWITCH_NODE_ID
            
            #노드 생성
            graph.node(node_id, f'{switch_value} == {case_condition}', shape="diamond", style='filled', fillcolor=red)
            graph.edge(prev_node, node_id)

            prev_node = node_id
            head_node_id = node_id

        elif switch_flag and line.startswith("break"):
            # 모든 if, for문 정리
            IF_DIVIDE_POINT = []
            continue
        

        # WHILE
        elif line.startswith("while"):
            loop_condition = re.search(r'while\((.*)\)', line).group(1)

            while_condition_id = f'{line_num}_while_{loop_condition}'
            while_head_id = f'{line_num}_while'

            # 현재 반복문 저장
            while_flag = bracket_lvl
            while_node_id = while_condition_id
            
            # 이전 IF문 분기점 삭제
            prev_if_node = None
            while len(IF_DIVIDE_POINT) > 0 and IF_DIVIDE_POINT[-1][1] == bracket_lvl:
                prev_if_node, lvl = IF_DIVIDE_POINT.pop()
            
            # 노드 생성 및 연결
            graph.node(while_head_id, f"while", shape='box', style="filled", fillcolor=blue)
            if prev_if_node: graph.edge(prev_if_node, while_head_id, label="False")
            graph.edge(prev_node,while_head_id,label=label_comment)

            # WHILE문 조건문 노드 생성 및 연결
            graph.node(while_condition_id, f"{loop_condition}", shape='diamond', style="filled", fillcolor=red)
            graph.edge(while_head_id,while_condition_id)

            label_comment = "True"
            prev_node = while_condition_id

        elif while_flag == bracket_lvl:
            # while문 루프 종료
            graph.edge(prev_node, while_node_id,label=label_comment)
            prev_node = while_node_id
            while_flag = 0
            
        elif line.startswith("for"):
            loop_condition = re.search(r'\((.*)\)', line).group(1)
            loop_parsing = loop_condition.split(';')  # for문은 세미콜론으로 구분됨


            # 이전 IF문 분기점 삭제
            prev_if_node = None
            while len(IF_DIVIDE_POINT) > 0 and IF_DIVIDE_POINT[-1][1] == bracket_lvl:
                prev_if_node, lvl = IF_DIVIDE_POINT.pop()

            # 노드 아이디 생성
            for_init_id = f'{line_num}_for_init_{loop_parsing[0].strip()}'
            for_condition_id = f'{line_num}_for_init_{loop_parsing[1].strip()}'
            for_end_id = f'{line_num}_for_init_{loop_parsing[2].strip()}'
            
            # 노드 생성
            graph.node(for_init_id, f"{loop_parsing[0]}", shape='box',style='filled', fillcolor=blue)
            graph.node(for_condition_id, f"{loop_parsing[1]}", shape='diamond',style='filled', fillcolor=red)
            graph.node(for_end_id, f"{loop_parsing[2]}", shape='box',style='filled', fillcolor=blue)

            if prev_if_node: graph.edge(prev_if_node, for_init_id)
            graph.edge(prev_node, for_init_id)
            

            graph.edge(for_init_id, for_condition_id)
            graph.edge(for_end_id, for_condition_id)

            # FOR문 분기점 추가
            FOR_DIVIDE_POINT.append([for_condition_id, bracket_lvl, for_end_id])

            label_comment = "True"

            prev_node = for_condition_id

        
            
        
        # 그 외의 일반문은 네모로 처리
        elif line:
            node_id = f'{line_num}_line_{line}'
            graph.node(node_id, line, shape='box',style='filled', fillcolor=blue)
        
            # 이전 IF문 분기점 삭제
            prev_if_node = None
            while len(IF_DIVIDE_POINT) > 0 and IF_DIVIDE_POINT[-1][1] >= bracket_lvl:
                prev_if_node, lvl = IF_DIVIDE_POINT.pop()
            
            
            if prev_if_node: graph.edge(prev_if_node, node_id, label="False")
            graph.edge(prev_node, node_id, label=label_comment)

            label_comment = ""
            prev_node = node_id
        

    ## END 포인트
    # end_node_id = f'end'
    # graph.node(end_node_id, f"end", shape="circle", style='filled', fillcolor=green)
    # graph.edge(prev_node, end_node_id, label=label_comment)
    
    return function_name, graph

class CFlowchartApp(wx.App):
    def OnInit(self):
        self.frame = CFlowchartFrame(None, "C Code Flowchart Generator")  # 부모창은 None으로 설정
        self.frame.Show()
        return True

class CFlowchartFrame(wx.Frame):
    def __init__(self, parent, title):
        # wx.Frame의 부모 및 제목 인자를 적절히 전달
        super().__init__(parent, title=title, size=(600, 300))

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # 텍스트 영역
        self.text_ctrl = wx.TextCtrl(panel, style=wx.TE_MULTILINE, size=(400, 200))
        vbox.Add(self.text_ctrl, 1, flag=wx.EXPAND | wx.ALL, border=10)

        # Generate 버튼
        self.generate_button = wx.Button(panel, label="Generate")
        vbox.Add(self.generate_button, 0, flag=wx.ALIGN_CENTER | wx.ALL, border=10)

        panel.SetSizer(vbox)

        self.generate_button.Bind(wx.EVT_BUTTON, self.on_generate)

    def on_generate(self, event):
        c_code = self.text_ctrl.GetValue()
        c_code = parse_c_comments(c_code)
        file_name, graph = convert_c_function(c_code)
        
        # 저장 경로를 절대 경로로 지정
        output_path = os.path.join(os.getcwd(), f'{file_name}')
        graph.render(output_path, format="png", view=True)  # PNG 이미지로 저장
        
        # 완료 메시지 박스
        if os.path.exists(output_path):
            wx.MessageBox(f"Flowchart saved as {file_name}.png", "Success", wx.ICON_INFORMATION)
        else:
            wx.MessageBox("Flowchart image generation failed!", "Error", wx.ICON_ERROR)

  

# 실행
if __name__ == "__main__":
    app = CFlowchartApp()
    app.MainLoop()