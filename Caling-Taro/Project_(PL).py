# ============================================================
# Lexical Analysis Simulator - Flask Web Application
# A single-file educational tool demonstrating lexical analysis
# ============================================================

# --- Standard Library Imports ---
import re  # For regex-based tokenization
import json  # For sending data as JSON between Python and JavaScript

# --- Flask Imports ---
from flask import Flask, render_template_string, request, jsonify

# --- Initialize Flask App ---
app = Flask(__name__)

# ============================================================
# LEXICAL ANALYSIS ENGINE
# This section handles the actual tokenization logic
# ============================================================

# Python keywords that the tokenizer should recognize
PYTHON_KEYWORDS = {
    'False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await',
    'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except',
    'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is',
    'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try',
    'while', 'with', 'yield', 'print', 'input', 'range', 'len', 'int',
    'float', 'str', 'list', 'dict', 'set', 'tuple', 'type', 'isinstance',
    'open', 'super', 'self'
}

# Token color mapping for the UI - each token type gets a distinct color
TOKEN_COLORS = {
    'KEYWORD':     '#f59e0b',   # Amber
    'IDENTIFIER':  '#60a5fa',   # Blue
    'NUMBER':      '#34d399',   # Green
    'OPERATOR':    '#f87171',   # Red
    'STRING':      '#a78bfa',   # Purple
    'PARENTHESIS': '#fb923c',   # Orange
    'DELIMITER':   '#e879f9',   # Pink/Magenta
    'COMMENT':     '#6b7280',   # Gray
    'WHITESPACE':  '#374151',   # Dark Gray (usually hidden)
    'UNKNOWN':     '#94a3b8',   # Slate
}

def tokenize_source_code(source_code):
    """
    Tokenizes the given source code string into a list of token dictionaries.

    Each token dictionary contains:
        - 'value': the actual text of the token
        - 'type':  the classified token type (e.g., KEYWORD, IDENTIFIER)
        - 'line':  the line number where the token appears

    Args:
        source_code (str): Raw source code entered by the user

    Returns:
        list: A list of token dictionaries
    """

    # List to collect all discovered tokens
    tokens = []

    # Define regex patterns for each token type.
    # Order matters: more specific patterns must come before general ones.
    token_patterns = [
        # Single-line comments (# ...) — must be before operators
        ('COMMENT',     r'#[^\n]*'),

        # Multi-line / triple-quoted strings (before single-quoted strings)
        ('STRING',      r'"""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\''),

        # Single-quoted and double-quoted strings
        ('STRING',      r'"(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\''),

        # Floating point and integer numbers
        ('NUMBER',      r'\b\d+\.\d*|\.\d+|\b\d+\b'),

        # Identifiers and keywords (letters, digits, underscores)
        ('IDENTIFIER',  r'\b[A-Za-z_][A-Za-z0-9_]*\b'),

        # Multi-character operators first (==, !=, <=, >=, **, //, ->, etc.)
        ('OPERATOR',    r'==|!=|<=|>=|\*\*|//|->|:=|\+=|-=|\*=|/=|%=|[+\-*/%=&|^~<>!]'),

        # Parentheses and brackets
        ('PARENTHESIS', r'[(){}\[\]]'),

        # Delimiters: comma, colon, semicolon, dot
        ('DELIMITER',   r'[,;:.]'),

        # Skip whitespace (spaces, tabs) — we still count lines separately
        ('WHITESPACE',  r'[ \t]+'),

        # Newline — used to increment line counter
        ('NEWLINE',     r'\n'),

        # Catch-all for any unrecognized characters
        ('UNKNOWN',     r'.'),
    ]

    # Combine all patterns into one master regex using named groups
    # Each group is named after its token type
    combined_pattern = '|'.join(
        f'(?P<{name}_{idx}>{pattern})'
        for idx, (name, pattern) in enumerate(token_patterns)
    )

    # Compile the combined regex for efficiency
    master_regex = re.compile(combined_pattern)

    # Track the current line number as we scan through the source
    current_line = 1

    # Iterate over every match found by the regex
    for match in master_regex.finditer(source_code):

        # Find which named group matched
        for idx, (token_type, _) in enumerate(token_patterns):
            group_name = f'{token_type}_{idx}'
            value = match.group(group_name)

            if value is not None:
                # We found the matching group

                if token_type == 'NEWLINE':
                    # Count new lines but don't add to token list
                    current_line += 1

                elif token_type == 'WHITESPACE':
                    # Skip plain whitespace tokens in the output
                    pass

                else:
                    # For IDENTIFIER tokens, check if they are actually keywords
                    if token_type == 'IDENTIFIER' and value in PYTHON_KEYWORDS:
                        token_type = 'KEYWORD'

                    # Add the token to our results list
                    tokens.append({
                        'value': value,
                        'type':  token_type,
                        'line':  current_line,
                        'color': TOKEN_COLORS.get(token_type, '#94a3b8')
                    })

                # Stop checking other groups once we've found the match
                break

    return tokens


