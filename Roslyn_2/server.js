const express = require('express');
const fs = require('fs');
const path = require('path');
const app = express();
const port = 3000;

// .md 파일이 있는 폴더 경로
const markdownFolderPath = path.join(__dirname, 'docs');
app.use(express.json()); 

// .md 파일 및 폴더 구조를 재귀적으로 탐색하는 함수
const getFolderTree = (folderPath) => {
    const result = [];
    const files = fs.readdirSync(folderPath); // 현재 폴더의 모든 파일과 폴더 목록 읽기

    files.forEach(file => {
        const filePath = path.join(folderPath, file);
        const stat = fs.statSync(filePath);

        if (stat.isDirectory()) {
            // 폴더일 경우, 해당 폴더를 트리 구조로 재귀적으로 탐색
            result.push({
                name: file,
                type: 'folder',
                children: getFolderTree(filePath)
            });
        } else if (file.endsWith('.md')) {
            // .md 파일인 경우, 파일명을 저장
            result.push({
                name: file,
                type: 'file',
                path: filePath.replace(markdownFolderPath + path.sep, '').replace(/\\/g, '/')
            });
        }
    });

    return result;
};

// index.html 파일을 클라이언트에 제공
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});


// docs 폴더의 트리 구조를 가져오는 API (POST 방식)
app.post('/api/docs', (req, res) => {
    try {
        const folderTree = getFolderTree(markdownFolderPath);
        res.json(folderTree);  // 클라이언트로 폴더 트리 구조 응답
    } catch (err) {
        res.status(500).send('폴더를 읽는 데 문제가 발생했습니다.');
    }
});

// .md 파일의 내용을 클라이언트에 제공하는 API (POST 방식)
app.post('/api/docs/item', (req, res) => {
    const { filename } = req.body;
    console.log('Request filename:', filename); // filename 확인

    const filePath = path.join(markdownFolderPath, filename);
    console.log('File path:', filePath); // 파일 경로 확인

    if (!filePath.endsWith('.md')) {
        return res.status(400).send('잘못된 파일 형식입니다. .md 파일만 허용됩니다.');
    }

    fs.readFile(filePath, 'utf-8', (err, data) => {
        if (err) {
            console.error('파일을 읽는 데 문제가 발생했습니다.', err); // 에러 로그 추가
            return res.status(500).send('파일을 읽는 데 문제가 발생했습니다.');
        }

        res.send(data);  // 클라이언트로 파일 내용 전송
    });
});


// ------------------------------------------------------------------------------------

// .md 파일의 내용을 클라이언트에 제공하는 API
app.get('/api/docs/:filename', (req, res) => {
    console.log("/api/docs/:filename", req.params.filename);

    // 요청된 파일의 경로를 추출
    const filePath = path.join(markdownFolderPath, req.params.filename);

    // 경로가 유효한지, 그리고 .md 파일인지 확인
    if (!filePath.startsWith(markdownFolderPath)) {
        return res.status(400).send('잘못된 파일 경로 요청입니다.');
    }

    // .md 확장자 체크
    if (!filePath.endsWith('.md')) {
        return res.status(400).send('잘못된 파일 형식입니다. .md 파일만 허용됩니다.');
    }

    // 파일을 읽어서 내용을 클라이언트에 전송
    fs.readFile(filePath, 'utf-8', (err, data) => {
        if (err) {
            return res.status(500).send('파일을 읽는 데 문제가 발생했습니다.');
        }

        res.send(data);  // 클라이언트로 파일 내용 전송
    });
});

// 정적 파일 서비스 (HTML, CSS, JS 파일 제공)
app.use(express.static(path.join(__dirname, 'public')));

app.listen(port, () => {
    console.log(`서버가 http://localhost:${port}에서 실행 중입니다.`);
});
