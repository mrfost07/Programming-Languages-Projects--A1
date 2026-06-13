import streamlit as st
import time
import random

# --- PAGE SETTINGS ---
st.set_page_config(page_title="Interactive Quiz Generator PL", page_icon="🎯", layout="centered")

# --- INITIALIZE SYSTEM STATES ---
if "pipeline_stage" not in st.session_state:
    st.session_state.pipeline_stage = "idle"  # idle, processing, active, summary
if "quiz_questions" not in st.session_state:
    st.session_state.quiz_questions = []
if "current_q_index" not in st.session_state:
    st.session_state.current_q_index = 0
if "user_score" not in st.session_state:
    st.session_state.user_score = 0
if "selected_answers" not in st.session_state:
    st.session_state.selected_answers = {}
if "has_answered" not in st.session_state:
    st.session_state.has_answered = False
if "start_time" not in st.session_state:
    st.session_state.start_time = 0
if "history" not in st.session_state:
    st.session_state.history = []
if "quiz_length_setting" not in st.session_state:
    st.session_state.quiz_length_setting = 30

# --- THEME SELECTION INTERFACE ---
st.sidebar.header("🎨 Interface Theme Customization")
theme_choice = st.sidebar.selectbox("Choose Application Theme:", ["Light Mode ☀️", "Dark Mode 🌙"])

