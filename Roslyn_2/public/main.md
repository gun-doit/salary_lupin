### 서론

RobustCommonLibrary, Utility 등 처음 라이브러리를 분석할 때 주석이 달려있지 않고, 프로그램이 어떻게 돌아가는지 모르니 인터페이스, 메서드, 클래스들의 간단한 요약 정보가 달린 API Docs가 필요하다고 생각하여 문서화 작업 프로세스를 진행하려고 함

### 조건

1. 문서화 작업이 수작업이 아닌, 자동화로 이루어져야 함
2. 코드 수정 시 같이 수정하게 만들어야 함

 ※ 즉, 코드를 수정하면 코드에 해당하는 폴더 및 문서에 일일이 접근해서 문서도 수정하는 번거로운 행동을 최대한 지양해야 함

1. 모르는 사용자도 이용하기 편리하게 해야 함
⇒ 때문에 자동화를 진행 & 이 문서를 작성하였다고 봐도 무방.

### 결론

1. SandcastleHelpFileBuilder (SHFB) ⇒ MS에서 공식 지원하지 않는 외부 프로젝트, 업데이트가 잘 이루어지지 않으므로 패스.
2. DocFX ⇒ MS에서 공식 지원하는 닷넷 툴 nuget 패키지. 결정

---

## 설명하기에 앞서

기존의 DocFX 2.75.2 버전은 SHFB와는 다르게 Obsolete된 클래스 등을 따로 표시하는 기능이 없었고, 이 기능의 존재 여부는 꽤나 중요하다고 생각했다.

따라서 플러그인 제작을 시도했으나, 관련 API에 대한 정보가 턱없이 부족하여, DocFX GitHub에서 Source Copy를 불러와서 Obsolete에 관한 부분을 직접 추가하여 빌드한 버전이 해당 버전이다.
(해당 버전의 파일은 DocFX_Install 폴더에 저장되어있고, Install 배치파일 실행시 자동 적용된다)

향 후 공식 DocFX가 새로운 버전으로 업데이트 되면서 기능들이 더 많아지면, 해당 버전을 버리는 것이 현재 진행하고자 하는 방향이다. ( 버전 유지보수에 자원이 낭비된다고 생각 )

---

## DocFX 사용 시작하기

