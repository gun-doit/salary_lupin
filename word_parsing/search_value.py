# import json

# # .json 파일 로드
# with open('value_data.json', 'r') as json_file:
#     VALUE = json.load(json_file)

# # 변수 이름 입력받기
# variable_name = input("변수 이름을 입력하세요: ")

# # 변수 이름에 해당하는 데이터 출력
# if variable_name in VALUE:
#     for item in VALUE[variable_name]:
#         print(f"잘못된 데이터 형식: {item}")
# else:
#     print(f"'{variable_name}'에 해당하는 변수가 존재하지 않습니다.")

import wx
import json

class VariableLookupApp(wx.Frame):
    def __init__(self, *args, **kw):
        super(VariableLookupApp, self).__init__(*args, **kw)

        self.panel = wx.Panel(self)
        self.panel.SetSize((400, 500))

        # 변수 이름 입력 필드
        self.var_name_label = wx.StaticText(self.panel, label="변수 이름 :", pos=(10, 10))
        # wx.TE_PROCESS_ENTER 스타일을 추가하여 Enter 키 이벤트 처리 가능
        self.var_name_text = wx.TextCtrl(self.panel, pos=(150, 10), size=(200, 25), style=wx.TE_PROCESS_ENTER)

        # 출력 영역
        self.result_label = wx.StaticText(self.panel, label="결과:", pos=(10, 50))
        self.result_text = wx.TextCtrl(self.panel, pos=(10, 80), size=(360, 130), style=wx.TE_MULTILINE|wx.TE_READONLY)

        # 버튼 생성 (버튼 크기를 크게 설정)
        self.lookup_button = wx.Button(self.panel, label="검색", pos=(150, 215), size=(100, 40))  # size 변경

        # 버튼 클릭 이벤트 연결
        self.lookup_button.Bind(wx.EVT_BUTTON, self.on_lookup_button_click)

        # Enter 키 이벤트 처리 (TextCtrl에서 Enter가 눌리면 검색 실행)
        self.var_name_text.Bind(wx.EVT_TEXT_ENTER, self.on_lookup_button_click)

        # 리사이즈 불가능하게 설정
        self.SetSizeHints(self.GetSize(), self.GetSize())  # 최소/최대 크기를 동일하게 설정하여 리사이즈 방지
        
        # JSON 파일 로드
        with open('value_data.json', 'r') as json_file:
            self.VALUE = json.load(json_file)

        self.Show()
        
    def on_lookup_button_click(self, event):
        # 변수 이름 입력 받기
        variable_name = self.var_name_text.GetValue()

        # 변수 이름에 해당하는 데이터 출력
        if variable_name in self.VALUE:
            result = ""
            for item in self.VALUE[variable_name]:
                result += f": {item}\n"
            self.result_text.SetValue(result)
        else:
            self.result_text.SetValue(f"'{variable_name}'에 해당하는 변수가 존재하지 않습니다.")

# wxPython 애플리케이션 실행
app = wx.App(False)
frame = VariableLookupApp(None, title="변수 검색", size=(400, 300))
app.MainLoop()
