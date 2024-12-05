import wx
import re
from graphviz import Digraph
import os
import subprocess
import copy

blue = "#DAE8FC"
red = "#F8CECC"

def parse_c_comments(c_code):
    lines = c_code.splitlines()

    #if 0 and #ifdef 처리
    if_exclude_code = ['#if 0', '#ifdef WIRECAR']
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

        
        temp_lines = re.split(r'([{}])', temp_line)
        # print(temp_lines, len(temp_lines),":", temp_line)
        if(len(temp_lines) > 1):
            for tmp in temp_lines:
                if(tmp == ''): continue
                statements.append(tmp.strip())
                temp_line = ""


        # blines = re.split(r'(\{\})', line)
        # print(len(blines),':', line, blines)
        # if(len(blines) > 1):
        #     for tmp in blines:
        #         statements.append(tmp.strip())
        #     temp_line = ""
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
    
    # 반복문 처리
    repeat_index = -1
    repeat_flag = [False for i in range(100)]
    repeat_bracket = [0 for i in range(100)]
    repeat_condition_node_id = []
    repeat_condition = []
    repeat_start_end_flag = ""

    if_index = -1
    if_stack = []

    bracket_lvl = 0
    max_bracket_lvl = 0

    

    prev_node = None
    for line_num, line in enumerate(c_code,start=1):
        line = line.replace("&&", "and").replace("||", "or")
        print(line_num, " : ", line)

        if any(e in line for e in exclude_code):
            if '{' in line:
                bracket_lvl += 1
                if max_bracket_lvl < bracket_lvl:
                    max_bracket_lvl = bracket_lvl
            elif '}' in line:
                bracket_lvl -= 1

            # 반복문 속일때
            if repeat_index >= 0:
                if '{' in line:
                    repeat_bracket[repeat_index] += 1
                elif '}' in line:
                    repeat_bracket[repeat_index] -= 1
                    # 반복문 종료
                    if repeat_flag[repeat_index] and repeat_bracket[repeat_index] == 0:
                        repeat_start_end_flag = "False"
                        # 루프 종료 후 증감 처리
                        increment_node_id = f'{line_num}_increment_{repeat_condition[repeat_index]}'
                        graph.node(increment_node_id, f"{repeat_condition[repeat_index]}", shape='box',style='filled', fillcolor=blue)
                        graph.edge(prev_node, increment_node_id)
                        graph.edge(increment_node_id, repeat_condition_node_id[repeat_index], label=repeat_start_end_flag)
                        prev_node = repeat_condition_node_id[repeat_index]

                        #반복문 플래그 종료
                        repeat_flag[repeat_index] = False
                        repeat_index -= 1
                        
            
            continue
        if line.startswith("for"):
            print("for문 체크")
            loop_condition = re.search(r'\((.*)\)', line).group(1)
            loop_parsing = loop_condition.split(';')  # for문은 세미콜론으로 구분됨

            # 현재 반복문 저장
            repeat_index += 1
            repeat_flag[repeat_index] = True
            repeat_bracket[repeat_index] += 1
            repeat_condition.append(loop_parsing[2])
            repeat_start_end_flag = "True"

            # 반복문 시작
            temp = ' '.join(loop_parsing[0].split(' ')[1:])
            repeat_init_id = f'{line_num}_for_{temp}'
            
            graph.node(repeat_init_id, f"{temp}", shape='box',style='filled', fillcolor=blue)
            if prev_node:
                graph.edge(prev_node, repeat_init_id, )
            prev_node = repeat_init_id

            # 조건 부분
            repeat_condition_id = f'{line_num}_condition_{loop_parsing[1]}'
            repeat_condition_node_id.append(repeat_condition_id)
            graph.node(repeat_condition_id, f"{loop_parsing[1]}", shape='diamond',style='filled', fillcolor=red)
            graph.edge(repeat_init_id, repeat_condition_id)
            
            # 루프 조건 재확인
            # graph.edge(increment_node_id, condition_node_id, label="Repeat")

            prev_node = repeat_condition_id
            continue

        # 'if' 문 처리
        elif line.startswith("if"):
            condition = re.search(r'\((.*)\)', line).group(1)
            node_id = f'{line_num}_if_{condition}'
            graph.node(node_id, f"if {condition}", shape='diamond',style='filled', fillcolor=red)

            #이전 조건문 확인
            if len(if_stack) > 0:
                while if_stack[-1][1] > bracket_lvl:
                    if_stack.pop()
                if if_stack[-1][1] == bracket_lvl:
                    prev_node, tmp = if_stack.pop()

            if prev_node:
                graph.edge(prev_node, node_id, label=repeat_start_end_flag)
                repeat_start_end_flag = ""
            prev_node = node_id

            #if 문 스택에 추가
            if_stack.append([node_id, bracket_lvl])

        # 'else if' 문 처리
        elif line.startswith("else if"):
            condition = re.search(r'\((.*)\)', line).group(1)
            node_id = f'{line_num}_else_if_{condition}'
            graph.node(node_id, f"else if {condition}", shape='diamond',style='filled', fillcolor=red)

            
            # 이전 조건문으로 분기
            prev_node, tmp = if_stack.pop()

            graph.edge(prev_node, node_id, label=repeat_start_end_flag)
            repeat_start_end_flag = ""  # 이전 'if' 또는 'else'와 연결
            prev_node = node_id
            
            #if 문 스택에 추가
            if_stack.append([node_id, bracket_lvl])
        
        # 'else' 문 처리
        elif line.startswith("else"):
            # node_id = f'{line_num}_else_{prev_node}'
            # graph.node(node_id, "else", shape='diamond',style='filled', fillcolor=red)
            
            #이전 조건문 확인
            if len(if_stack) > 0:
                while if_stack[-1][1] > bracket_lvl:
                    if_stack.pop()
                if if_stack[-1][1] == bracket_lvl:
                    prev_node, tmp = if_stack.pop()


            # graph.edge(prev_node, node_id, label=repeat_start_end_flag)
            # repeat_start_end_flag = ""
            # prev_node = node_id
            
            #if 문 스택에 추가
            if_stack.append([node_id, bracket_lvl])
        
        # 그 외의 일반문은 네모로 처리
        elif line:
            node_id = f'{line_num}_line_{line}'
            graph.node(node_id, line, shape='box',style='filled', fillcolor=blue)
            #이전 조건문 확인
            if len(if_stack) > 0:
                while if_stack[-1][1] > bracket_lvl:
                    if_stack.pop()
                if if_stack[-1][1] == bracket_lvl:
                    prev_node, tmp = if_stack.pop()
            if prev_node:
                graph.edge(prev_node, node_id, label=repeat_start_end_flag)
                repeat_start_end_flag = ""
            prev_node = node_id


    end_node_id = f'end'
    graph.node(end_node_id, f"end", shape="circle", style='filled', fillcolor=red)
    graph.edge(prev_node, end_node_id, label=repeat_start_end_flag)
    return graph

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
        
        # 이미지 표시 (Flowchart 이미지)
        self.image_panel = wx.Panel(panel)
        self.image_bitmap = None
        vbox.Add(self.image_panel, 1, flag=wx.EXPAND | wx.ALL, border=10)

        panel.SetSizer(vbox)

        self.generate_button.Bind(wx.EVT_BUTTON, self.on_generate)

    def on_generate(self, event):
        c_code = self.text_ctrl.GetValue()
        c_code = parse_c_comments(c_code)
        graph = convert_c_function(c_code)
        file_name = "test_output"
        
        # 저장 경로를 절대 경로로 지정
        output_path = os.path.join(os.getcwd(), f'{file_name}')
        graph.render(output_path, view=False)
        
        # 완료 메시지 박스
        if os.path.exists(output_path):
            wx.MessageBox(f"Flowchart saved as {file_name}.png", "Success", wx.ICON_INFORMATION)
        else:
            wx.MessageBox("Flowchart image generation failed!", "Error", wx.ICON_ERROR)

  

# 실행
if __name__ == "__main__":
    app = CFlowchartApp()
    app.MainLoop()