# --- UNIVERSAL SIDEBAR STYLING (Always Dark Blue/Black) ---
# Enforces dark mode styling on the sidebar items to protect visibility when main panel goes light.
st.markdown("""
    <style>
    /* Darken Sidebar Panel Background */
    [data-testid="stSidebar"] { 
        background-color: #0b1329 !important; 
        border-right: 1px solid #1e293b !important; 
    }
    
    /* Enforce High Contrast White Text for all Sidebar Header Labels and Texts */
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, 
    [data-testid="stSidebar"] h4, [data-testid="stSidebar"] h5, [data-testid="stSidebar"] h6,
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stMarkdown { 
        color: #ffffff !important; 
    }
    
    /* FIX 1: Fix Selectbox Font Colors inside the Sidebar */
    [data-testid="stSidebar"] div[data-baseweb="select"] div {
        color: #0f172a !important; /* Makes selected text option crisp dark charcoal inside the white box */
        font-weight: 500 !important;
    }
    
    /* FIX 2: Clear White Contrast Text override for the Red Primary Action Button */
    [data-testid="stSidebar"] div.stButton > button[data-testid="baseButton-primary"] p {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    /* FIX 3: Crisp Dark Text configuration for the white Reset Application Secondary Button */
    [data-testid="stSidebar"] div.stButton > button[data-testid="baseButton-secondary"] {
        background-color: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
    }
    [data-testid="stSidebar"] div.stButton > button[data-testid="baseButton-secondary"] p {
        color: #0f172a !important; /* Fixes invisible white text on white button */
        font-weight: 600 !important;
    }
    [data-testid="stSidebar"] div.stButton > button[data-testid="baseButton-secondary"]:hover {
        background-color: #f1f5f9 !important;
        border-color: #2563eb !important;
    }
    [data-testid="stSidebar"] div.stButton > button[data-testid="baseButton-secondary"]:hover p {
        color: #2563eb !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- DYNAMIC MAIN CONTENT THEME ENGINE ---
if theme_choice == "Dark Mode 🌙":
    st.markdown("""
        <style>
        /* Main Application Dark Panel Layout */
        .stApp { background-color: #0f172a !important; }
        
        /* Main Stage Panel Text Hierarchies */
        .stApp [data-testid="stMain"] h1, .stApp [data-testid="stMain"] h2, .stApp [data-testid="stMain"] h3, 
        .stApp [data-testid="stMain"] h4, .stApp [data-testid="stMain"] label, .stApp [data-testid="stMain"] span, 
        .stApp [data-testid="stMain"] p, .stApp [data-testid="stMain"] .stMarkdown { 
            color: #f8fafc !important; 
        }
        
        /* Main Stage Secondary Structural Controls */
        [data-testid="stMain"] div.stButton > button[data-testid="baseButton-secondary"] {
            background-color: #1e293b !important;
            border: 1px solid #475569 !important;
        }
        [data-testid="stMain"] div.stButton > button[data-testid="baseButton-secondary"] p {
            color: #f8fafc !important;
        }
        
        /* Dark Card Overrides for Quiz Display Frames */
        div.stInfo {
            background-color: #1e293b !important;
            border: 1px solid #334155 !important;
            border-radius: 12px !important;
        }
        div.stInfo div, div.stInfo h4, div.stInfo p { color: #f8fafc !important; }
        
        /* KPI Dashboard Metric Card Grids */
        div.metric-card {
            background-color: #1e293b;
            border: 1px solid #334155;
            border-radius: 12px;
            padding: 20px;
            text-align: center;
        }
        .metric-val { font-size: 32px; font-weight: 700; color: #38bdf8; }
        .metric-lbl { font-size: 14px; color: #94a3b8; font-weight: 600; text-transform: uppercase; }
        
        .custom-hr { margin: 1.5rem 0; height: 3px; background: linear-gradient(to right, #38bdf8, #818cf8, transparent); }
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
        /* Main Application Light Panel Layout */
        .stApp { background-color: #f8fafc !important; }
        
        /* Main Stage Panel Text Hierarchies */
        .stApp [data-testid="stMain"] h1, .stApp [data-testid="stMain"] h2, .stApp [data-testid="stMain"] h3, 
        .stApp [data-testid="stMain"] h4, .stApp [data-testid="stMain"] label, .stApp [data-testid="stMain"] span, 
        .stApp [data-testid="stMain"] p, .stApp [data-testid="stMain"] .stMarkdown { 
            color: #0f172a !important; 
        }
        
        /* Main Stage Secondary Structural Controls */
        [data-testid="stMain"] div.stButton > button[data-testid="baseButton-secondary"] {
            background-color: #ffffff !important;
            border: 1px solid #cbd5e1 !important;
        }
        [data-testid="stMain"] div.stButton > button[data-testid="baseButton-secondary"] p {
            color: #0f172a !important;
        }
        [data-testid="stMain"] div.stButton > button[data-testid="baseButton-secondary"]:hover {
            background-color: #f1f5f9 !important;
            border-color: #2563eb !important;
        }
        [data-testid="stMain"] div.stButton > button[data-testid="baseButton-secondary"]:hover p {
            color: #2563eb !important;
        }
        
        /* Light Card Overrides for Quiz Display Frames */
        div.stInfo {
            background-color: #ffffff !important;
            border: 1px solid #e2e8f0 !important;
            border-radius: 12px !important;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05) !important;
        }
        div.stInfo div, div.stInfo h4, div.stInfo p { color: #0f172a !important; }
        
        /* KPI Dashboard Metric Card Grids */
        div.metric-card {
            background-color: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        }
        .metric-val { font-size: 32px; font-weight: 700; color: #2563eb; }
        .metric-lbl { font-size: 14px; color: #64748b; font-weight: 600; text-transform: uppercase; }
        
        .custom-hr { margin: 1.5rem 0; height: 3px; background: linear-gradient(to right, #3b82f6, #60a5fa, transparent); }
        </style>
    """, unsafe_allow_html=True)


# --- 30 CATEGORIZED PROGRAMMING LANGUAGES (PL) QUIZ DATA ---
PL_QUIZ_DATA = [
    {"q": "Which data structure follows a Last-In, First-Out (LIFO) principle?", "options": ["Queue", "Stack", "Array"], "ans": "Stack", "cat": "Data Structures"},
    {"q": "What is Python's primary framework used here for rendering web components?", "options": ["Django", "Flask", "Streamlit"], "ans": "Streamlit", "cat": "Web Architecture"},
    {"q": "In a 3-stack system, which layer compiles and stitches user interface states?", "options": ["Claude", "Jules", "Stitch"], "ans": "Stitch", "cat": "Advanced Systems"},
    {"q": "Which programming paradigm is based on the concept of 'objects' containing data and code?", "options": ["Functional", "Procedural", "Object-Oriented"], "ans": "Object-Oriented", "cat": "OOP Concepts"},
    {"q": "What keyword is used to define a function in Python?", "options": ["func", "def", "function"], "ans": "def", "cat": "Core Syntax"},
    {"q": "Which language is primarily known for running natively inside web browsers?", "options": ["Java", "C++", "JavaScript"], "ans": "JavaScript", "cat": "Core Syntax"},
    {"q": "What is the time complexity of searching for an element in a balanced Binary Search Tree (BST)?", "options": ["O(1)", "O(log n)", "O(n)"], "ans": "O(log n)", "cat": "Data Structures"},
    {"q": "Which of the following is a statically typed language?", "options": ["Python", "Java", "Ruby"], "ans": "Java", "cat": "Core Syntax"},
    {"q": "What does SQL stand for?", "options": ["Structured Query Language", "Simple Queue Language", "Sequential Query Logic"], "ans": "Structured Query Language", "cat": "Core Syntax"},
    {"q": "In Python, which built-in data type is unordered and does not allow duplicate members?", "options": ["List", "Tuple", "Set"], "ans": "Set", "cat": "Data Structures"},
    {"q": "Which HTML/CSS-based styling framework is highly popular for rapid frontend UI development?", "options": ["Django", "Tailwind CSS", "Pandas"], "ans": "Tailwind CSS", "cat": "Web Architecture"},
    {"q": "What is the term used when a function calls itself inside its own body?", "options": ["Iteration", "Recursion", "Encapsulation"], "ans": "Recursion", "cat": "Core Syntax"},
    {"q": "Which language is standardly used for native Android development modernly?", "options": ["Swift", "Kotlin", "C#"], "ans": "Kotlin", "cat": "Core Syntax"},
    {"q": "What does the 'JVM' stand for in the context of Java execution?", "options": ["Java Virtual Machine", "Java Version Manager", "Java Variable Model"], "ans": "Java Virtual Machine", "cat": "Advanced Systems"},
    {"q": "Which Git command is used to save changes locally without committing them to a branch history?", "options": ["git stash", "git push", "git clone"], "ans": "git stash", "cat": "Advanced Systems"},
    {"q": "What is the index of the first element in an array or list in most programming languages?", "options": ["1", "0", "-1"], "ans": "0", "cat": "Data Structures"},
    {"q": "Which data structure uses key-value pairs to store information?", "options": ["Dictionary / Hash Map", "Linked List", "Queue"], "ans": "Dictionary / Hash Map", "cat": "Data Structures"},
    {"q": "What operator is used for string concatenation in JavaScript?", "options": ["&", "+", "."], "ans": "+", "cat": "Core Syntax"},
    {"q": "Which of the following is a compiled language rather than interpreted?", "options": ["PHP", "C++", "Python"], "ans": "C++", "cat": "Advanced Systems"},
    {"q": "What is the purpose of a 'try-except' block in Python programming?", "options": ["Performance Loop", "Memory Allocation", "Exception Handling"], "ans": "Exception Handling", "cat": "Core Syntax"},
    {"q": "Which programming language was developed by Microsoft and runs primarily on the .NET framework?", "options": ["C#", "Java", "Go"], "ans": "C#", "cat": "Core Syntax"},
    {"q": "What does API stand for?", "options": ["Application Programming Interface", "Automated Processing Integration", "Array Parameter Index"], "ans": "Application Programming Interface", "cat": "Web Architecture"},
    {"q": "In Object-Oriented Programming, what is it called when a child class adopts variables and methods from a parent class?", "options": ["Polymorphism", "Abstraction", "Inheritance"], "ans": "Inheritance", "cat": "OOP Concepts"},
    {"q": "Which CSS property is used to change the background color of an element?", "options": ["color", "background-color", "fg-color"], "ans": "background-color", "cat": "Web Architecture"},
    {"q": "What kind of language uses a garbage collector to manage memory automatically?", "options": ["Managed Language", "Low-Level Language", "Assembly Language"], "ans": "Managed Language", "cat": "Advanced Systems"},
    {"q": "Which keyword is used in JavaScript to declare a variable that cannot be reassigned?", "options": ["let", "var", "const"], "ans": "const", "cat": "Core Syntax"},
    {"q": "What format is commonly used to exchange data between a web server and a web application?", "options": ["JSON", "HTML Only", "TXT"], "ans": "JSON", "cat": "Web Architecture"},
    {"q": "What does the 'len()' function do in Python?", "options": ["Clears a collection", "Returns the number of items", "Generates a random integer"], "ans": "Returns the number of items", "cat": "Core Syntax"},
    {"q": "Which data structure uses pointers to connect nodes sequentially in memory?", "options": ["Array", "Linked List", "Stack"], "ans": "Linked List", "cat": "Data Structures"},
    {"q": "What is the standard port number used for secure HTTPS web traffic?", "options": ["80", "443", "8080"], "ans": "443", "cat": "Web Architecture"}
]

# --- UI HEADER ---
st.title("🎯 Interactive Quiz Generator PL")
st.markdown('<div class="custom-hr"></div>', unsafe_allow_html=True)

# --- SIDEBAR DASHBOARD CONTROL MODULES ---
st.sidebar.markdown("### ⚙️ Application Configuration")
st.sidebar.info("📚 **Active Module:** Programming Languages (PL)")

# Debug Switch Toggle Feature
debug_mode = st.sidebar.toggle("🖥️ Enable 3-Stack Debug Mode", value=False)

# Adjustable Mode Settings Configuration
if st.session_state.pipeline_stage == "idle":
    st.sidebar.markdown("### 🛠️ Session Settings")
    length_choice = st.sidebar.selectbox(
        "Select Quiz Session Size:",
        options=[30, 20, 10, 5],
        format_func=lambda x: f"Complete {x} Challenges Pool" if x == 30 else f"Shortened {x} Questions Sprint"
    )
    st.session_state.quiz_length_setting = length_choice

# Live metric dashboards display
if st.session_state.pipeline_stage in ["active", "summary"]:
    st.sidebar.markdown("### 📈 Live Scoreboard")
    st.sidebar.metric(label="Total Points Secured", value=f"{st.session_state.user_score} / {len(st.session_state.quiz_questions)}")
    if st.session_state.current_q_index > 0:
        pct = int((st.session_state.user_score / st.session_state.current_q_index) * 100)
        st.sidebar.metric(label="Current Run Accuracy", value=f"{pct}%")
        
    # Live Progress Tracker Matrix inside Sidebar
    st.sidebar.markdown("### 📋 Live Track Grid")
    cols = st.sidebar.columns(5)
    for index in range(len(st.session_state.quiz_questions)):
        col_selector = index % 5
        if index < st.session_state.current_q_index:
            q_obj = st.session_state.quiz_questions[index]
            u_ans = st.session_state.selected_answers.get(index)
            if u_ans == q_obj['ans']:
                cols[col_selector].markdown(f"🟢 `Q{index+1}`")
            else:
                cols[col_selector].markdown(f"🔴 `Q{index+1}`")
        elif index == st.session_state.current_q_index:
            cols[col_selector].markdown(f"🔵 `Q{index+1}`")
        else:
            cols[col_selector].markdown(f"⚪ `Q{index+1}`")

if st.session_state.history:
    st.sidebar.markdown("### 📜 Session History Logs")
    for idx, run in enumerate(st.session_state.history):
        st.sidebar.text(f"Attempt #{idx+1}: {run['score']}/{run['total']} ({run['percent']}%)\n")

st.sidebar.markdown("---")
if st.sidebar.button("🚀 Generate New Random Quiz", type="primary", use_container_width=True):
    st.session_state.pipeline_stage = "processing"
    st.session_state.current_q_index = 0
    st.session_state.user_score = 0
    st.session_state.selected_answers = {}
    st.session_state.has_answered = False
    st.session_state.start_time = time.time()
    st.rerun()

if st.sidebar.button("🗑️ Reset Application", use_container_width=True):
    st.session_state.pipeline_stage = "idle"
    st.session_state.quiz_questions = []
    st.session_state.history = []
    st.rerun()

# Developers Credit Footer Banner
st.sidebar.markdown("---")
st.sidebar.markdown("**Project Developers:** Anislag, Camingue, Galo")

# --- DEBUG OVERLAY PANEL DISPLAY ---
if debug_mode:
    st.warning("⚠️ **3-Stack Pipeline Debug Monitor Active**")
    st.json({
        "pipeline_state": st.session_state.pipeline_stage,
        "current_index": st.session_state.current_q_index,
        "questions_loaded": len(st.session_state.quiz_questions),
        "score_tracker": st.session_state.user_score
    })

# --- SYSTEM ENGINE COMPILATION LIFECYCLE ---
if st.session_state.pipeline_stage == "idle":
    st.info(f"💡 **Welcome to the Quiz Simulator!** Click 'Generate New Random Quiz' on the left sidebar controls to launch your customized exam session.")

elif st.session_state.pipeline_stage == "processing":
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    status_text.text("🤖 [Claude] Parsing randomized data criteria arrays...")
    time.sleep(0.3)
    progress_bar.progress(33)
    
    status_text.text("⚡ [Jules] Dynamic compilation & internal option shuffling...")
    shuffled_pool = list(PL_QUIZ_DATA)
    random.shuffle(shuffled_pool)
    
    target_pool_slice = shuffled_pool[:st.session_state.quiz_length_setting]
    for q in target_pool_slice:
        random.shuffle(q["options"])
    st.session_state.quiz_questions = target_pool_slice
    time.sleep(0.3)
    progress_bar.progress(66)
    
    status_text.text("🧵 [Stitch] Mounting layouts and finalizing visual frames...")
    time.sleep(0.3)
    progress_bar.progress(100)
    
    status_text.empty()
    progress_bar.empty()
    st.session_state.pipeline_stage = "active"
    st.rerun()

# --- ACTIVE INTERACTIVE EXAM VIEW ---
elif st.session_state.pipeline_stage == "active":
    questions = st.session_state.quiz_questions
    current_idx = st.session_state.current_q_index
    
    if current_idx < len(questions):
        current_item = questions[current_idx]
        
        col_q, col_p = st.columns([3, 1.2])
        col_q.subheader(f"📝 Question {current_idx + 1} of {len(questions)}")
        col_p.markdown(f"**Topic Tag:** :orange[[{current_item['cat']}]]")
        
        progress_val = int(((current_idx) / len(questions)) * 100)
        st.progress(progress_val)
        
        st.info(f"#### {current_item['q']}")
        
        user_choice = st.radio(
            "Select the correct answer choice below:", 
            current_item['options'], 
            key=f"question_{current_idx}",
            disabled=st.session_state.has_answered
        )
        st.markdown("")

        if not st.session_state.has_answered:
            if st.button("📥 Check Answer Verification", type="primary", use_container_width=True):
                st.session_state.selected_answers[current_idx] = user_choice
                st.session_state.has_answered = True
                st.rerun()
        else:
            correct_answer = current_item['ans']
            if user_choice == correct_answer:
                st.success(f"🎯 **Correct Choice!** Points added to session memory state tracker.")
            else:
                st.error(f"⚠️ **Incorrect Choice.** The valid target answer was: **{correct_answer}**")
            
            if st.button("Advance to Next Question ➡️", use_container_width=True):
                if user_choice == correct_answer:
                    st.session_state.user_score += 1
                
                st.session_state.current_q_index += 1
                st.session_state.has_answered = False
                st.rerun()
    else:
        final_pct = int((st.session_state.user_score / len(questions)) * 100)
        st.session_state.history.append({
            "score": st.session_state.user_score,
            "total": len(questions),
            "percent": final_pct
        })
        st.session_state.pipeline_stage = "summary"
        st.rerun()

# --- ANALYTICS PERFORMANCE DASHBOARD ---
elif st.session_state.pipeline_stage == "summary":
    questions = st.session_state.quiz_questions
    st.balloons()
    
    elapsed_time = int(time.time() - st.session_state.start_time)
    minutes = elapsed_time // 60
    seconds = elapsed_time % 60
    percentage = int((st.session_state.user_score / len(questions)) * 100)
    
    st.markdown("## 📊 Performance Analytics Dashboard")
    st.markdown("Review complete statistical diagnostic parameters generated for this runtime evaluation session.")
    
    # 1. Metric Columns Row
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f'<div class="metric-card"><div class="metric-val">{st.session_state.user_score} / {len(questions)}</div><div class="metric-lbl">Total Score</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="metric-card"><div class="metric-val">{percentage}%</div><div class="metric-lbl">Accuracy</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="metric-card"><div class="metric-val">{minutes:02d}:{seconds:02d}</div><div class="metric-lbl">Time Taken</div></div>', unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Performance Class Callout Info Card
    if percentage >= 90:
        st.success("🥇 **Performance Ranking: Master of PL Architecture** — Flawless foundational execution matrix.")
    elif percentage >= 70:
        st.info("🥈 **Performance Ranking: Competent Software Engineer** — High algorithmic competency profile.")
    else:
        st.warning("🥉 **Performance Ranking: Junior Developer Trainee** — Needs additional structured compilation practice.")
        
    st.markdown('<div class="custom-hr"></div>', unsafe_allow_html=True)
    
    # 2. Split Screen Row for Mastery Maps
    col_left, col_right = st.columns([1.1, 1])
    
    with col_left:
        st.markdown("### 📈 Category Mastery Levels")
        cat_metrics = {}
        for i, q in enumerate(questions):
            category = q['cat']
            if category not in cat_metrics:
                cat_metrics[category] = {"correct": 0, "total": 0}
            cat_metrics[category]["total"] += 1
            if st.session_state.selected_answers.get(i) == q['ans']:
                cat_metrics[category]["correct"] += 1
                
        for cat, data in cat_metrics.items():
            cat_pct = int((data["correct"] / data["total"]) * 100)
            st.write(f"**{cat}** *({data['correct']}/{data['total']})*")
            st.progress(cat_pct)
            
    with col_right:
        st.markdown("### 🎛️ Chronological Matrix")
        st.markdown("Visual sequence mapping of questions processed:")
        
        timeline_html = "<div style='display: flex; flex-wrap: wrap; gap: 8px; margin-top: 10px;'>"
        for i, q in enumerate(questions):
            u_ans = st.session_state.selected_answers.get(i)
            bg_color = "#22c55e" if u_ans == q['ans'] else "#ef4444"
            timeline_html += f"<div style='background-color: {bg_color}; color: white; padding: 6px 12px; border-radius: 6px; font-weight: bold; font-size: 13px;'>Q{i+1}</div>"
        timeline_html += "</div>"
        st.markdown(timeline_html, unsafe_allow_html=True)
        
    st.markdown('<div class="custom-hr"></div>', unsafe_allow_html=True)
    
    # 3. Tab Elements for Logs and Exports
    tab1, tab2 = st.tabs(["🔍 Itemized Audit Logs", "💾 Export Session JSON"])
    
    with tab1:
        for i, q in enumerate(questions):
            u_ans = st.session_state.selected_answers.get(i)
            c_ans = q['ans']
            status_icon = "🟢" if u_ans == c_ans else "🔴"
            st.markdown(f"**Q{i+1}:** {q['q']} *({q['cat']})*")
            st.write(f"{status_icon} User Input: *{u_ans}* | Correct Target: **{c_ans}**")
            st.markdown("---")
            
    with tab2:
        st.markdown("Raw system parameters payload logged by the framework:")
        st.json({
            "session_metrics": {
                "raw_score": st.session_state.user_score,
                "total_questions": len(questions),
                "accuracy_percentage": percentage,
                "duration_seconds": elapsed_time
            },
            "user_selections": st.session_state.selected_answers
        })
        
    if st.button("🔄 Restart Quiz Session Iteration", type="primary", use_container_width=True):
        st.session_state.pipeline_stage = "idle"
        st.rerun()