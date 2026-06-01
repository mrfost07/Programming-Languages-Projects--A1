/* ==================== GLOBAL STATE ==================== */

let totalMemory = 100;
let usedMemory = 0;
let objects = [];

/* ==================== DARK MODE ==================== */

function toggleTheme() {
  const html = document.documentElement;
  const btn = document.getElementById('themeBtn');
  
  if (html.classList.contains('dark-mode')) {
    html.classList.remove('dark-mode');
    btn.innerHTML = '<i class="fas fa-moon"></i>';
    localStorage.setItem('theme', 'light');
  } else {
    html.classList.add('dark-mode');
    btn.innerHTML = '<i class="fas fa-sun"></i>';
    localStorage.setItem('theme', 'dark');
  }
}

// Load saved theme preference
function initTheme() {
  const savedTheme = localStorage.getItem('theme') || 'light';
  const html = document.documentElement;
  const btn = document.getElementById('themeBtn');
  
  if (savedTheme === 'dark') {
    html.classList.add('dark-mode');
    btn.innerHTML = '<i class="fas fa-sun"></i>';
  } else {
    html.classList.remove('dark-mode');
    btn.innerHTML = '<i class="fas fa-moon"></i>';
  }
}

/* ==================== MEMORY UI UPDATES ==================== */

function updateMemoryUI() {
  const usedPercent = (usedMemory / totalMemory) * 100;
  const freeMemory = totalMemory - usedMemory;
  const objectCount = objects.filter(obj => obj.used).length;

  // Update memory values
  document.getElementById("usedMemory").innerText = usedMemory + " MB";
  document.getElementById("freeMemory").innerText = freeMemory + " MB";
  document.getElementById("usagePercent").innerText = Math.round(usedPercent) + "%";
  document.getElementById("freePercent").innerText = Math.round(100 - usedPercent) + "%";
  document.getElementById("objectCount").innerText = objectCount;

  // Update progress bars
  document.getElementById("memoryProgress").style.width = usedPercent + "%";

  // Update stat card bars
  const usedBar = document.querySelector('[data-stat="used"] .stat-bar-fill');
  const freeBar = document.querySelector('[data-stat="free"] .stat-bar-fill');
  const countBar = document.querySelector('[data-stat="count"] .stat-bar-fill');
  
  if (usedBar) usedBar.style.width = usedPercent + "%";
  if (freeBar) freeBar.style.width = (100 - usedPercent) + "%";
  if (countBar) countBar.style.width = Math.min((objectCount / 10) * 100, 100) + "%";

  // Update object count badge
  document.getElementById("objectCountBadge").innerText = objectCount;
}

/* ==================== LOGGING SYSTEM ==================== */

function log(message) {
  const logs = document.getElementById("logs");
  const time = new Date().toLocaleTimeString();

  // Determine log type based on message content
  let logType = 'info';
  if (message.includes('failed') || message.includes('error') || message.includes('Error')) {
    logType = 'error';
  } else if (message.includes('removed') || message.includes('cleaned') || message.includes('GC')) {
    logType = 'success';
  }

  const logEntry = document.createElement('div');
  logEntry.className = 'log-entry';
  logEntry.innerHTML = `
    <span class="log-time">[${time}]</span>
    <span class="log-message log-${logType}">${escapeHtml(message)}</span>
  `;

  logs.appendChild(logEntry);
  logs.scrollTop = logs.scrollHeight;

  // Update log count
  const logCount = logs.querySelectorAll('.log-entry').length;
  document.getElementById("logCount").innerText = logCount + " " + (logCount === 1 ? "entry" : "entries");
}

function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

function clearLogs() {
  const logs = document.getElementById("logs");
  logs.innerHTML = '';
  document.getElementById("logCount").innerText = "0 entries";
  log("Logs cleared.");
}

/* ==================== OBJECT RENDERING ==================== */

