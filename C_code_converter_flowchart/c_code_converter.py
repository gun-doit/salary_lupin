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
        

        # # 변수 선언문 (초기화하지 않은 선언문은 건너뛰기)
        if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*\s+[a-zA-Z_][a-zA-Z0-9_]*\s*;', line):
            continue
        
        # 초기화된 변수 선언문 처리 (자료형 제외, 변수명과 초기값만 포함)
        elif re.match(r'([a-zA-Z_][a-zA-Z0-9_]*\s+[a-zA-Z_][a-zA-Z0-9_]*\s*=\s*.*);', line):
            continue


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

    # for i in statements:
    #     print(i)

    return statements

def convert_c_function(c_code):
    # 간단한 파싱 (if/else, else if, for, printf, 일반문 처리)
    graph = Digraph(format='png')
    graph.attr(
        rankdir='TB',
        dpi='2000',
        # splines='true',
        size='5,5',
        nodesep='0.6',
        ranksep='0.3',
        fontsize='12'
    )  # 해상도 및 크기 조정

    exclude_code = ['{', '}']

    # 헤드 노드
    head_id = None
    function_name = ""
    
    # 반복문 처리
    repeat_index = -1
    repeat_flag = [False for i in range(100)]
    repeat_bracket = [0 for i in range(100)]
    repeat_condition_node_id = []
    repeat_condition = []
    label_comment = ""

    while_flag = False
    while_node_id = None

    # 스위치 처리
    switch_flag = False
    switch_node_id = 0
    switch_value = ""

    IF_DIVIDE_POINT = []
    IF_END_POINT = []

    bracket_lvl = 0
    max_bracket_lvl = 0

    prev_node = None
    for line_num, line in enumerate(c_code,start=1):
        line = line.replace("&&", "and").replace("||", "or")

        if any(e in line for e in exclude_code):
            if '{' in line:                 
                bracket_lvl += 1
                if max_bracket_lvl < bracket_lvl:   
                    max_bracket_lvl = bracket_lvl
            elif '}' in line:
                bracket_lvl -= 1
                
                # IF문 종료 처리
                while len(IF_DIVIDE_POINT) > 0 and IF_DIVIDE_POINT[-1][1] >= bracket_lvl:
                    IF_END_POINT.append(IF_DIVIDE_POINT[-1][0])
                    IF_DIVIDE_POINT.pop()

            # 반복문 속일때
            if repeat_index >= 0:
                if '{' in line:
                    repeat_bracket[repeat_index] += 1
                elif '}' in line:
                    repeat_bracket[repeat_index] -= 1
                    # 반복문 종료
                    if repeat_flag[repeat_index] and repeat_bracket[repeat_index] == 0:
                        label_comment = "False"
                        # 루프 종료 후 증감 처리
                        increment_node_id = f'{line_num}_increment_{repeat_condition[repeat_index]}'
                        graph.node(increment_node_id, f"{repeat_condition[repeat_index]}", shape='box',style='filled', fillcolor=blue)
                        graph.edge(prev_node, increment_node_id)
                        graph.edge(increment_node_id, repeat_condition_node_id[repeat_index], label=label_comment)
                        label_comment = ""
                        prev_node = repeat_condition_node_id[repeat_index]

                        #반복문 플래그 종료
                        repeat_flag[repeat_index] = False
                        repeat_index -= 1
                        
            
            continue
        # 첫 노드인 함수 이름 생성
        if line_num == 1:
            head_id = f'{line_num}_line_{line}'
            head_node_id = line.strip()
            function_name = re.search(r'\b(?:\w+\s*\([^)]*\)\s*)?(\w+)\s*\(', line).group(1)
            
            # 노드 생성 및 연결
            graph.node(head_id, f'{line}', shape='box',style='filled', fillcolor=green)
            prev_node = head_id
            continue

        elif line.startswith("switch"):
            switch_condition = re.search(r'switch\s*\((.*?)\)', line).group(1)
            switch_parsing_name = switch_condition.strip()
            
            node_id = f'{line_num}_switch_{switch_parsing_name}'
            switch_value = switch_parsing_name

            #현재 스위치 문 저장
            switch_flag = bracket_lvl
            switch_node_id = node_id

            #노드 생성
            graph.node(node_id,f'switch({switch_parsing_name})', shape='box',style='filled', fillcolor=blue)

            while len(IF_END_POINT) > 0:
                prev_node = IF_END_POINT[-1]
                IF_END_POINT.pop()
                graph.edge(prev_node,node_id)
                label_comment = ""
            else: graph.edge(prev_node,node_id)
            prev_node = node_id

        
        elif switch_flag and (line.startswith("case") or line.startswith("default")):
            if "case" in line: case_condition =  re.search(r'case\s+(\w+):', line).group(1) 
            else: case_condition = "defualt"

            node_id = f'{line_num}_switch_case_{case_condition}'

            #이전 노드 변경
            prev_node = switch_node_id
            
            #노드 생성
            graph.node(node_id, f'{switch_value} == {case_condition}', shape="diamond", style='filled', fillcolor=red)
            graph.edge(prev_node, node_id)
            prev_node = node_id

        elif switch_flag and line.startswith("break"):
            # 모든 if, for문 정리
                    
            # 반복문 처리
            repeat_index = -1
            repeat_flag = [False for i in range(100)]
            repeat_bracket = [0 for i in range(100)]
            repeat_condition_node_id = []
            repeat_condition = []
            label_comment = ""

            IF_DIVIDE_POINT = []
            IF_END_POINT = []
            continue
        
        elif switch_flag == bracket_lvl:
            #스위치문 빠져나옴
            prev_node = switch_node_id
            switch_flag = 0

        # WHILE
        elif line.startswith("while"):
            loop_condition = re.search(r'while\((.*)\)', line).group(1)

            while_condition_id = f'{line_num}_while_{loop_condition}'
            while_head_id = f'{line_num}_while'

            # 현재 반복문 저장
            while_flag = bracket_lvl
            while_node_id = while_condition_id
            
            # 노드 생성 및 연결
            graph.node(while_head_id, f"while", shape='box', style="filled", fillcolor=blue)
            while len(IF_END_POINT) > 0:
                prev_node = IF_END_POINT[-1]
                IF_END_POINT.pop()
                graph.edge(prev_node,node_id)
                label_comment = ""
            else: graph.edge(prev_node,while_head_id,label=label_comment)

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
            
            # 모든 if, for문 정리
                    
            # 반복문 처리
            repeat_index = -1
            repeat_flag = [False for i in range(100)]
            repeat_bracket = [0 for i in range(100)]
            repeat_condition_node_id = []
            repeat_condition = []
            label_comment = "False"
            
            IF_DIVIDE_POINT = []
            IF_END_POINT = []
            
            continue
            

        elif line.startswith("for"):
            loop_condition = re.search(r'\((.*)\)', line).group(1)
            loop_parsing = loop_condition.split(';')  # for문은 세미콜론으로 구분됨

            # 현재 반복문 저장
            repeat_index += 1
            repeat_flag[repeat_index] = True
            repeat_bracket[repeat_index] += 1
            repeat_condition.append(loop_parsing[2])
            label_comment = "True"

            # 반복문 시작
            temp = ' '.join(loop_parsing[0].split(' ')[1:])
            repeat_init_id = f'{line_num}_for_{temp}'
            
            graph.node(repeat_init_id, f"{temp}", shape='box',style='filled', fillcolor=blue)
            while len(IF_END_POINT) > 0:
                prev_node = IF_END_POINT[-1]
                IF_END_POINT.pop()
                graph.edge(prev_node,node_id)
                label_comment = ""
            else: graph.edge(prev_node, repeat_init_id)
            prev_node = repeat_init_id

            # 조건 부분
            repeat_condition_id = f'{line_num}_condition_{loop_parsing[1]}'
            repeat_condition_node_id.append(repeat_condition_id)
            graph.node(repeat_condition_id, f"{loop_parsing[1]}", shape='diamond',style='filled', fillcolor=red)
            graph.edge(repeat_init_id, repeat_condition_id,label=label_comment)
            label_comment = ""
            # 루프 조건 재확인
            # graph.edge(increment_node_id, condition_node_id, label="Repeat")

            prev_node = repeat_condition_id
            continue

        # IF 조건문 처리
        elif line.startswith("if"):
            condition = re.search(r'\((.*)\)', line).group(1)
            node_id = f'{line_num}_if_{condition}'
            graph.node(node_id, f"if {condition}", shape='diamond',style='filled', fillcolor=red)


            #if 문 스택에 추가 개선 로직
            # 이전 스택 확인 후 제거후 삽입
            if len(IF_DIVIDE_POINT) > 0 and bracket_lvl <= IF_DIVIDE_POINT[-1][1]:
                while IF_DIVIDE_POINT[-1][1] > bracket_lvl:
                    IF_DIVIDE_POINT.pop()
                prev_node, tmp = IF_DIVIDE_POINT.pop()
            IF_DIVIDE_POINT.append([node_id, bracket_lvl])

            # 노드 연결
            graph.edge(prev_node, node_id, label=label_comment)
            prev_node = node_id

            label_comment = "True"

            

        # 'else if' 문 처리
        elif line.startswith("else if"):
            condition = re.search(r'\((.*)\)', line).group(1)
            node_id = f'{line_num}_else_if_{condition}'
            graph.node(node_id, f"else if {condition}", shape='diamond',style='filled', fillcolor=red)

            
            # 이전 조건문으로 분기
            IF_DIVIDE_POINT.append([node_id, bracket_lvl])
            prev_node, tmp = IF_DIVIDE_POINT.pop()
            label_comment = "False"

            graph.edge(prev_node, node_id, label=label_comment)
            label_comment = ""
            prev_node = node_id

            
        
        # 'else' 문 처리
        elif line.startswith("else"):
            # node_id = f'{line_num}_else_{prev_node}'
            # graph.node(node_id, "else", shape='diamond',style='filled', fillcolor=red)
            
            #이전 조건문에서 분기
            IF_DIVIDE_POINT.append([node_id, bracket_lvl])
            prev_node, tmp = IF_DIVIDE_POINT.pop()
            label_comment = "False"
            

        
        # 그 외의 일반문은 네모로 처리
        elif line:
            node_id = f'{line_num}_line_{line}'
            graph.node(node_id, line, shape='box',style='filled', fillcolor=blue)
        
            while len(IF_END_POINT) > 0:
                graph.edge(IF_END_POINT.pop(),node_id, label="False")
                
            else: 
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