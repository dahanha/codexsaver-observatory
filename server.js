const http = require('http');
const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');

const PORT = 3000;

const server = http.createServer((req, res) => {
  if (req.url === '/' || req.url === '/app.html') {
    fs.readFile(path.join(__dirname, 'app.html'), (err, data) => {
      if (err) {
        res.writeHead(500);
        res.end('Error loading app');
        return;
      }
      res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
      res.end(data);
    });
  } else {
    res.writeHead(404);
    res.end();
  }
});

server.listen(PORT, () => {
  console.log('Pomodoro timer running at http://localhost:' + PORT);
  const cmd = 'start http://localhost:' + PORT;
  exec(cmd);
});
