import re
from graphviz import Digraph

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

    

    prev_node = None
    for line in c_code:
        print(line)
        line = line.replace("&&", "and").replace("||", "or")

        if any(e in line for e in exclude_code):
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
                        increment_node_id = f'increment_{repeat_condition[repeat_index]}'
                        graph.node(increment_node_id, f"{repeat_condition[repeat_index]}", shape='box',style='filled', fillcolor=blue)
                        graph.edge(prev_node, increment_node_id)
                        graph.edge(increment_node_id, repeat_condition_node_id[repeat_index], label=repeat_start_end_flag)
                        prev_node = repeat_condition_node_id[repeat_index]

                        #반복문 플래그 종료
                        repeat_flag[repeat_index] = False
                        repeat_index -= 1
                        
            
            continue
        if line.startswith("for"):
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
            repeat_init_id = f'for_{temp}'
            
            graph.node(repeat_init_id, f"{temp}", shape='box',style='filled', fillcolor=blue)
            if prev_node:
                graph.edge(prev_node, repeat_init_id, )
            prev_node = repeat_init_id

            # 조건 부분
            repeat_condition_id = f'condition_{loop_parsing[1]}'
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
            node_id = f'if_{condition}'
            graph.node(node_id, f"if {condition}", shape='diamond',style='filled', fillcolor=red)
            if prev_node:
                graph.edge(prev_node, node_id, label=repeat_start_end_flag)
                repeat_start_end_flag = ""
            prev_node = node_id

        # 'else if' 문 처리
        elif line.startswith("else if"):
            condition = re.search(r'\((.*)\)', line).group(1)
            node_id = f'else_if_{condition}'
            graph.node(node_id, f"else if {condition}", shape='diamond',style='filled', fillcolor=red)
            graph.edge(prev_node, node_id, label=repeat_start_end_flag)
            repeat_start_end_flag = ""  # 이전 'if' 또는 'else'와 연결
            prev_node = node_id
        
        # 'else' 문 처리
        elif line.startswith("else"):
            node_id = f'else_{prev_node}'
            graph.node(node_id, "else", shape='diamond',style='filled', fillcolor=red)
            graph.edge(prev_node, node_id, label=repeat_start_end_flag)
            repeat_start_end_flag = ""
            prev_node = node_id
        
        # 그 외의 일반문은 네모로 처리
        elif line:
            node_id = f'line_{line}'
            graph.node(node_id, line, shape='box',style='filled', fillcolor=blue)
            if prev_node:
                graph.edge(prev_node, node_id, label=repeat_start_end_flag)
                repeat_start_end_flag = ""
            prev_node = node_id

    end_node_id = f'end'
    graph.node(end_node_id, f"end", shape="circle", style='filled', fillcolor=red)
    graph.edge(prev_node, end_node_id)
    return graph

# C 코드 불러오기
c_code = """
"""

# Graphviz로 순서도 생성
code = parse_c_comments(c_code)
graph = convert_c_function(code)
graph.render('example_flowchart', view=True)  # 'example_flowchart.png'로 저장 및 보기