function renderObjects() {
  const container = document.getElementById("objectsContainer");
  
  if (objects.length === 0) {
    container.innerHTML = `
      <div class="empty-state">
        <i class="fas fa-inbox"></i>
        <p>No memory objects yet</p>
        <p style="font-size: 0.9rem; opacity: 0.7;">Create an object to get started</p>
      </div>
    `;
    return;
  }

  container.innerHTML = '';

  objects.forEach((obj, index) => {
    const div = document.createElement("div");
    div.className = "object";

    const statusClass = obj.used ? 'status-active' : 'status-unused';
    const statusText = obj.used ? 'ACTIVE' : 'UNUSED';
    const statusIcon = obj.used ? 'fas fa-circle-check' : 'fas fa-circle-xmark';

    div.innerHTML = `
      <div class="object-info">
        <div class="object-name">
          <i class="fas fa-cube"></i>
          ${escapeHtml(obj.name)}
        </div>
        <div class="object-detail">
          <i class="fas fa-microchip"></i>
          <strong>${obj.size} MB</strong>
        </div>
        <div class="object-detail">
          <i class="fas fa-calendar-alt"></i>
          Date Created: <strong>${obj.createdAt}</strong>
        </div>
        <div class="object-detail">
          Status: <strong>${statusText}</strong>
        </div>
      </div>
    `;

    container.appendChild(div);
  });
}

function analyzeCode() {

  const code =
    document.getElementById("codeInput").value;

  objects = [];
  usedMemory = 0;

  try {

    const ast = acorn.parse(code, {
      ecmaVersion: "latest"
    });

    walk(ast);

    updateMemoryUI();
    renderObjects();

    log("Code analyzed successfully.");

    if (
      document.getElementById("gcType").value
      === "implicit"
    ) {
      log("Implicit GC triggered automatically.");
      runGC();
    }

  } catch(err) {

    log("Syntax Error: " + err.message);
  }
}

function walk(node) {

  if (!node) return;

  if (Array.isArray(node)) {
    node.forEach(walk);
    return;
  }

  if (
    node.type === "VariableDeclarator" &&
    node.init &&
    node.init.type === "ObjectExpression"
  ) {

    let objectSize = 5;

    // Basahon ang size gikan sa object
    const sizeProp = node.init.properties.find(
      p => p.key && p.key.name === "size"
    );

    if (sizeProp && sizeProp.value.type === "Literal") {
      objectSize = parseInt(sizeProp.value.value) || 5;
    }

    // Check kung naa pay memory
    if (usedMemory + objectSize > totalMemory) {

      log(
        `❌ Object "${node.id.name}" (${objectSize} MB) NOT created. Memory Full!`
      );

    } else {

      objects.push({
        name: node.id.name,
        size: objectSize,
        used: true,
        createdAt: new Date().toLocaleString()
      });

      usedMemory += objectSize;

      log(
        `📦 Object "${node.id.name}" created (${objectSize} MB)`
      );
    }
  }

  if (
    node.type === "AssignmentExpression" &&
    node.right &&
    node.right.type === "Literal" &&
    node.right.value === null
  ) {

    const obj =
      objects.find(
        o => o.name === node.left.name
      );

    if(obj){
      obj.used = false;
    }
  }

  for(const key in node){

    const value = node[key];

    if(
      value &&
      typeof value === "object"
    ){
      walk(value);
    }
  }
}

/* ==================== GARBAGE COLLECTION ==================== */

function runGC() {
  let cleaned = 0;
  let removedObjects = [];

  objects = objects.filter(obj => {
    if (!obj.used) {
      cleaned += obj.size;
      removedObjects.push(obj.name);
      return false;
    }
    return true;
  });

  usedMemory = Math.max(0, usedMemory - cleaned);

  log("♻️ Garbage Collection Started...");

  if (removedObjects.length > 0) {
    log(`🗑️ Removed objects: ${removedObjects.join(", ")}`);
    log(`🧹 Freed memory: ${cleaned} MB`);
  } else {
    log("⚠️ No unused objects found to remove.");
  }

  log(`📦 Current active objects: ${objects.length}`);
  log(`💾 Free memory available: ${totalMemory - usedMemory} MB`);

  updateMemoryUI();
  renderObjects();

  log("✅ Garbage Collection completed.");
}

/* ==================== #Example_Code ==================== */

/* ==================== INITIALIZATION ==================== */

document.addEventListener('DOMContentLoaded', function() {
  document.getElementById("codeInput").value =
`// #Example_Code

let a = { file: "Music", size: 20 };
let b = { file: "Movie", size: 25 };
let c = { file: "Temp File", size: 15 };
let d = { file: "Project", size: 20 };
let e = { file: "Backup", size: 15 };

b = null;
e = null;`;

  initTheme();
  updateMemoryUI();

  log("🚀 Memory Management System initialized.");
  log("ℹ️ Example code loaded.");
});