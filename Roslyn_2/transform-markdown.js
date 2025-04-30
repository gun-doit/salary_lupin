// transform-markdown.js
export function transformMarkdown(mdText) {
    // 매우 단순한 Markdown to HTML 변환기 (예: #, ##, ###, 줄바꿈만 처리)
    return mdText
      .replace(/^### (.*$)/gim, '<h3>$1</h3>')
      .replace(/^## (.*$)/gim, '<h2>$1</h2>')
      .replace(/^# (.*$)/gim, '<h1>$1</h1>')
      .replace(/\*\*(.*?)\*\*/gim, '<strong>$1</strong>')
      .replace(/\n/g, '<br>');
  }
  