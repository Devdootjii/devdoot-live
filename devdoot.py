import streamlit as st
import pandas as pd
import os
import datetime
import time
import sys
import base64
from io import StringIO

# ==========================================
# BLOCK 1: ENGINE & CONFIG
# ==========================================
st.set_page_config(page_title="Devdoot HQ", page_icon="🦅", layout="wide")

FILES = {
    "users": "users_db.csv", "attendance": "attendance_log.csv",
    "tasks": "task_log.csv", "logo": "logo.png", "video": "background.mp4"
}

# --- IST TIME FUNCTION (INDIA TIME) ---
def get_ist_time():
    # Server Time (UTC) + 5 Hours 30 Minutes
    return datetime.datetime.now() + datetime.timedelta(hours=5, minutes=30)

def init_db():
    if not os.path.exists(FILES["users"]):
        data = {"Username": ["Devdoot", "Balram", "Naina", "Ritesh", "Harsh", "Shalini"],
                "Password": ["admin123", "1234", "1234", "1234", "1234", "1234"],
                "Role": ["Admin", "Agent", "Agent", "Agent", "Agent", "Agent"],
                "Level": [1]*6, "XP": [0]*6}
        pd.DataFrame(data).to_csv(FILES["users"], index=False)

def load_db(key): return pd.read_csv(FILES[key]) if os.path.exists(FILES[key]) else pd.DataFrame()
def save_db(df, key): df.to_csv(FILES[key], index=False)
def get_user_data(user): df = load_db("users"); return df[df['Username'] == user].iloc[0]
def update_level(user, lvl, xp): 
    df = load_db("users"); 
    df.loc[df['Username'] == user, 'Level'] = lvl
    df.loc[df['Username'] == user, 'XP'] += xp
    save_db(df, "users")

init_db()

# ==========================================
# BLOCK 2: UI & CSS
# ==========================================
def add_bg_from_local(image_file):
    with open(image_file, "rb") as file:
        encoded_string = base64.b64encode(file.read())
    st.markdown(
        f"""
        <style>
        .stApp {{ background: rgba(0,0,0,0); }}
        .bg-video {{
            position: fixed; top: 0; left: 0; min-width: 100%; min-height: 100%;
            z-index: -1; opacity: 0.85; object-fit: cover;
        }}
        </style>
        <video autoplay muted loop id="myVideo" class="bg-video">
            <source src="data:video/mp4;base64,{encoded_string.decode()}" type="video/mp4">
        </video>
        """, unsafe_allow_html=True
    )

