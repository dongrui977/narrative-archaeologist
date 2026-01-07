import streamlit as st
from openai import OpenAI

# 1. 视觉配置：韦斯安德森电影美学 + 复古胶片 UI
st.set_page_config(page_title="MindMemo | 心理考古城堡", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@300;600&family=Cinzel:wght@400;700&display=swap');

    .stApp {
        background-color: #E6E1D6;
        background-image: url("https://www.transparenttextures.com/patterns/handmade-paper.png");
        color: #4A4A4A;
        font-family: 'Noto Serif SC', serif;
    }

    header, footer, #MainMenu {visibility: hidden;}

    /* 首页入口卡片 */
    .portal-card {
        background: #FDFCF0;
        border: 2px solid #1A1A1A;
        padding: 40px 20px;
        text-align: center;
        transition: 0.3s;
        cursor: pointer;
        box-shadow: 10px 10px 0px #423629;
        margin-bottom: 20px;
    }
    .portal-card:hover {
        transform: translate(-5px, -5px);
        box-shadow: 15px 15px 0px #D4A373;
    }

    /* 电影胶片边框 */
    .film-strip {
        background: #1A1A1A;
        border-radius: 5px;
        padding: 40px 20px;
        margin-bottom: 30px;
        position: relative;
        border-top: 20px solid #1A1A1A;
        border-bottom: 20px solid #1A1A1A;
    }
    .film-strip::before, .film-strip::after {
        content: "■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■";
        color: #E6E1D6;
        font-size: 8px;
        letter-spacing: 15px;
        position: absolute; width: 100%; text-align: center; left: 0;
    }
    .film-strip::before { top: -15px; }
    .film-strip::after { bottom: -15px; }

    .inner-frame {
        background: #FDFCF0;
        padding: 30px;
        border: 1px solid #D4A373;
    }

    /* 按钮样式：复古高定 */
    .stButton > button {
        background-color: #423629 !important;
        color: #E6E1D6 !important;
        border: 1px solid #D4A373 !important;
        border-radius: 0px !important;
        width: 100%;
        letter-spacing: 3px;
        font-family: 'Cinzel', serif;
    }
    </style>
    """, unsafe_allow_html=True)

# 初始化状态
if 'mode' not in st.session_state:
    st.session_state.mode = None # 'daily' or 'deep'
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'answers' not in st.session_state:
    st.session_state.answers = []

# --- 首页：入口选择 ---
if st.session_state.mode is None:
    st.markdown("<h1 style='text-align:center; font-family:Cinzel; letter-spacing:10px;'>THE CASTLE</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; opacity:0.6; margin-bottom:50px;'>请选择您今日的探索路径</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="portal-card"><h3>🩹</h3><h4 style="font-family:Cinzel;">Daily Relief</h4><p style="font-size:0.8rem;">日常情绪清理<br>MindMemo 引擎</p></div>', unsafe_allow_html=True)
        if st.button("进入日常门扉"):
            st.session_state.mode = 'daily'
            st.rerun()
            
    with col2:
        st.markdown('<div class="portal-card"><h3>🏺</h3><h4 style="font-family:Cinzel;">Deep Archive</h4><p style="font-size:0.8rem;">深度生命考古<br>叙事重构师</p></div>', unsafe_allow_html=True)
        if st.button("进入深层暗室"):
            st.session_state.mode = 'deep'
            st.rerun()

# --- 模式 A：日常情绪处理 (MindMemo) ---
elif st.session_state.mode == 'daily':
    st.markdown("<h2 style='text-align:center; font-family:Cinzel;'>MINDMEMO ENGINE</h2>", unsafe_allow_html=True)
    st.markdown('<div class="film-strip"><div class="inner-frame"><h4>现在，请倾倒出您此刻堆积的情绪碎片。</h4><p style="font-size:0.8rem; opacity:0.5;">引擎将为您生成结构化心理卡片</p></div></div>', unsafe_allow_html=True)
    
    daily_input = st.text_area("", height=200, placeholder="无需逻辑，无需修饰，写下此刻...")
    
    if st.button("执行静默分析"):
        if daily_input:
            with st.spinner("剥离噪音，识别脚本..."):
                client = OpenAI(api_key=st.secrets["DEEPSEEK_API_KEY"], base_url="https://api.deepseek.com")
                prompt = f"# Role: MindMemo引擎\\n原则：去聊天化、极简主义、ACT+CBT视角。\\n格式：### 🏷️ 智能标签\\n### 🧠 思维侦探 (CBT)\\n### 🍃 接纳与行动 (ACT)\\n内容：{daily_input}"
                response = client.chat.completions.create(model="deepseek-chat", messages=[{"role": "user", "content": prompt}])
                st.markdown(f'<div style="background:#FDFCF0; padding:30px; border:2px solid #D4A373; box-shadow:0 0 20px rgba(212,163,115,0.3);">{response.choices[0].message.content}</div>', unsafe_allow_html=True)
        
        if st.button("返回城堡大厅"):
            st.session_state.mode = None
            st.rerun()

# --- 模式 B：深度个人发掘 (考古重构师) ---
elif st.session_state.mode == 'deep':
    rooms = [
        {"icon": "🌱", "title": "原生底色", "q": "原生底色：出生在哪里？童年记忆中最深刻的一个画面是什么？父母的关系以及他们对你的教育方式是怎样的？"},
        {"icon": "✨", "title": "高光至暗", "q": "高光与至暗：哪一刻让你觉得自己是世界的中心？又是哪一刻让你感到彻底的羞耻或绝望？"},
        {"icon": "💊", "title": "身体记号", "q": "身体的记号：你的身体生过什么病？当你压力最大时，身体哪个部位会先报警？"},
        {"icon": "🤝", "title": "重要他人", "q": "关键关系人：谁是你生命中的重要他人？那些让你爱恨交织的人是谁？"},
        {"icon": "🔀", "title": "转折执念", "q": "转折与执念：你换过哪些赛道？有没有什么模式是你发誓不想重复却一直在重复的？"}
    ]
    
    if st.session_state.step < len(rooms):
        r = rooms[st.session_state.step]
        st.markdown(f"<h3 style='text-align:center; font-family:Cinzel;'>DEEP ARCHIVE: ROOM {st.session_state.step + 1}</h3>", unsafe_allow_html=True)
        st.markdown(f'''<div class="film-strip"><div class="inner-frame"><div style="font-size:3rem;">{r['icon']}</div><h4 style="font-weight:600;">{r['title']}</h4><p>{r['q']}</p></div></div>''', unsafe_allow_html=True)
        
        ans = st.text_area("", key=f"deep_{st.session_state.step}", height=150, placeholder="请详细、私人、揉碎了写给我...")
        
        if st.button("前往下一间暗室"):
            if ans:
                st.session_state.answers.append(ans)
                st.session_state.step += 1
                st.rerun()
    else:
        st.markdown("<h2 style='text-align:center;'>考古档案已就绪</h2>", unsafe_allow_html=True)
        if st.button("开启叙事重构报告"):
            with st.spinner("考古学家正在通过碎片复原您的人生剧本..."):
                client = OpenAI(api_key=st.secrets["DEEPSEEK_API_KEY"], base_url="https://api.deepseek.com")
                full_data = "\\n".join(st.session_state.answers)
                prompt = f"# Role: 心理叙事重构师\\n核心：分析自动化脚本。绝对禁令：禁止行动建议。\\n格式：1.【叙事重构】2.【核心图式】3.【躯体化标记】4.【未完成的情结】5.【觉察时刻】\\n内容：{full_data}"
                response = client.chat.completions.create(model="deepseek-chat", messages=[{"role": "user", "content": prompt}])
                st.markdown(f'<div style="background:#FDFCF0; padding:30px; border:2px solid #423629; line-height:1.8;">{response.choices[0].message.content}</div>', unsafe_allow_html=True)
                
                if st.button("离开城堡大厅"):
                    st.session_state.mode = None
                    st.session_state.step = 0
                    st.session_state.answers = []
                    st.rerun()