[DocFX 관련 참고 내용](https://www.notion.so/DocFX-d00c7a9aef684a80810478b9d45bad40?pvs=21)

### **[1] 설치**

D:\Src\VS2024\docfx 경로에 들어가서 DocFX_Run.bat 실행하여 ‘5’ 입력

### [2] 변경된 메타데이터 (문서, 어셈블리) 적용

( 처음 설치 이후에는 무조건 실행해야 함 )
DocFX_Run.bat ⇒ '1' 입력

⇒ 솔루션의 갱신 정보를 api/~ 에 최신화 하는 과정

<aside>
💡 메타데이터 적용 및 빌드 이후 페이지에 반영되지 않으면
브라우저의 캐시를 지워보고 시도해보자

(크롬의 경우) 우측 상단 더보기 → 인터넷 사용 기록 삭제 → 캐시된 이미지 및 파일만 체크

</aside>

### [3] 빌드 및 로컬 호스팅

DocFX_Run.bat ⇒ '2' 입력

⇒ api/~의 정보와 템플릿을 이용하여 웹을 구성하여 빌드하는 단계

### [3-1] 이미 빌드된 페이지에 대한 로컬 호스팅

DocFX_Run.bat ⇒ '4' 입력

빌드에 사용되는 소요시간이 긴 편이므로, 이미 빌드가 되어있고, 최신화된 내용이 없다면 python3.x를 이용하여 바로 웹 로컬 호스팅이 가능함

- Python 3.12.2 다운로드 링크 (공식) (Win 64bit 전용)
    
    [](https://www.python.org/ftp/python/3.12.2/python-3.12.2-amd64.exe)
    

### [4] .md 파일 수정시

.md 파일은 markdown 형식의 파일로 현재 RobustCommonLibrary, Utility 내부의 .md 파일을 인식하도록 되어있음, 해당 .md 파일 수정 후, **D:\Src\VS2024\DocFX_UpdateMD.bat** 파일 실행

⇒ 각 .md 파일을 설정한 경로에 넣고. toc.yml 을 자동 작성해줌

- 다른 폴더에도 .md 를 추가하려면 DocFX_UpdateMD.bat 파일을 수정하면 된다.

### **자주하는 질문**

💡 **메타데이터 적용 및 빌드가 완료되었는데 페이지가 바뀌지 않는 경우**

이전 페이지가 캐싱되어있을 수 있다. 브라우저의 캐시를 지워보고 재시도하자.
(크롬의 경우) 우측 상단 더보기 → 인터넷 사용 기록 삭제 → 캐시된 이미지 및 파일만 체크

💡 **라이브러리 추가된 경우 확인해야 할 작업**

1. `docfx.json`에서 `metadata`에 적절한 값 추가 (src, files, exclude, dest)
2. `toc.yml`에서 name과 href값 추가, (name = 상단 탭 이름, href = dest 경로)
3. `.md` 파일 추가시 `<span class="orange">DocFX_UpdateMD.bat</span>`에서 직접 내용추가 및 실행
4. 빌드

💡 **CSS 또는 템플릿을 변경했는데, 적용되지 않은 경우**

1. 빌드가 제대로 되었는지 확인 (CSS, 템플릿의 경우 메타데이터 적용 불필요, 재빌드만 요구)
2. 브라우저 캐시를 지웠는지 확인
3. DocFX_Run.bat 에서 '6' 을 입력하여 설치 폴더에 제대로 적용했는지 확인

---

## 코드 문서화에 대한 XML 태그 (주석) 작성법

※ 모든 XML 태그는 클래스, 메서드 등의 선언부등의 Attribute를 제외한 바로 위에 위치해야함 

- 줄바꿈에 대한 참고사항
    
     summary 작성 시 줄바꿈은 두 번 해야 적용되며, 간격이 좁은 줄바꿈은 문단 뒤에 “  “(공백 두 개) 이후 한 번만 줄바꿈 하면 됨
    
    ```csharp
      /// <summary>
    	/// 로그인과 워크스페이스, 설정 등을 포함하여 여러 예시 폼, 기능들을 이어주는 역할
    	/// 
    	/// MainForm.cs => 메인 폼의 이벤트 처리를 위한 부분  < 여기 스페이스 바 두 번
    	/// MainFormStartLib.cs => 메인 폼의 초기화, 로그인 관련, 설정 저장, 설정 불러오기 등의 기능을 위한 부분
    	/// 
    	/// (초기 세팅) StockChartDataBoard 에서 시세 수신 + MarketDataSet 에서 실시간 이벤트 등록 등의 기능 포함
    	/// </summary>
    ```
    
    ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/e10de201-b3bf-4052-9d4c-d740f217cea8/7f42314c-8f8a-4476-9fe1-c28ee81103b8/Untitled.png)
    

| 설명 | 사용 예시 |
| --- | --- |
| 요소에 대한 설명 | <summary>
테스트 summary
</summary> |
| 예제 코드 | <example>
<code>
internal class ATESTEST {
        TESTEST;
}
</code>
</example> |
| 비고 | <remarks>
비고로 표시할 내용
</remarks> |
| 참고 주제 | <seealso cref="System.Object.GetType"></seealso> |
| **문서화 제외 대상** | **<exclude/>** |
| 글자에 색넣기 | <summary>
텍스트
<span style=”color: #색코드”>색상 텍스트</span>
텍스트
</summary> |
- (거의) 모든 태그를 포함한 예시 코드
    
    ```csharp
      /// <summary>
    	/// 테스트 summary
    	/// </summary>
    	/// <example>
    	/// <code>
    	/// internal class ATESTEST {
    	///		TESTEST;
    	/// }
    	/// </code>
    	/// </example>
    	/// <remarks>
    	/// 비고로 표시할 내용
    	/// </remarks>
    	/// <seealso cref="System.Object.GetType"></seealso>
    	[TestClass]
    	[Obsolete("테스트")]
    	public class AATest
    	{
    		~
    	}
    ```
    

### 결과

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/e10de201-b3bf-4052-9d4c-d740f217cea8/b4604ca6-1776-4e96-9b1b-f578ea88f378/Untitled.png)