# ============================================================
# HTML TEMPLATE
# The entire frontend is embedded here as a multi-line string
# ============================================================

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Lexical Analysis Simulator</title>

    <!-- Google Fonts: JetBrains Mono for code, Syne for headings, Inter for body -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;700&family=Syne:wght@400;600;700;800&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">

    <style>
        /* =============================================
           CSS CUSTOM PROPERTIES (Design Tokens)
           ============================================= */
        :root {
            --bg-void:        #020408;
            --bg-deep:        #060d16;
            --bg-surface:     #0a1628;
            --bg-raised:      #0f2040;
            --bg-card:        #112347;
            --border-dim:     rgba(99, 179, 237, 0.08);
            --border-glow:    rgba(99, 179, 237, 0.25);
            --accent-cyan:    #00d4ff;
            --accent-blue:    #3b82f6;
            --accent-violet:  #8b5cf6;
            --accent-amber:   #f59e0b;
            --text-primary:   #e2f0ff;
            --text-secondary: #7ea8cc;
            --text-muted:     #3d6080;
            --font-mono:      'JetBrains Mono', 'Fira Code', monospace;
            --font-display:   'Syne', sans-serif;
            --font-body:      'Inter', sans-serif;
            --radius-sm:      6px;
            --radius-md:      12px;
            --radius-lg:      20px;
            --shadow-glow:    0 0 40px rgba(0, 212, 255, 0.12);
            --shadow-deep:    0 20px 60px rgba(0, 0, 0, 0.6);
        }

        /* =============================================
           RESET & BASE
           ============================================= */
        *, *::before, *::after {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        html { scroll-behavior: smooth; }

        body {
            font-family: var(--font-body);
            background: var(--bg-void);
            color: var(--text-primary);
            min-height: 100vh;
            overflow-x: hidden;
            position: relative;
        }

        /* =============================================
           ANIMATED BACKGROUND
           ============================================= */
        .bg-canvas {
            position: fixed;
            inset: 0;
            z-index: 0;
            pointer-events: none;
            overflow: hidden;
        }

        /* Radial nebula blobs */
        .bg-blob {
            position: absolute;
            border-radius: 50%;
            filter: blur(120px);
            opacity: 0.15;
            animation: drift 20s ease-in-out infinite;
        }
        .bg-blob-1 {
            width: 700px; height: 700px;
            background: radial-gradient(circle, #0066cc, transparent);
            top: -200px; left: -200px;
            animation-delay: 0s;
        }
        .bg-blob-2 {
            width: 500px; height: 500px;
            background: radial-gradient(circle, #6600cc, transparent);
            bottom: -100px; right: -100px;
            animation-delay: -7s;
        }
        .bg-blob-3 {
            width: 400px; height: 400px;
            background: radial-gradient(circle, #00cccc, transparent);
            top: 40%; left: 50%;
            animation-delay: -14s;
        }

        /* Subtle grid overlay */
        .bg-grid {
            position: absolute;
            inset: 0;
            background-image:
                linear-gradient(rgba(0, 212, 255, 0.03) 1px, transparent 1px),
                linear-gradient(90deg, rgba(0, 212, 255, 0.03) 1px, transparent 1px);
            background-size: 60px 60px;
        }

        /* Scanline effect */
        .bg-scanlines {
            position: absolute;
            inset: 0;
            background: repeating-linear-gradient(
                0deg,
                transparent,
                transparent 3px,
                rgba(0, 0, 0, 0.08) 3px,
                rgba(0, 0, 0, 0.08) 4px
            );
        }

        @keyframes drift {
            0%, 100% { transform: translate(0, 0) scale(1); }
            33%       { transform: translate(60px, -40px) scale(1.1); }
            66%       { transform: translate(-40px, 60px) scale(0.95); }
        }

        /* Floating code particles */
        .particles-container {
            position: absolute;
            inset: 0;
            overflow: hidden;
        }
        .particle {
            position: absolute;
            font-family: var(--font-mono);
            font-size: 11px;
            color: rgba(0, 212, 255, 0.12);
            animation: float-up linear infinite;
            white-space: nowrap;
            pointer-events: none;
        }
        @keyframes float-up {
            0%   { transform: translateY(100vh) rotate(0deg); opacity: 0; }
            10%  { opacity: 1; }
            90%  { opacity: 0.8; }
            100% { transform: translateY(-100px) rotate(20deg); opacity: 0; }
        }

        /* =============================================
           LAYOUT WRAPPER
           ============================================= */
        .app-wrapper {
            position: relative;
            z-index: 1;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }

        /* =============================================
           NAVIGATION BAR
           ============================================= */
        .navbar {
            position: sticky;
            top: 0;
            z-index: 100;
            background: rgba(6, 13, 22, 0.85);
            backdrop-filter: blur(20px) saturate(180%);
            -webkit-backdrop-filter: blur(20px) saturate(180%);
            border-bottom: 1px solid var(--border-dim);
            padding: 0 2rem;
            height: 70px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .navbar-brand {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .brand-icon {
            width: 38px;
            height: 38px;
            background: linear-gradient(135deg, var(--accent-cyan), var(--accent-violet));
            border-radius: var(--radius-sm);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
            box-shadow: 0 0 20px rgba(0, 212, 255, 0.3);
            animation: icon-pulse 3s ease-in-out infinite;
        }
        @keyframes icon-pulse {
            0%, 100% { box-shadow: 0 0 20px rgba(0, 212, 255, 0.3); }
            50%       { box-shadow: 0 0 35px rgba(0, 212, 255, 0.6); }
        }

        .brand-text {
            font-family: var(--font-display);
            font-size: 1.1rem;
            font-weight: 700;
            letter-spacing: -0.02em;
            background: linear-gradient(90deg, var(--accent-cyan), #a78bfa);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .nav-badge {
            font-family: var(--font-mono);
            font-size: 0.65rem;
            font-weight: 500;
            letter-spacing: 0.08em;
            padding: 3px 10px;
            border: 1px solid rgba(0, 212, 255, 0.3);
            border-radius: 100px;
            color: var(--accent-cyan);
            background: rgba(0, 212, 255, 0.06);
        }

        /* =============================================
           MAIN CONTENT
           ============================================= */
        .main-content {
            flex: 1;
            max-width: 1280px;
            width: 100%;
            margin: 0 auto;
            padding: 3rem 2rem 4rem;
        }

        /* =============================================
           HERO SECTION
           ============================================= */
        .hero {
            text-align: center;
            margin-bottom: 3rem;
            animation: fade-down 0.8s ease both;
        }
        @keyframes fade-down {
            from { opacity: 0; transform: translateY(-30px); }
            to   { opacity: 1; transform: translateY(0); }
        }

        .hero-eyebrow {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            font-family: var(--font-mono);
            font-size: 0.72rem;
            letter-spacing: 0.15em;
            text-transform: uppercase;
            color: var(--accent-cyan);
            background: rgba(0, 212, 255, 0.06);
            border: 1px solid rgba(0, 212, 255, 0.2);
            padding: 6px 16px;
            border-radius: 100px;
            margin-bottom: 1.5rem;
        }
        .hero-eyebrow::before {
            content: '';
            width: 6px; height: 6px;
            background: var(--accent-cyan);
            border-radius: 50%;
            animation: blink 1.5s ease-in-out infinite;
        }
        @keyframes blink {
            0%, 100% { opacity: 1; } 50% { opacity: 0.2; }
        }

        .hero-title {
            font-family: var(--font-display);
            font-size: clamp(2rem, 5vw, 3.5rem);
            font-weight: 800;
            letter-spacing: -0.04em;
            line-height: 1.1;
            margin-bottom: 1rem;
        }
        .hero-title .line-1 { color: var(--text-primary); }
        .hero-title .line-2 {
            background: linear-gradient(90deg, var(--accent-cyan) 0%, var(--accent-violet) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .hero-desc {
            max-width: 600px;
            margin: 0 auto;
            font-size: 1rem;
            line-height: 1.7;
            color: var(--text-secondary);
            font-weight: 300;
        }

        /* =============================================
           EDUCATIONAL EXPLAINER CARD
           ============================================= */
        .explainer-card {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1px;
            background: var(--border-dim);
            border: 1px solid var(--border-dim);
            border-radius: var(--radius-lg);
            overflow: hidden;
            margin-bottom: 2.5rem;
            animation: fade-up 0.8s ease 0.2s both;
        }
        @keyframes fade-up {
            from { opacity: 0; transform: translateY(20px); }
            to   { opacity: 1; transform: translateY(0); }
        }

        .explainer-item {
            background: var(--bg-surface);
            padding: 1.5rem 1.75rem;
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
            transition: background 0.3s;
        }
        .explainer-item:hover { background: var(--bg-raised); }

        .explainer-step {
            font-family: var(--font-mono);
            font-size: 0.65rem;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            color: var(--accent-cyan);
            opacity: 0.7;
        }
        .explainer-title {
            font-family: var(--font-display);
            font-size: 1rem;
            font-weight: 700;
            color: var(--text-primary);
        }
        .explainer-body {
            font-size: 0.82rem;
            color: var(--text-secondary);
            line-height: 1.6;
        }

        /* =============================================
           EDITOR SECTION
           ============================================= */
        .editor-section {
            display: grid;
            grid-template-columns: 1fr;
            gap: 1.5rem;
            margin-bottom: 2rem;
            animation: fade-up 0.8s ease 0.4s both;
        }

        .panel {
            background: var(--bg-surface);
            border: 1px solid var(--border-dim);
            border-radius: var(--radius-lg);
            overflow: hidden;
            transition: border-color 0.3s, box-shadow 0.3s;
        }
        .panel:hover {
            border-color: var(--border-glow);
            box-shadow: var(--shadow-glow);
        }

        .panel-header {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 1rem 1.5rem;
            border-bottom: 1px solid var(--border-dim);
            background: rgba(0, 0, 0, 0.2);
        }

        /* macOS-style traffic light dots */
        .dot-group { display: flex; gap: 6px; }
        .dot {
            width: 11px; height: 11px;
            border-radius: 50%;
        }
        .dot-red    { background: #ff5f56; }
        .dot-yellow { background: #ffbd2e; }
        .dot-green  { background: #27c93f; }

        .panel-title {
            font-family: var(--font-mono);
            font-size: 0.75rem;
            letter-spacing: 0.06em;
            color: var(--text-secondary);
            margin-left: 4px;
        }

        .panel-lang-badge {
            margin-left: auto;
            font-family: var(--font-mono);
            font-size: 0.65rem;
            padding: 2px 10px;
            background: rgba(0, 212, 255, 0.08);
            border: 1px solid rgba(0, 212, 255, 0.15);
            border-radius: 100px;
            color: var(--accent-cyan);
        }

        /* Code Textarea */
        #code-input {
            width: 100%;
            min-height: 220px;
            background: transparent;
            border: none;
            outline: none;
            resize: vertical;
            font-family: var(--font-mono);
            font-size: 0.9rem;
            line-height: 1.75;
            color: var(--text-primary);
            padding: 1.5rem;
            caret-color: var(--accent-cyan);
        }
        #code-input::placeholder {
            color: var(--text-muted);
            opacity: 0.7;
        }
        #code-input:focus {
            box-shadow: inset 0 0 0 1px rgba(0, 212, 255, 0.15);
        }

        /* Line Numbers Decoration */
        .editor-body {
            display: flex;
        }
        .line-numbers {
            padding: 1.5rem 0.75rem 1.5rem 1.25rem;
            font-family: var(--font-mono);
            font-size: 0.9rem;
            line-height: 1.75;
            color: var(--text-muted);
            text-align: right;
            user-select: none;
            min-width: 48px;
            border-right: 1px solid var(--border-dim);
        }

        /* =============================================
           BUTTON BAR
           ============================================= */
        .button-bar {
            display: flex;
            gap: 1rem;
            flex-wrap: wrap;
            animation: fade-up 0.8s ease 0.5s both;
        }

        .btn {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 0.75rem 1.75rem;
            border-radius: var(--radius-md);
            font-family: var(--font-body);
            font-size: 0.9rem;
            font-weight: 600;
            cursor: pointer;
            border: none;
            outline: none;
            transition: all 0.25s ease;
            position: relative;
            overflow: hidden;
        }
        .btn::after {
            content: '';
            position: absolute;
            inset: 0;
            background: white;
            opacity: 0;
            transition: opacity 0.2s;
        }
        .btn:active::after { opacity: 0.08; }

        .btn-primary {
            background: linear-gradient(135deg, var(--accent-cyan), var(--accent-blue));
            color: #001824;
            box-shadow: 0 4px 20px rgba(0, 212, 255, 0.25);
        }
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 30px rgba(0, 212, 255, 0.4);
        }

        .btn-secondary {
            background: var(--bg-raised);
            color: var(--text-secondary);
            border: 1px solid var(--border-dim);
        }
        .btn-secondary:hover {
            border-color: var(--border-glow);
            color: var(--text-primary);
            transform: translateY(-2px);
        }

        /* =============================================
           LOADING INDICATOR
           ============================================= */
        .loading-bar {
            display: none;
            height: 3px;
            background: var(--bg-void);
            border-radius: 100px;
            overflow: hidden;
            margin-top: 1rem;
        }
        .loading-bar.active { display: block; }
        .loading-bar-fill {
            height: 100%;
            background: linear-gradient(90deg, var(--accent-cyan), var(--accent-violet), var(--accent-cyan));
            background-size: 200% 100%;
            animation: shimmer 1.2s linear infinite;
        }
        @keyframes shimmer {
            0%   { background-position: 200% 0; }
            100% { background-position: -200% 0; }
        }

        /* =============================================
           STATS ROW
           ============================================= */
        .stats-row {
            display: none;
            grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
            gap: 1rem;
            margin-bottom: 1.5rem;
            animation: fade-up 0.5s ease both;
        }
        .stats-row.visible { display: grid; }

        .stat-card {
            background: var(--bg-surface);
            border: 1px solid var(--border-dim);
            border-radius: var(--radius-md);
            padding: 1.1rem 1.25rem;
            transition: all 0.3s;
        }
        .stat-card:hover {
            border-color: var(--border-glow);
            box-shadow: 0 0 20px rgba(0, 212, 255, 0.08);
            transform: translateY(-2px);
        }
        .stat-value {
            font-family: var(--font-display);
            font-size: 1.8rem;
            font-weight: 800;
            color: var(--accent-cyan);
            line-height: 1;
        }
        .stat-label {
            font-size: 0.75rem;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-top: 4px;
        }

        /* =============================================
           RESULTS TABLE
           ============================================= */
        .results-section {
            display: none;
            animation: fade-up 0.5s ease both;
        }
        .results-section.visible { display: block; }

        .results-panel {
            background: var(--bg-surface);
            border: 1px solid var(--border-dim);
            border-radius: var(--radius-lg);
            overflow: hidden;
        }

        .results-panel:hover {
            border-color: var(--border-glow);
            box-shadow: var(--shadow-glow);
        }

        .token-table-wrap {
            overflow-x: auto;
        }

        .token-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.875rem;
        }

        .token-table thead th {
            padding: 1rem 1.5rem;
            text-align: left;
            font-family: var(--font-mono);
            font-size: 0.68rem;
            font-weight: 500;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            color: var(--text-muted);
            border-bottom: 1px solid var(--border-dim);
            background: rgba(0, 0, 0, 0.2);
            position: sticky;
            top: 0;
        }

        .token-row {
            border-bottom: 1px solid rgba(255,255,255,0.02);
            transition: background 0.2s;
            animation: row-reveal 0.4s ease both;
        }
        .token-row:last-child { border-bottom: none; }
        .token-row:hover { background: rgba(0, 212, 255, 0.04); }

        @keyframes row-reveal {
            from { opacity: 0; transform: translateX(-12px); }
            to   { opacity: 1; transform: translateX(0); }
        }

        .token-row td {
            padding: 0.8rem 1.5rem;
            vertical-align: middle;
        }

        /* Row number */
        .td-index {
            font-family: var(--font-mono);
            font-size: 0.7rem;
            color: var(--text-muted);
            width: 50px;
        }

        /* Token value */
        .td-value {
            font-family: var(--font-mono);
            font-size: 0.875rem;
        }
        .token-value-pill {
            display: inline-block;
            padding: 2px 10px;
            border-radius: 4px;
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(255,255,255,0.06);
        }

        /* Token type badge */
        .token-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 3px 12px;
            border-radius: 100px;
            font-family: var(--font-mono);
            font-size: 0.7rem;
            font-weight: 500;
            letter-spacing: 0.04em;
        }
        .token-badge::before {
            content: '';
            width: 6px; height: 6px;
            border-radius: 50%;
            background: currentColor;
        }

        /* Line number */
        .td-line {
            font-family: var(--font-mono);
            font-size: 0.75rem;
            color: var(--text-muted);
        }
        .line-pill {
            display: inline-block;
            padding: 2px 8px;
            background: var(--bg-raised);
            border-radius: 4px;
            border: 1px solid var(--border-dim);
        }

        /* Empty state */
        .empty-state {
            text-align: center;
            padding: 4rem 2rem;
            color: var(--text-muted);
        }
        .empty-state-icon { font-size: 3rem; margin-bottom: 1rem; }
        .empty-state-text { font-size: 0.9rem; }

        /* =============================================
           TOKEN LEGEND
           ============================================= */
        .legend-section {
            margin-top: 1.5rem;
            animation: fade-up 0.8s ease 0.6s both;
        }
        .legend-title {
            font-family: var(--font-mono);
            font-size: 0.68rem;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            color: var(--text-muted);
            margin-bottom: 0.75rem;
        }
        .legend-grid {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
        }
        .legend-item {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 4px 12px;
            border-radius: 100px;
            font-family: var(--font-mono);
            font-size: 0.68rem;
            border: 1px solid;
            cursor: default;
            transition: all 0.2s;
        }
        .legend-item:hover { transform: translateY(-2px); }
        .legend-dot {
            width: 7px; height: 7px;
            border-radius: 50%;
        }

        /* =============================================
           FOOTER
           ============================================= */
        .footer {
            border-top: 1px solid var(--border-dim);
            padding: 2rem;
            text-align: center;
            background: rgba(0,0,0,0.2);
        }
        .footer-text {
            font-size: 0.8rem;
            color: var(--text-muted);
            line-height: 1.7;
            max-width: 700px;
            margin: 0 auto;
        }
        .footer-text strong {
            color: var(--text-secondary);
            font-weight: 500;
        }
        .footer-phases {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 0.5rem;
            flex-wrap: wrap;
            margin-top: 1rem;
            font-family: var(--font-mono);
            font-size: 0.68rem;
            color: var(--text-muted);
        }
        .phase-item {
            padding: 3px 10px;
            border: 1px solid var(--border-dim);
            border-radius: 100px;
        }
        .phase-item.active {
            border-color: var(--accent-cyan);
            color: var(--accent-cyan);
            background: rgba(0, 212, 255, 0.06);
        }
        .phase-arrow { opacity: 0.3; }

        /* =============================================
           RESPONSIVE
           ============================================= */
        @media (max-width: 640px) {
            .navbar { padding: 0 1rem; }
            .main-content { padding: 2rem 1rem 3rem; }
            .hero-desc { font-size: 0.9rem; }
            .token-row td { padding: 0.7rem 1rem; }
            .btn { padding: 0.7rem 1.25rem; font-size: 0.85rem; }
        }

        /* =============================================
           UTILITY
           ============================================= */
        .sr-only {
            position: absolute; width: 1px; height: 1px;
            padding: 0; margin: -1px; overflow: hidden;
            clip: rect(0,0,0,0); white-space: nowrap; border: 0;
        }
    </style>
</head>

<body>
    <!-- Animated Background -->
    <div class="bg-canvas" aria-hidden="true">
        <div class="bg-blob bg-blob-1"></div>
        <div class="bg-blob bg-blob-2"></div>
        <div class="bg-blob bg-blob-3"></div>
        <div class="bg-grid"></div>
        <div class="bg-scanlines"></div>
        <div class="particles-container" id="particles"></div>
    </div>

    <!-- App Shell -->
    <div class="app-wrapper">

        <!-- Navigation Bar -->
        <nav class="navbar">
            <div class="navbar-brand">
                <div class="brand-icon">⚙</div>
                <span class="brand-text">Lexical Analysis Simulator</span>
            </div>
            <span class="nav-badge">Phase I · Compiler Theory</span>
        </nav>

        <!-- Main Content -->
        <main class="main-content">

            <!-- Hero Section -->
            <header class="hero">
                <div class="hero-eyebrow">Language Translation Process</div>
                <h1 class="hero-title">
                    <div class="line-1">Source Code</div>
                    <div class="line-2">Token by Token</div>
                </h1>
                <p class="hero-desc">
                    Lexical analysis is the first phase of the language translation process.
                    Enter any source code below and watch it get broken down into classified tokens in real time.
                </p>
            </header>

            <!-- Educational Explainer -->
            <div class="explainer-card" role="region" aria-label="How lexical analysis works">
                <div class="explainer-item">
                    <div class="explainer-step">Step 01</div>
                    <div class="explainer-title">Source Code Input</div>
                    <div class="explainer-body">Raw program text is fed into the lexical analyser character by character.</div>
                </div>
                <div class="explainer-item">
                    <div class="explainer-step">Step 02</div>
                    <div class="explainer-title">Pattern Matching</div>
                    <div class="explainer-body">Regex patterns scan the input, grouping characters into meaningful sequences called lexemes.</div>
                </div>
                <div class="explainer-item">
                    <div class="explainer-step">Step 03</div>
                    <div class="explainer-title">Token Classification</div>
                    <div class="explainer-body">Each lexeme is labelled with a token type: KEYWORD, IDENTIFIER, OPERATOR, and so on.</div>
                </div>
                <div class="explainer-item">
                    <div class="explainer-step">Step 04</div>
                    <div class="explainer-title">Token Stream Output</div>
                    <div class="explainer-body">The resulting token stream is passed to the parser for the next phase of compilation.</div>
                </div>
            </div>

            <!-- Code Editor Panel -->
            <div class="editor-section">
                <div class="panel">
                    <div class="panel-header">
                        <div class="dot-group" aria-hidden="true">
                            <div class="dot dot-red"></div>
                            <div class="dot dot-yellow"></div>
                            <div class="dot dot-green"></div>
                        </div>
                        <span class="panel-title">source_input.py</span>
                        <span class="panel-lang-badge">Python</span>
                    </div>
                    <div class="editor-body">
                        <div class="line-numbers" id="line-numbers" aria-hidden="true">1</div>
                        <textarea
                            id="code-input"
                            spellcheck="false"
                            autocomplete="off"
                            autocorrect="off"
                            autocapitalize="off"
                            aria-label="Source code input"
                            placeholder="# Enter your source code here...
a = 5 + 3
print(a)"
                        ></textarea>
                    </div>
                </div>
            </div>

            <!-- Button Bar -->
            <div class="button-bar">
                <button class="btn btn-primary" id="analyze-btn" onclick="analyzeTokens()">
                    <span>▶</span> Analyze Tokens
                </button>
                <button class="btn btn-secondary" id="clear-btn" onclick="clearOutput()">
                    <span>✕</span> Clear Output
                </button>
            </div>

            <!-- Loading Bar -->
            <div class="loading-bar" id="loading-bar" role="status" aria-live="polite">
                <div class="loading-bar-fill"></div>
            </div>

            <!-- Stats Row (shown after analysis) -->
            <div class="stats-row" id="stats-row" style="margin-top:2rem">
                <div class="stat-card">
                    <div class="stat-value" id="stat-total">0</div>
                    <div class="stat-label">Total Tokens</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value" id="stat-lines">0</div>
                    <div class="stat-label">Lines Scanned</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value" id="stat-keywords">0</div>
                    <div class="stat-label">Keywords</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value" id="stat-identifiers">0</div>
                    <div class="stat-label">Identifiers</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value" id="stat-operators">0</div>
                    <div class="stat-label">Operators</div>
                </div>
            </div>

            <!-- Token Results Table -->
            <div class="results-section" id="results-section" style="margin-top:1.5rem">
                <div class="results-panel">
                    <div class="panel-header">
                        <div class="dot-group" aria-hidden="true">
                            <div class="dot dot-red"></div>
                            <div class="dot dot-yellow"></div>
                            <div class="dot dot-green"></div>
                        </div>
                        <span class="panel-title">token_stream.out</span>
                        <span class="panel-lang-badge" id="results-count-badge">0 tokens</span>
                    </div>
                    <div class="token-table-wrap">
                        <table class="token-table" id="token-table" aria-label="Token analysis results">
                            <thead>
                                <tr>
                                    <th>TOKEN ID</th>
                                    <th>Token Value</th>
                                    <th>Token Type</th>
                                    <th>Line</th>
                                </tr>
                            </thead>
                            <tbody id="token-tbody">
                                <!-- Rows inserted by JavaScript -->
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <!-- Token Type Legend -->
            <div class="legend-section">
                <div class="legend-title">Token Type Legend</div>
                <div class="legend-grid" id="legend-grid">
                    <!-- Populated by JavaScript -->
                </div>
            </div>

        </main>

        <!-- Footer -->
        <footer class="footer">
            <p class="footer-text">
                <strong>Lexical Analysis</strong> — also called <em>scanning</em> or <em>tokenization</em> — is the very
                first phase of the language translation process. A <strong>lexer</strong> (or lexical analyser) reads the
                raw character stream of source code and groups characters into meaningful units called
                <strong>tokens</strong>. Each token has a <em>type</em> (its grammatical role) and a <em>value</em>
                (the actual text). The resulting <strong>token stream</strong> is then passed to the
                <strong>parser</strong> for syntactic analysis.
            </p>
            <div class="footer-phases" aria-label="Compiler phases">
                <span class="phase-item active">Lexical Analysis</span>
                <span class="phase-arrow">→</span>
                <span class="phase-item">Syntax Analysis</span>
                <span class="phase-arrow">→</span>
                <span class="phase-item">Semantic Analysis</span>
                <span class="phase-arrow">→</span>
                <span class="phase-item">Intermediate Code</span>
                <span class="phase-arrow">→</span>
                <span class="phase-item">Code Optimisation</span>
                <span class="phase-arrow">→</span>
                <span class="phase-item">Code Generation</span>
            </div>
        </footer>

    </div><!-- /.app-wrapper -->

    <!-- ================================================
         JAVASCRIPT
         ================================================ -->
    <script>
        // -----------------------------------------------
        // Token type → display colour mapping
        // (must mirror TOKEN_COLORS in Python)
        // -----------------------------------------------
        const TOKEN_COLORS = {
            KEYWORD:     '#f59e0b',
            IDENTIFIER:  '#60a5fa',
            NUMBER:      '#34d399',
            OPERATOR:    '#f87171',
            STRING:      '#a78bfa',
            PARENTHESIS: '#fb923c',
            DELIMITER:   '#e879f9',
            COMMENT:     '#6b7280',
            WHITESPACE:  '#374151',
            UNKNOWN:     '#94a3b8',
        };

        // Build the legend once on page load
        (function buildLegend() {
            const grid = document.getElementById('legend-grid');
            Object.entries(TOKEN_COLORS).forEach(([type, color]) => {
                if (type === 'WHITESPACE') return; // hide whitespace
                const item = document.createElement('div');
                item.className = 'legend-item';
                item.style.color = color;
                item.style.borderColor = color + '33';
                item.style.background   = color + '11';
                item.innerHTML = `<span class="legend-dot" style="background:${color}"></span>${type}`;
                grid.appendChild(item);
            });
        })();

        // -----------------------------------------------
        // Line-number sync for the textarea
        // -----------------------------------------------
        const codeInput   = document.getElementById('code-input');
        const lineNumbers = document.getElementById('line-numbers');

        function updateLineNumbers() {
            const lines = codeInput.value.split('\\n').length;
            lineNumbers.innerHTML = Array.from({length: lines}, (_, i) => i + 1).join('<br>');
        }

        codeInput.addEventListener('input', updateLineNumbers);
        codeInput.addEventListener('keydown', function(e) {
            // Allow Tab key to insert spaces instead of moving focus
            if (e.key === 'Tab') {
                e.preventDefault();
                const start = this.selectionStart;
                const end   = this.selectionEnd;
                this.value = this.value.substring(0, start) + '    ' + this.value.substring(end);
                this.selectionStart = this.selectionEnd = start + 4;
                updateLineNumbers();
            }
        });

        // Initialise line numbers on load
        updateLineNumbers();

        // -----------------------------------------------
        // Floating code particles
        // -----------------------------------------------
        const PARTICLE_CHARS = [
            'TOKEN', 'LEXER', '<ID>', '<OP>',
            'def', 'if', 'for', '==', '+=', '()',
            '0x1F', '//comment', 'int', 'str',
            'KEYWORD', 'NUM', '→', '⚙', '01101', '{}',
        ];

        function spawnParticle() {
            const container = document.getElementById('particles');
            const el        = document.createElement('span');
            el.className    = 'particle';
            el.textContent  = PARTICLE_CHARS[Math.floor(Math.random() * PARTICLE_CHARS.length)];
            el.style.left   = Math.random() * 100 + 'vw';
            el.style.animationDuration  = (12 + Math.random() * 20) + 's';
            el.style.animationDelay     = (Math.random() * 5) + 's';
            el.style.fontSize           = (9 + Math.random() * 6) + 'px';
            container.appendChild(el);
            // Remove particle once its animation ends to avoid DOM bloat
            el.addEventListener('animationend', () => el.remove());
        }

        // Spawn an initial batch and then periodically add more
        for (let i = 0; i < 18; i++) spawnParticle();
        setInterval(spawnParticle, 2500);

        // -----------------------------------------------
        // CORE: Analyze Tokens
        // -----------------------------------------------
        async function analyzeTokens() {
            const code = codeInput.value.trim();

            // Guard: do nothing if the textarea is empty
            if (!code) {
                flashError('Please enter some source code first.');
                return;
            }

            // Show loading state
            setLoading(true);

            try {
                // POST the code to the Flask backend
                const response = await fetch('/analyze', {
                    method:  'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body:    JSON.stringify({ code: code }),
                });

                if (!response.ok) {
                    throw new Error(`Server error: ${response.status}`);
                }

                const data = await response.json();

                if (data.error) {
                    throw new Error(data.error);
                }

                // Render results
                renderResults(data.tokens);

            } catch (err) {
                flashError('Analysis failed: ' + err.message);
            } finally {
                setLoading(false);
            }
        }

        // -----------------------------------------------
        // Render token table and stats
        // -----------------------------------------------
        function renderResults(tokens) {
            const tbody = document.getElementById('token-tbody');
            tbody.innerHTML = ''; // Clear previous results

            // Stats counters
            let keywords    = 0;
            let identifiers = 0;
            let operators   = 0;
            let maxLine     = 0;

            if (tokens.length === 0) {
                // Empty state — no tokens found
                tbody.innerHTML = `
                    <tr><td colspan="4">
                        <div class="empty-state">
                            <div class="empty-state-icon">🔍</div>
                            <div class="empty-state-text">No tokens detected in the input.</div>
                        </div>
                    </td></tr>`;
            } else {
                // Build each table row with a staggered animation delay
                const tokenTypeNumbers = {};
                let nextNumber = 1;

                tokens.forEach((token, index) => {

                    // Give the same number to the same token type
                    if (!(token.type in tokenTypeNumbers)) {
                        tokenTypeNumbers[token.type] = nextNumber++;
                    }

                    if (token.type === 'KEYWORD') keywords++;
                    if (token.type === 'IDENTIFIER') identifiers++;
                    if (token.type === 'OPERATOR') operators++;
                    if (token.line > maxLine) maxLine = token.line;

                    const color = TOKEN_COLORS[token.type] || '#94a3b8';
                    const delay = Math.min(index * 30, 800); // Cap max delay

                    // Escape HTML special characters in token value for safety
                    const safeValue = escapeHtml(token.value);

                    const tr = document.createElement('tr');
                    tr.className = 'token-row';
                    tr.style.animationDelay = delay + 'ms';
                    tr.innerHTML = `
                        <td class="td-index">${tokenTypeNumbers[token.type]}</td>
                        <td class="td-value">
                            <span class="token-value-pill" style="color:${color}">${safeValue}</span>
                        </td>
                        <td>
                            <span class="token-badge"
                                  style="color:${color}; background:${color}18; border:1px solid ${color}33">
                                ${token.type}
                            </span>
                        </td>
                        <td class="td-line">
                            <span class="line-pill">L${token.line}</span>
                        </td>
                    `;
                    tbody.appendChild(tr);
                });

                // Update stats
                document.getElementById('stat-total').textContent      = tokens.length;
                document.getElementById('stat-lines').textContent      = maxLine;
                document.getElementById('stat-keywords').textContent   = keywords;
                document.getElementById('stat-identifiers').textContent = identifiers;
                document.getElementById('stat-operators').textContent  = operators;
                document.getElementById('results-count-badge').textContent = `${tokens.length} token${tokens.length !== 1 ? 's' : ''}`;
            }

            // Show the results and stats
            document.getElementById('stats-row').classList.add('visible');
            document.getElementById('results-section').classList.add('visible');

            // Smooth scroll to results
            document.getElementById('results-section').scrollIntoView({ behavior: 'smooth', block: 'start' });
        }

        // -----------------------------------------------
        // Clear everything
        // -----------------------------------------------
        function clearOutput() {
            document.getElementById('token-tbody').innerHTML = '';
            document.getElementById('stats-row').classList.remove('visible');
            document.getElementById('results-section').classList.remove('visible');
            codeInput.value = '';
            updateLineNumbers();
            codeInput.focus();
        }

        // -----------------------------------------------
        // Loading state toggle
        // -----------------------------------------------
        function setLoading(active) {
            const bar = document.getElementById('loading-bar');
            const btn = document.getElementById('analyze-btn');
            if (active) {
                bar.classList.add('active');
                btn.disabled   = true;
                btn.innerHTML  = '<span>⏳</span> Analyzing…';
            } else {
                bar.classList.remove('active');
                btn.disabled   = false;
                btn.innerHTML  = '<span>▶</span> Analyze Tokens';
            }
        }

        // -----------------------------------------------
        // Flash a temporary error message
        // -----------------------------------------------
        function flashError(msg) {
            const existing = document.getElementById('error-flash');
            if (existing) existing.remove();

            const div = document.createElement('div');
            div.id = 'error-flash';
            div.style.cssText = `
                position:fixed; bottom:2rem; left:50%; transform:translateX(-50%);
                background:#7f1d1d; color:#fca5a5; border:1px solid #dc2626;
                padding:0.8rem 1.5rem; border-radius:10px; font-size:0.85rem;
                z-index:999; box-shadow:0 8px 30px rgba(0,0,0,0.5);
                animation:fade-down 0.3s ease;
            `;
            div.textContent = msg;
            document.body.appendChild(div);
            setTimeout(() => div.remove(), 4000);
        }

        // -----------------------------------------------
        // HTML escape helper (prevents XSS)
        // -----------------------------------------------
        function escapeHtml(str) {
            const map = { '&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;', "'":'&#039;' };
            return String(str).replace(/[&<>"']/g, m => map[m]);
        }

        // -----------------------------------------------
        // Keyboard shortcut: Ctrl+Enter to analyze
        // -----------------------------------------------
        document.addEventListener('keydown', function(e) {
            if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
                analyzeTokens();
            }
        });
    </script>
</body>
</html>
"""


# ============================================================
# FLASK ROUTES
# ============================================================

@app.route('/')
def index():
    """
    Root route — serves the main HTML page.
    Uses render_template_string() so no separate templates folder is needed.
    """
    return render_template_string(HTML_TEMPLATE)


@app.route('/analyze', methods=['POST'])
def analyze():
    """
    API endpoint that receives source code and returns a list of tokens as JSON.

    Expects a JSON body: { "code": "<source code string>" }
    Returns a JSON body: { "tokens": [ { "value": ..., "type": ..., "line": ... }, ... ] }
    """
    try:
        # Parse the incoming JSON request body
        data = request.get_json(force=True, silent=True)

        # Validate that we actually received data and a code key
        if not data or 'code' not in data:
            return jsonify({'error': 'No source code provided.'}), 400

        source_code = data['code']

        # Ensure the code is a non-empty string
        if not isinstance(source_code, str) or not source_code.strip():
            return jsonify({'error': 'Source code must be a non-empty string.'}), 400

        # Run the lexical analyser
        tokens = tokenize_source_code(source_code)

        # Return the tokens as JSON
        return jsonify({'tokens': tokens})

    except Exception as e:
        # Catch any unexpected errors and return a helpful message
        return jsonify({'error': f'Internal error during analysis: {str(e)}'}), 500


# ============================================================
# ENTRY POINT
# Run the Flask development server when executed directly
# ============================================================
if __name__ == '__main__':
    print("=" * 55)
    print("  Lexical Analysis Simulator")
    print("  Starting Flask development server...")
    print("  Open your browser at: http://127.0.0.1:5000")
    print("=" * 55)
    # debug=True shows helpful error messages during development
    app.run(host="127.0.0.1", port=8080, debug=False, use_reloader=False)