if os.path.exists(FILES["video"]):
    add_bg_from_local(FILES["video"])

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Exo+2:wght@500;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Exo 2', sans-serif;
        color: #ffffff;
    }

    h1, h2, h3 {
        background: linear-gradient(90deg, rgba(0,0,0,0.8), rgba(0,0,0,0));
        border-left: 5px solid #00c6ff;
        padding: 10px 20px;
        background: linear-gradient(to right, #00c6ff, #0072ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 20px;
    }

    [data-testid="stImage"] img {
        border-radius: 50% !important;
        border: 3px solid #00c6ff;
        box-shadow: 0 0 15px #00c6ff;
        object-fit: cover !important;
        aspect-ratio: 1 / 1;
    }

    div[data-testid="column"] .stButton button p:contains("⏻") {
        color: #FF0000 !important;
        font-size: 24px !important;
        font-weight: 900 !important;
    }
    
    .stButton>button {
        background: rgba(0,0,0,0.6);
        color: #00c6ff;
        border: 1px solid #00c6ff;
        border-radius: 50px;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background: #00c6ff;
        color: black;
        box-shadow: 0 0 20px #00c6ff;
        transform: scale(1.05);
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 15px;
        background-color: transparent;
        padding: 15px;
        justify-content: center;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        border-radius: 50px;
        background-color: rgba(0,0,0,0.8);
        color: #aaa;
        border: 1px solid #333;
        padding: 0 25px;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #00c6ff, #0072ff);
        color: white !important;
        border: 1px solid #fff;
        box-shadow: 0 0 15px #00c6ff;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# BLOCK 3: MODULES
# ==========================================
MODULES = {
    1: {
        "title": "MODULE 1: GENESIS (VARIABLES)",
        "content": "### 📡 Concept: The Container\nVariables store data.\n\n`agent = 'Devdoot'`\n`id = 7`",
        "quiz": {"q": "Which variable name is INVALID?", "options": ["_agent", "agent_1", "1st_agent", "AGENT"], "ans": "1st_agent"}
    },
    2: {
        "title": "MODULE 2: LOGIC GATES (IF-ELSE)",
        "content": "### 📡 Concept: Decisions\n`if energy < 10: print('Sleep')`",
        "quiz": {"q": "What runs if 'if' fails?", "options": ["Error", "Code stops", "Runs 'else'", "Blast"], "ans": "Runs 'else'"}
    },
    3: {
        "title": "MODULE 3: CYCLES (LOOPS)",
        "content": "### 📡 Concept: Automation\n`for i in range(5): print(i)`",
        "quiz": {"q": "range(0, 5) generates?", "options": ["4 items", "5 items", "6 items"], "ans": "5 items"}
    },
    4: {
        "title": "MODULE 4: INVENTORY (LISTS)",
        "content": "### 📡 Concept: Lists\n`squad = ['A', 'B', 'C']`\nIndex starts at 0.",
        "quiz": {"q": "Get last item?", "options": ["list[0]", "list[-1]", "list[end]"], "ans": "list[-1]"}
    },
    5: {
        "title": "MODULE 5: TOOLS (FUNCTIONS)",
        "content": "### 📡 Concept: Functions\n`def action(): return 'Done'`",
        "quiz": {"q": "Keyword for function?", "options": ["func", "def", "define"], "ans": "def"}
    },
    6: {
        "title": "MODULE 6: ERROR HANDLING",
        "content": "### 📡 Concept: Safety\n`try: ... except: ...`",
        "quiz": {"q": "Catches error?", "options": ["try", "catch", "except"], "ans": "except"}
    }
}

# ==========================================
# BLOCK 4: LOGIN
# ==========================================
if "logged_in" not in st.session_state: st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        if os.path.exists(FILES["logo"]):
            st.image(FILES["logo"], width=120)
        st.markdown("""<div style='background: rgba(0,0,0,0.8); padding: 30px; border-radius: 20px; border: 1px solid #00c6ff; text-align: center;'>
            <h2>IDENTITY VERIFICATION</h2></div>""", unsafe_allow_html=True)
        
        users = load_db("users")
        u = st.selectbox("SELECT AGENT", users['Username'])
        p = st.text_input("SECURITY CODE", type="password")
        if st.button("AUTHENTICATE"):
            user = users[users['Username']==u].iloc[0]
            if str(user['Password']) == p:
                st.session_state.update({"logged_in": True, "user": u, "role": user['Role']})
                st.toast("✅ ACCESS GRANTED", icon="🔐")
                time.sleep(1)
                st.rerun()
            else: st.error("⚠️ ACCESS DENIED")
    st.stop()

# ==========================================
# BLOCK 5: MAIN APP (IST FIXED)
# ==========================================
user = get_user_data(st.session_state['user'])
lvl, xp = int(user['Level']), int(user['XP'])

top_col1, top_col2, top_col3 = st.columns([1, 8, 1])
with top_col1:
    if os.path.exists(FILES["logo"]): st.image(FILES["logo"], width=80)
with top_col2:
    st.markdown(f"<h3 style='margin:0; font-size: 20px; text-align: left;'>WELCOME, AGENT {st.session_state['user']} | LEVEL {lvl}</h3>", unsafe_allow_html=True)
    st.progress(min(lvl*16, 100))
with top_col3:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("⏻"):
        st.session_state["logged_in"] = False
        st.rerun()

st.divider()

tab_names = ["📊 DASHBOARD", "💻 CODE LAB", "🧠 TRAINING", "📝 ATTENDANCE", "⚙️ SETTINGS"]
if st.session_state['role'] == "Admin": tab_names.append("👁️ GOD VIEW")
tabs = st.tabs(tab_names)

# --- DASHBOARD (Uses IST Time) ---
with tabs[0]:
    st.title("COMMAND CENTER")
    c1, c2, c3 = st.columns(3)
    c1.metric("OPERATOR LEVEL", f"{lvl}", f"{xp} XP")
    
    att = load_db("attendance")
    # FIX: Use IST time for comparing today's date
    today = get_ist_time().strftime("%Y-%m-%d")
    present = att[att['Date']==today].shape[0] if not att.empty else 0
    c2.metric("SQUAD STATUS", f"{present}/6 Online", "Active")
    c3.metric("NEXT MISSION", f"Module {min(lvl+1, 6)}", "Pending")

# --- CODE LAB ---
with tabs[1]:
    st.title("PYTHON IDE")
    col_code, col_out = st.columns([1, 1])
    with col_code:
        st.markdown("### 📝 EDITOR")
        code = st.text_area("Write Python Code:", height=300, value="# Practice here\nprint('Devdoot HQ')")
        b1, b2 = st.columns([1, 1])
        with b1: run = st.button("▶ RUN CODE")
        with b2: st.download_button(label="💾 SAVE FILE", data=code, file_name="mission.py", mime="text/x-python")
    with col_out:
        st.markdown("### 📟 TERMINAL OUTPUT")
        if run:
            redirected_output = sys.stdout = StringIO()
            try: 
                exec(code)
                st.code(redirected_output.getvalue())
                st.toast("Executed Successfully", icon="✅")
            except Exception as e: st.error(f"RUNTIME ERROR:\n{e}")

# --- TRAINING ---
with tabs[2]:
    st.title("ACADEMY")
    mod_tabs = st.tabs([f"MOD {i}" for i in MODULES])
    for i, tab in enumerate(mod_tabs):
        m = i + 1
        with tab:
            if lvl < m: st.error(f"🔒 LOCKED. FINISH MODULE {m-1} FIRST.")
            else:
                d = MODULES[m]
                st.markdown(d['content'])
                st.divider()
                st.subheader("QUIZ PROTOCOL")
                q = d['quiz']
                st.write(f"**Q:** {q['q']}")
                ans = st.radio("Select:", q['options'], key=m)
                if st.button(f"SUBMIT ANSWER {m}"):
                    if ans == q['ans']:
                        st.toast(f"CORRECT! +50 XP", icon="🏆")
                        update_level(st.session_state['user'], m+1, 50)
                        time.sleep(1); st.rerun()
                    else: st.toast("NEGATIVE.", icon="❌")

# --- ATTENDANCE (Uses IST Time) ---
with tabs[3]:
    st.title("DAILY LOG")
    c1, c2 = st.columns([1,2])
    with c1:
        if st.button("MARK PRESENCE"):
            df = load_db("attendance")
            # FIX: Use IST Time
            now_ist = get_ist_time()
            today_str = now_ist.strftime("%Y-%m-%d")
            time_str = now_ist.strftime("%H:%M:%S")
            
            if not df.empty and not df[(df['Name']==st.session_state['user']) & (df['Date']==today_str)].empty:
                st.toast("ALREADY LOGGED", icon="🛑")
            else:
                new = pd.DataFrame({"Date": [today_str], "Time": [time_str], "Name": [st.session_state['user']], "Status": ["Present"]})
                save_db(pd.concat([df, new]), "attendance")
                st.toast(f"LOGGED AT {time_str}", icon="📍")
    with c2:
        st.dataframe(load_db("attendance"), use_container_width=True)

# --- SETTINGS ---
with tabs[4]:
    st.title("SETTINGS")
    new_p = st.text_input("NEW PASSWORD", type="password")
    if st.button("UPDATE"):
        df = load_db("users")
        df.loc[df['Username']==st.session_state['user'], 'Password'] = new_p
        save_db(df, "users")
        st.toast("UPDATED", icon="🔐")

if st.session_state['role'] == "Admin":
    with tabs[5]:
        st.title("👁️ GOD VIEW")
        st.dataframe(load_db("users"), use_container_width=True)
        st.dataframe(load_db("attendance"), use_container_width=True)
