// static/script.js

const treeFeatures = {
    Claude: {
        title: 'Claude',
        description: 'Cloud-inspired behavior checking for objects that act like ducks across different environments.',
        example: 'Object with quack() and walk() methods is accepted as duck-like.'
    },
    jules: {
        title: 'jules',
        description: 'Interactive extension for quirky duck objects and simulated behavior flows.',
        example: 'Use it to demonstrate duck typing in playful examples.'
    },
    stitch: {
        title: 'stitch',
        description: 'Linking object behavior and compatibility into a structured feature tree.',
        example: 'Tracks whether objects fit the duck interface by method shape.'
    }
};

const typingSystems = {
    Python: 'Dynamic',
    JavaScript: 'Dynamic',
    Java: 'Static'
};

const aiEngines = {
    Claude: {
        name: 'Claude',
        flavor: 'concise, cloud-native analysis',
        prefix: '[Claude]'
    },
    jules: {
        name: 'jules',
        flavor: 'playful, example-driven analysis',
        prefix: '[jules]'
    }
};

const codeSamples = {
    Python: `class Duck:
    def quack(self):
        print("Quack!")

    def walk(self):
        print("Walking...")

if __name__ == '__main__':
    duck = Duck()
    duck.quack()
    duck.walk()`,
    JavaScript: `class RobotDuck {
    quack() {
        console.log("Quack!");
    }

    walk() {
        console.log("Walking...");
    }
}

const duck = new RobotDuck();
duck.quack();
duck.walk();`,
    Java: `interface Duck {
    void quack();
    void walk();
}

class RobotDuck implements Duck {
    public void quack() {
        System.out.println("Quack!");
    }

    public void walk() {
        System.out.println("Walking...");
    }
}

// Java execution is not supported in-browser.
`};

// Pyodide (Python-in-browser) initialization
let pyodide = null;
let pyodideReadyPromise = null;
(function initPyodide() {
    const statusEl = () => document.getElementById('pyStatus');
    if (typeof loadPyodide === 'function') {
        pyodideReadyPromise = loadPyodide({ indexURL: 'https://cdn.jsdelivr.net/pyodide/v0.23.4/full/' })
            .then(p => {
                pyodide = p;
                const s = statusEl(); if (s) s.textContent = 'Python runtime: ready';
                return p;
            })
            .catch(e => {
                const s = statusEl(); if (s) s.textContent = 'Python runtime: failed to load';
                console.error('Pyodide load error', e);
            });
    } else {
        pyodideReadyPromise = new Promise((resolve, reject) => {
            const script = document.createElement('script');
            script.src = 'https://cdn.jsdelivr.net/pyodide/v0.23.4/full/pyodide.js';
            script.onload = function () {
                loadPyodide({ indexURL: 'https://cdn.jsdelivr.net/pyodide/v0.23.4/full/' })
                    .then(p => {
                        pyodide = p;
                        const s = statusEl(); if (s) s.textContent = 'Python runtime: ready';
                        resolve(p);
                    })
                    .catch(err => {
                        const s = statusEl(); if (s) s.textContent = 'Python runtime: failed to init';
                        reject(err);
                    });
            };
            script.onerror = function (e) {
                const s = statusEl(); if (s) s.textContent = 'Failed to load pyodide script';
                reject(e);
            };
            document.head.appendChild(script);
        });
    }
})();

function updateTypingInfo(language) {
    const info = document.getElementById('typingInfo');
    const system = typingSystems[language] || 'Unknown';
    const engineSel = document.getElementById('aiEngine');
    const engine = engineSel ? (aiEngines[engineSel.value] || aiEngines.Claude) : aiEngines.Claude;

    info.innerHTML = `
        <strong>${language}</strong> is generally <strong>${system}</strong> typed.
        <br><em>${engine.prefix} ${engine.flavor}</em>
        <div style="margin-top:8px">${system === 'Dynamic'
            ? 'Duck typing fits well here because objects are accepted by behavior.'
            : 'Static typing checks types before runtime and often requires explicit interfaces.'}</div>
    `;

    const codeInput = document.getElementById('codeInput');
    if (codeInput) codeInput.value = codeSamples[language] || '';
}

