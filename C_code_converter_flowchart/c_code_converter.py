import wx
import re
from graphviz import Digraph
import os
import subprocess

blue = "#DAE8FC"
red = "#F8CECC"

def parse_c_function(c_code):
    lines = c_code.splitlines()
    graph = Digraph(format='png')
    graph.attr(
        rankdir='TB',
        dpi='2000',
        size='5,5',
        nodesep='0.6',
        ranksep='0.3',
        fontsize='12'
    )

    exclude_code = ['{', '}']
    if_exclude_code = ['#if 0', '#ifdef WIRECAR']
    
    repeat_index = -1
    repeat_flag = [False for i in range(100)]
    repeat_bracket = [0 for i in range(100)]
    repeat_condition_node_id = []
    repeat_condition = []

    comments_flag = False
    if_flag = False
    
    statements = []
    temp_line = ""
    for line in c_code.splitlines():
        line = line.strip()
        if line:
            temp_line += " " + line
        if line.endswith((';')):
            statements.append(temp_line.strip())
            temp_line = ""
        if line.endswith(('{', '}')):
            statements.append(temp_line.strip()[:-1])
            if line.endswith('{'): statements.append('{')
            else: statements.append('}')
            temp_line = ""

    if temp_line:
        statements.append(temp_line.strip())

    prev_node = None
    function_name = statements[0].split(' ')[1]
    for line in statements:
        line = re.sub(r'//.*', '', line)
        line = re.sub(r'/\*.*?\*/', '', line, flags=re.DOTALL)
        line = line.strip()

        line = line.replace("&&", "and").replace("||", "or")

        if any(e in line for e in if_exclude_code):
            if_flag = True
            continue

        if if_flag == True:
            if line == "#endif":
                if_flag = False
            continue

        if '/*' in line:
            comments_flag = True
            continue
        
        if comments_flag:
            if '*/' in line:
                comments_flag = False
            continue

        if any(e in line for e in exclude_code):
            if repeat_index >= 0:
                if '{' in line:
                    repeat_bracket[repeat_index] += 1
                elif '}' in line:
                    repeat_bracket[repeat_index] -= 1
                    if repeat_flag[repeat_index] and repeat_bracket[repeat_index] == 0:
                        increment_node_id = f'increment_{repeat_condition[repeat_index]}'
                        graph.node(increment_node_id, f"{repeat_condition[repeat_index]}", shape='box',style='filled', fillcolor=blue)
                        graph.edge(prev_node, increment_node_id)
                        graph.edge(increment_node_id, repeat_condition_node_id[repeat_index])
                        prev_node = repeat_condition_node_id[repeat_index]
                        repeat_flag[repeat_index] = False
                        repeat_index -= 1
            continue

        if line.startswith("for"):
            loop_condition = re.search(r'\((.*)\)', line).group(1)
            loop_parsing = loop_condition.split(';')

            repeat_index += 1
            repeat_flag[repeat_index] = True
            repeat_bracket[repeat_index] += 1
            repeat_condition.append(loop_parsing[2])

            temp = ' '.join(loop_parsing[0].split(' ')[1:])
            repeat_init_id = f'for_{temp}'
            graph.node(repeat_init_id, f"{temp}", shape='box',style='filled', fillcolor=blue)
            if prev_node:
                graph.edge(prev_node, repeat_init_id)
            prev_node = repeat_init_id

            repeat_condition_id = f'condition_{loop_parsing[1]}'
            repeat_condition_node_id.append(repeat_condition_id)
            graph.node(repeat_condition_id, f"{loop_parsing[1]}", shape='diamond',style='filled', fillcolor=red)
            graph.edge(repeat_init_id, repeat_condition_id)

            prev_node = repeat_condition_id
            continue

        if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*\s+[a-zA-Z_][a-zA-Z0-9_]*\s*;', line):
            continue
        
        elif re.match(r'([a-zA-Z_][a-zA-Z0-9_]*\s+[a-zA-Z_][a-zA-Z0-9_]*\s*=\s*.*);', line):
            var_init = " ".join(line.split(' ')[1:]).replace(';','')
            node_id = f'{var_init}_init'
            graph.node(node_id, f'{var_init}', shape='box',style='filled', fillcolor=blue)
            if prev_node:
                graph.edge(prev_node, node_id)
            prev_node = node_id
            continue

        elif line.startswith("if"):
            condition = re.search(r'\((.*)\)', line).group(1)
            node_id = f'if_{condition}'
            graph.node(node_id, f"if {condition}", shape='diamond',style='filled', fillcolor=red)
            if prev_node:
                graph.edge(prev_node, node_id)
            prev_node = node_id

        elif line.startswith("else if"):
            condition = re.search(r'\((.*)\)', line).group(1)
            node_id = f'else_if_{condition}'
            graph.node(node_id, f"else if {condition}", shape='diamond',style='filled', fillcolor=red)
            graph.edge(prev_node, node_id)
            prev_node = node_id

        elif line.startswith("else"):
            node_id = f'else_{prev_node}'
            graph.node(node_id, "else", shape='diamond',style='filled', fillcolor=red)
            graph.edge(prev_node, node_id)
            prev_node = node_id

        elif line:
            node_id = f'line_{line}'
            graph.node(node_id, line, shape='box',style='filled', fillcolor=blue)
            if prev_node:
                graph.edge(prev_node, node_id)
            prev_node = node_id

    end_node_id = f'end'
    graph.node(end_node_id, f"end", shape="circle", style='filled', fillcolor=red)
    graph.edge(prev_node, end_node_id)
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
        
        # 이미지 표시 (Flowchart 이미지)
        self.image_panel = wx.Panel(panel)
        self.image_bitmap = None
        vbox.Add(self.image_panel, 1, flag=wx.EXPAND | wx.ALL, border=10)

        panel.SetSizer(vbox)

        self.generate_button.Bind(wx.EVT_BUTTON, self.on_generate)

    def on_generate(self, event):
        c_code = self.text_ctrl.GetValue()
        file_name, graph = parse_c_function(c_code)
        
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