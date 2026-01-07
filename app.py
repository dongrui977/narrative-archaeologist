import streamlit as st
from openai import OpenAI

# 1. 视觉黑科技：韦斯安德森电影美学 + 胶片 UI
st.set_page_config(page_title="MindMemo | Cinema Archive", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@300;600&display=swap');

    /* 全局背景：复古米色纸张感 */
    .stApp {
        background-color: #E6E1D6;
        background-image: url("https://www.transparenttextures.com/patterns/handmade-paper.png");
        color: #4A4A4A;
        font-family: 'Noto Serif SC', serif;
    }

    header, footer, #MainMenu {visibility: hidden;}

    /* 电影胶片容器：黑底打孔 */
    .film-strip {
        background: #1A1A1A;
        border-radius: 15px;
        padding: 40px 20px;
        margin-bottom: 30px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.3);
        border-top: 25px solid #1A1A1A;
        border-bottom: 25px solid #1A1A1A;
        position: relative;
    }

    /* 模拟胶片打孔 */
    .film-strip::before, .film-strip::after {
        content: "■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■";
        color: #E6E1D6;
        font-size: 10px;
        letter-spacing: 12px;
        position: absolute;
        width: 100%;
        text-align: center;
        left: 0;
    }
    .film-strip::before { top: -20px; }
    .film-strip::after { bottom: -20px; }

    /* 内部白底输入区：高级复古感 */
    .inner-frame {
        background: #FDFCF0;
        border-radius: 5px;
        padding: 30px;
        border: 1px solid #D4A373;
    }

    .room-title {
        font-size: 1.8rem;
        font-weight: 600;
        color: #2C2C2C;
        margin-bottom: 15px;
        letter-spacing: 2px;
        display: flex;
        align-items: center;
    }

    .dessert-label {
        font-size: 2rem;
        margin-right: 15px;
    }

    /* 字体：剧本感 */
    h4 {
        color: #5E5E5E;
        line-height: 1.6;
        font-weight: 300;
        margin-bottom: 25px;
    }

    /* 输入框：透明底、极简线 */
    .stTextArea textarea {
        background-color: transparent !important;
        border: none !important;
        border-bottom: 1px dashed #D4A373 !important;
        color: #2C2C2C !important;
        font-size: 1.1rem !important;
        padding: 10px 0 !important;
        border-radius: 0 !important;
    }

    /* 按钮：深咖色火漆印感 */
    .stButton > button {
        background-color: #423629 !important;
        color: #E6E1D6 !important;
        border: 1px solid #D4A373 !important;
        border-radius: 0px !important;
        padding: 12px 0 !important;
        width: 100%;
        letter-spacing: 5px;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton > button:hover {
        background-color: #D4A373 !important;
        color: #1A1A1A !important;
    }

    /* 结果卡片：圣光闪烁的仪式感 */
    .report-card {
        background: #FDFCF0;
        border: 2px solid #D4A373;
        padding: 40px;
        box-shadow: 0 0 50px rgba(212, 163, 115, 0.4);
        animation: divineGlow 3s infinite alternate;
        color: #2C2C2C;
    }
    @keyframes divineGlow {
        from { box-shadow: 0 0 20px rgba(212, 163, 115, 0.2); }
        to { box-shadow: 0 0 60px rgba(212, 163, 115, 0.6); }
    }
    </style>
    """, unsafe_allow_html=True)

# 2. 数据与逻辑
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'answers' not in st.session_state:
    st.session_state.answers = []

rooms = [
    {"icon": "🍮", "title": "系全底色", "q": "童年记忆里，那个最让你安心的味道或画面是什么？"},
    {"icon": "🍰", "title": "珠光时刻", "q": "哪一刻，你觉得自己像缀满珍珠的蛋糕般耀眼？"},
    {"icon": "🌑", "title": "至暗瞬间", "q": "有没有什么时候，生活让你尝到了烧焦般的苦涩？"},
    {"icon": "🌡️", "title": "身身警报", "q": "当你感到压力时，身体哪个部位会先向你发出信号？"},
    {"icon": "🤝", "title": "重要他人", "q": "那个人对你性格的影响，更像哪种甜味的层次？"},
    {"icon": "🌀", "title": "通耐慢圈", "q": "有什么不爽的套路，是你一直在‘复读’运行的？"}
]

# 3. 页面渲染
if st.session_state.step < len(rooms):
    r = rooms[st.session_state.step]
    
    st.markdown(f'''
        <div class="film-strip">
            <div class="inner-frame">
                <div class="room-title">
                    <span class="dessert-label">{r['icon']}</span>
                    {r['title']}
                </div>
                <h4>{r['q']}</h4>
            </div>
        </div>
    ''', unsafe_allow_html=True)
    
    ans = st.text_area("", key=f"f_{st.session_state.step}", height=120, label_visibility="collapsed", placeholder="记录下这段墙砖上的文字...")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("PROCEED / 下一帧"):
            if ans:
                st.session_state.answers.append(ans)
                st.session_state.step += 1
                st.rerun()
            else:
                st.warning("请留下些什么...")

else:
    st.markdown('<h2 style="text-align:center; letter-spacing:10px;">FIN / 封存完成</h2>', unsafe_allow_html=True)
    
    if st.button("OPEN THE DOSSIER / 解密档案"):
        with st.spinner("正在注塑、重构叙事中..."):
            try:
                client = OpenAI(api_key=st.secrets["DEEPSEEK_API_KEY"], base_url="https://api.deepseek.com")
                full_context = "\\n".join(st.session_state.answers)
                
                prompt = f"你是一个名为MindMemo的心理分析引擎。对以下内容进行冷峻深刻的分析，不要客套话。格式：### 🏷️ 灵魂标签 \\n ### 🧠 脚本监测 \\n ### 🍃 进化路径。内容：{full_context}"
                
                response = client.chat.completions.create(model="deepseek-chat", messages=[{"role": "user", "content": prompt}])
                
                st.markdown(f'''
                    <div class="report-card">
                        <div style="text-align:center; font-weight:bold; letter-spacing:5px; border-bottom:1px solid #D4A373; padding-bottom:10px; margin-bottom:20px;">MINDMEMO FINAL REPORT</div>
                        {response.choices[0].message.content}
                    </div>
                ''', unsafe_allow_html=True)
                
                if st.button("RESTART / 重新开启"):
                    st.session_state.step = 0
                    st.session_state.answers = []
                    st.rerun()
                    
            except Exception as e:
                st.error("API Error. 请检查余额。")
