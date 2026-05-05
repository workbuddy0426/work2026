const express = require('express');
const path = require('path');
const fs = require('fs');
const { execSync } = require('child_process');

const app = express();
const PORT = process.env.PORT || 3000;

// ---------- Config ----------
const WORKBUDDY_DIR = path.resolve(__dirname, '..', '.workbuddy');
const TODOS_FILE = path.join(WORKBUDDY_DIR, 'todos.json');
const ALARMS_FILE = path.join(WORKBUDDY_DIR, 'alarms.json');
const MEMORY_DIR = path.join(WORKBUDDY_DIR, 'memory');

// ---------- Static Files ----------
app.use(express.static(__dirname));

// ---------- API: System Status ----------
app.get('/api/status', (req, res) => {
  res.json({
    server: '🦞 龙虾后台管理',
    version: '1.0.0',
    uptime: Math.floor(process.uptime()),
    timestamp: new Date().toISOString()
  });
});

// ---------- API: Today's Todos ----------
app.get('/api/todos', (req, res) => {
  try {
    if (!fs.existsSync(TODOS_FILE)) {
      return res.json({ todos: [], note: 'todos.json 不存在' });
    }
    const raw = fs.readFileSync(TODOS_FILE, 'utf-8');
    const data = JSON.parse(raw);
    const today = new Date().toISOString().slice(0, 10);

    // Find today's date key or the first date key
    let todosList = [];
    if (Array.isArray(data)) {
      todosList = data;
    } else if (data.todos && Array.isArray(data.todos)) {
      todosList = data.todos;
    } else {
      // Keyed by date
      const keys = Object.keys(data);
      const todayKey = keys.find(k => k.startsWith(today));
      const target = data[todayKey || keys[0]] || [];
      todosList = Array.isArray(target) ? target : [];
    }

    res.json({
      date: today,
      total: todosList.length,
      done: todosList.filter(t => t.done || t.status === 'completed').length,
      pending: todosList.filter(t => !t.done && t.status !== 'completed').length,
      todos: todosList
    });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// ---------- API: Alarms ----------
app.get('/api/alarms', (req, res) => {
  try {
    if (!fs.existsSync(ALARMS_FILE)) {
      return res.json({ alarms: [] });
    }
    const raw = fs.readFileSync(ALARMS_FILE, 'utf-8');
    res.json(JSON.parse(raw));
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// ---------- API: Learning Progress ----------
app.get('/api/learning', (req, res) => {
  try {
    const userMd = path.join(WORKBUDDY_DIR, '..', 'USER.md');
    const data = { chapters: [] };

    // Try reading 书籍目录.md if it exists
    const catalogFile = path.join(WORKBUDDY_DIR, '..', 'books', '书籍目录.md');
    if (fs.existsSync(catalogFile)) {
      const content = fs.readFileSync(catalogFile, 'utf-8');
      const chapters = content.split('\n').filter(l => l.startsWith('## '));
      data.chapters = chapters.map(c => c.replace('## ', '').trim());
    }

    res.json(data);
  } catch (err) {
    res.json({ chapters: [] });
  }
});

// ---------- API: Memory Usage Stats ----------
app.get('/api/memory', (req, res) => {
  try {
    const files = [];
    if (fs.existsSync(MEMORY_DIR)) {
      const items = fs.readdirSync(MEMORY_DIR, { withFileTypes: true });
      for (const item of items) {
        if (item.isFile() && item.name.endsWith('.md')) {
          const stat = fs.statSync(path.join(MEMORY_DIR, item.name));
          files.push({ name: item.name, size: stat.size, mtime: stat.mtime });
        } else if (item.isDirectory() && item.name !== 'snapshots') {
          const dirPath = path.join(MEMORY_DIR, item.name);
          const subFiles = fs.readdirSync(dirPath).filter(f => f.endsWith('.md'));
          files.push({ name: `${item.name}/ (${subFiles.length} 文件)`, size: 0, isDir: true });
        }
      }
    }
    res.json({ memoryDir: MEMORY_DIR, files });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// ---------- API: Refresh (placeholder for data reload) ----------
app.post('/api/refresh', (req, res) => {
  res.json({ refreshed: true, timestamp: new Date().toISOString() });
});

// ---------- Error handling ----------
app.use((err, req, res, next) => {
  console.error('Server error:', err);
  res.status(500).json({ error: '内部服务器错误' });
});

// ---------- Start ----------
app.listen(PORT, '0.0.0.0', () => {
  console.log('');
  console.log('  🦞 龙虾后台管理已启动');
  console.log('');
  console.log(`  Local:   http://localhost:${PORT}`);
  console.log(`  Network: http://0.0.0.0:${PORT}`);
  console.log('');
  console.log(`  静态文件路径: ${__dirname}`);
  console.log(`  WorkBuddy 目录: ${WORKBUDDY_DIR}`);
  console.log('');
});