---

# 문서화 커스터마이징

## 템플릿 (구성요소, 배치, 순서) 변경하기

기본적으로 사용되는 템플릿(modern 템플릿)은 다음 경로에 존재 (2.75.2 버전 기준)

```
C:\Users\(사용자)\.dotnet\tools\.store\docfx\2.75.2\docfx\2.75.2\templates\modern\partials
```

좌측 탐색기에서 각 네임스페이스를 선택했을 때 나오는 페이지 (클래스,인터페이스 등의 목록)
⇒ namespace.tmpl.partial

각 클래스 정보 페이지에 대한 템플릿

⇒ class.header.tmpl.partial

클래스 페이지에 대한 참고 주제 템플릿
(클래스 멤버에 대한 페이지가 분리되어있고, 이 끝에 참고 주제가 있음)

⇒ class.memberpage.tmpl.partial

[링크](https://www.notion.so/087140edf6fe4281b7969aa16dea99a3?pvs=21)

### Mustache 템플릿 엔진의 발견된 키워드들 (tmpl)

```html
# 변수는 {{ 와 }} 사이에 입력

# 객체 안에 객체가 있을 때는 .으로 구분
ex) {{syntax.content.0.value}}
=> syntax의 content 배열 요소 첫 번째(0)의 value 값.

# {{! 내용}} => 주석처리

# 외부(부분) 템플릿은 > 사용
{{>partial/~~}}

{{#isConditionMet}}
<div>조건이 충족되었을 때 표시될 내용</div>
{{/isConditionMet}}

{{^isConditionMet}}
<div>조건이 충족되지 않았을 때 표시될 내용</div>
{{/isConditionMet}}

※ 0, false, 빈 문자열은 거짓으로 판단됨
※ 변수의 값이 배열 (복수형) 이면 해당 조건문은 반복문이 됨

---------------------------------------------------

{{id}} 네임스페이스 및 클래스명을 . 대신 _ 로 구분한 것
ex) Robust_Controls_NoneClosingMenuStrip

{{uid}} 네임스페이스 및 클래스명을 . 로 구분한 것
ex) Robust.Controls.NoneClosingMenuStrip

{{sourceurl}} 알 수 없음

{{>partials/title}}
패키지, 네임스페이스, 클래스 등등에 따른 명시된 이름
(partials 폴더의 title.tmpl 파일을 의미)

{{__global.~~}} 한글화된 내용 (한글화 json 파일에 있는 변수명)

{{{namespace.specName.0.value}}} 네임스페이스 이름

{{assemblies.0}} 어셈블리명 (.dll 제외)

{{{summary}}} 서머리

{{{conceptual}}} 뭔지 모르겠음

{{syntax.content.0.value}} 아마도, 코드의 첫 줄 + 메타데이타

{{syntax.parameters}} 파라미터들

{{syntax.typeParameters}} 타입 파라미터

{{inheritance}} 상속

{{specName.0.value}} 상속 상위 클래스 이름 및 경로

{{name.0.value}} 해당 객체 이름

{{inClass}} 클래스가 상속되었는지? 

{{implements}} 인터페이스 구현한 것

{{derivedClasses}} 파생된 클래스들

{{inheritedMembers}} 상속받은 멤버

{{extensionMethods}} 확장메서드

{{definition}} .

{{#example}} 예제

{{#remarks}} 비고

{{children}} 하위항목 => {{#children}} 하위 항목 foreach 문
```

XML 주석 사용법 정리

템플릿 사용법 정리

## CSS 변경하기

기본적으로 사용되는 CSS (modern 템플릿)는 다음 경로에 존재 (2.75.2 버전 기준)

```
C:\Users\(사용자)\.dotnet\tools\.store\docfx\2.75.2\docfx\2.75.2\templates\modern\public\main.css
```

위 경로의 `main.css` 에서 템플릿에 쓰이는 각 css를 지정할 수 있다.

[2024-02-22 수정]
위처럼 사용하기보다, DocFX_Install 폴더 내에 있는 위 경로로 이동한 뒤, `main.css`를 수정하고 `DocFX_Run.bat` → `6` 을 실행시키는 것이 더 효율적이다.

---