async function runCodeFromInput() {
    const language = document.getElementById('language').value;
    const engineName = document.getElementById('aiEngine')?.value || 'Claude';
    const engine = aiEngines[engineName] || aiEngines.Claude;
    const code = document.getElementById('codeInput').value || '';
    const outputEl = document.getElementById('codeRunOutput');
    outputEl.textContent = '';

    if (!code.trim()) {
        outputEl.textContent = 'No code provided.';
        return;
    }

    if (language === 'JavaScript') {
        // Create a blob-based iframe to safely execute the code and capture console output
        const html = `<!doctype html><html><body><script>
            (function(){
                const logs = [];
                const origLog = console.log;
                console.log = function(){
                    try { logs.push(Array.from(arguments).join(' ')); }
                    catch(e){}
                    origLog.apply(console, arguments);
                };
                try {
                    ${code}
                } catch (err) {
                    logs.push('Error: ' + err.message);
                }
                // write logs to body
                document.body.textContent = logs.join('\n');
            })();
        <\/script></body></html>`;

        const blob = new Blob([html], { type: 'text/html' });
        const url = URL.createObjectURL(blob);
        const iframe = document.createElement('iframe');
        iframe.style.display = 'none';
        iframe.src = url;
        document.body.appendChild(iframe);

        iframe.onload = function () {
            try {
                const result = iframe.contentDocument.body.textContent || '';
                outputEl.textContent = `${engine.prefix} ${result || 'No output.'}`;
            } catch (e) {
                outputEl.textContent = `${engine.prefix} Execution error: ` + e.message;
            }
            URL.revokeObjectURL(url);
            iframe.remove();
        };

        return;
    }

    if (language === 'Python') {
        // Execute Python using Pyodide in the browser
        try {
            await pyodideReadyPromise;
        } catch (e) {
            outputEl.textContent = `${engine.prefix} Python runtime not available.`;
            return;
        }

        try {
            const indented = code.split('\n').map(l => '    ' + l).join('\n');
            const runner = `import sys, io, traceback\nbuf = io.StringIO()\nsys_stdout = sys.stdout\nsys.stdout = buf\ntry:\n${indented}\nexcept Exception:\n    traceback.print_exc()\nfinally:\n    sys.stdout = sys_stdout`;

            await pyodide.runPythonAsync(runner);
            const result = await pyodide.runPythonAsync('buf.getvalue()');
            outputEl.textContent = `${engine.prefix} ${result || 'No output.'}`;
        } catch (err) {
            outputEl.textContent = `${engine.prefix} Python execution error: ${err}`;
        }

        return;
    }

    // Fallback: static analysis for other languages (e.g., Java)
    const used = [];
    if (/quack\s*\(/i.test(code) || /quack\s*:/i.test(code)) used.push('quack()');
    if (/walk\s*\(/i.test(code) || /walk\s*:/i.test(code)) used.push('walk()');
    const system = typingSystems[language] || 'Unknown';
    let text = `${engine.prefix} ${language} (${system}) — cannot execute in browser.\n`;
    text += used.length ? `Detected behaviors: ${used.join(', ')}` : 'No duck-like behaviors detected.';
    outputEl.textContent = text;
}

function copyCodeToClipboard() {
    const codeInput = document.getElementById('codeInput');
    if (!codeInput) return;
    codeInput.select();
    document.execCommand('copy');
}

function checkDuckTyping() {

    const objectName =
        document.getElementById('objectName').value.trim();

    const methods =
        document.getElementById('methods').value.toLowerCase();

    const language =
        document.getElementById('language').value;

    const output =
        document.getElementById('output');

    updateTypingInfo(language);
    output.style.display = 'block';

    if (!objectName || !methods) {

        output.className = 'result rejected';

        output.innerHTML = `
            <h3>⚠️ Missing Input</h3>
            <p>Please enter object name and methods.</p>
        `;

        return;
    }

    const hasQuack = methods.includes('quack');
    const hasWalk = methods.includes('walk');

    let status =
        hasQuack && hasWalk
        ? "ACCEPTED"
        : "REJECTED";

    let stackHTML = `
        <div class="stack-box">

            <h3>📚 Stack</h3>

            <div class="stack-item">
                ${language}
            </div>

            <div class="stack-arrow">
                ↓
            </div>

            <div class="stack-item">
                ${objectName}
            </div>

            <div class="stack-arrow">
                ↓
            </div>

            <div class="stack-item">
                ${methods}
            </div>

            <div class="stack-arrow">
                ↓
            </div>

            <div class="
                ${status === 'ACCEPTED'
                    ? 'stack-success'
                    : 'stack-failed'}
            ">
                ${status}
            </div>

        </div>
    `;

    if (hasQuack && hasWalk) {

        output.className = 'result accepted';

        const engineName = document.getElementById('aiEngine')?.value || 'Claude';
        const engine = aiEngines[engineName] || aiEngines.Claude;

        output.innerHTML = `
            <h3>${engine.prefix} ✅ ACCEPTED</h3>

            <p>
                <strong>${objectName}</strong>
                behaves like a duck in
                <strong>${language}</strong>.
            </p>

            ${stackHTML}
        `;
    }

    else {

        output.className = 'result rejected';

        const engineName = document.getElementById('aiEngine')?.value || 'Claude';
        const engine = aiEngines[engineName] || aiEngines.Claude;

        output.innerHTML = `
            <h3>${engine.prefix} ❌ REJECTED</h3>

            <p>
                <strong>${objectName}</strong>
                is not a duck in
                <strong>${language}</strong>.
            </p>

            ${stackHTML}
        `;
    }
}

function showFeature(name) {
    const details = document.getElementById('featureDetails');
    const feature = treeFeatures[name];

    if (!feature) {
        details.innerHTML = '<strong>Feature not found.</strong>';
        return;
    }

    details.innerHTML = `
        <h4>${feature.title}</h4>
        <p>${feature.description}</p>
        <p><em>${feature.example}</em></p>
    `;
}

function fillExample(type) {

    if (type === 'duck') {

        document.getElementById('objectName').value =
            'Duck Object';

        document.getElementById('methods').value =
            'quack, walk';

        document.getElementById('language').value =
            'Python';
    }

    else if (type === 'robot') {

        document.getElementById('objectName').value =
            'Robot Duck';

        document.getElementById('methods').value =
            'quack, walk';

        document.getElementById('language').value =
            'JavaScript';
    }

    else if (type === 'dog') {

        document.getElementById('objectName').value =
            'Dog';

        document.getElementById('methods').value =
            'bark, run';

        document.getElementById('language').value =
            'Java';
    }

    else if (type === 'person') {

        document.getElementById('objectName').value =
            'Person';

        document.getElementById('methods').value =
            'talk, walk';

        document.getElementById('language').value =
            'JavaScript';
    }

    updateTypingInfo(document.getElementById('language').value);
}

document.getElementById('language').addEventListener('change', function () {
    updateTypingInfo(this.value);
});

updateTypingInfo(document.getElementById('language').value);
// update when AI engine selection changes
const aiSelect = document.getElementById('aiEngine');
if (aiSelect) {
    aiSelect.addEventListener('change', function () {
        updateTypingInfo(document.getElementById('language').value);
    });
}