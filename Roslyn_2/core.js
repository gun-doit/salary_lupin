// core.js
import { transformMarkdown } from './transform-markdown.js';

export async function scanMarkdown() {
  if (!window.showDirectoryPicker) {
    alert("이 브라우저는 File System Access API를 지원하지 않습니다.\nChrome 또는 Edge를 사용하고, localhost 또는 HTTPS에서 실행하세요.");
    return;
  }

  const rootHandle = await window.showDirectoryPicker();
  const fileListElement = document.getElementById("file-list");
  fileListElement.innerHTML = ""; // 초기화

  await traverseDirectory(rootHandle, fileListElement);
}

async function traverseDirectory(dirHandle, parentUl, path = "") {
  for await (const [name, handle] of dirHandle.entries()) {
    const fullPath = `${path}/${name}`;

    if (handle.kind === "file" && name.endsWith(".md")) {
      const li = document.createElement("li");
      const link = document.createElement("a");
      link.href = "#";
      link.textContent = fullPath;
      link.onclick = async () => {
        const file = await handle.getFile();
        const text = await file.text();
        const html = transformMarkdown(text);
        document.querySelector("main").innerHTML = `<h2>${name}</h2><div>${html}</div>`;
      };

      li.appendChild(link);
      parentUl.appendChild(li);
    }

    else if (handle.kind === "directory") {
      const li = document.createElement("li");
      li.textContent = fullPath;

      const subUl = document.createElement("ul");
      li.appendChild(subUl);
      parentUl.appendChild(li);

      await traverseDirectory(handle, subUl, fullPath);
    }
  }
}
