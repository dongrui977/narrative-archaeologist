import streamlit as st
from openai import OpenAI

# 1. 视觉魔法：奶油色调 + 闪烁精灵
st.set_page_config(page_title="MindMemo | 甜品档案馆", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=ZCOOL+XiaoWei&display=swap');

    /* 全局：奶油马卡龙背景 */
    .stApp {
        background: linear-gradient(135deg, #fff5f5 0%, #f0f7ff 100%);
        color: #7d5a5a;
        font-family: 'sans-serif';
    }

    /* 隐藏杂项 */
    header, footer, #MainMenu {visibility: hidden;}

    /* 小精灵闪烁动画 */
    .sparkles {
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        pointer-events: none;
        background: url('https://www.transparenttextures.com/patterns/stardust.png');
        opacity: 0.3;
        animation: twinkle 5s infinite;
    }
    @keyframes twinkle {
        0%, 100% { opacity: 0.3; transform: scale(1); }
        50% { opacity: 0.6; transform: scale(1.1); }
    }

    /* 可爱卡片容器 */
    .sweet-card {
        background: rgba(255, 255, 255, 0.8);
        border-radius: 30px;
        padding: 40px;
        box-shadow: 0 20px 40px rgba(255, 182, 193, 0.2);
        border: 4px solid #fff;
        text-align: center;
        margin-top: 20px;
    }

    /* 标题字体 */
    .cute-title {
        font-family: 'ZCOOL XiaoWei', serif;
        font-size: 2.5rem;
        color: #ff8fab;
        margin-bottom: 10px;
        text-shadow: 2px 2px 0px #fff;
    }

    /* 输入框：圆滚滚 */
    .stTextArea textarea {
        background-color: #fff !important;
        border: 3px solid #ffe5ec !important;
        border-radius: 20px !important;
        color: #7d5a5a !important;
        font-size: 1.1rem !important;
        padding: 20px !important;
    }
    .stTextArea textarea:focus {
        border-color: #ffc2d1 !important;
        box-shadow: 0 0 15px rgba(255, 194, 209, 0.5) !important;
    }

    /* 按钮：Q弹感 */
    .stButton > button {
        background: linear-gradient(to right, #ffafbd, #ffc3a0) !important;
        color: white !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 15px 40px !important;
        font-weight: bold !important;
        font-size: 1.1rem !important;
        transition: 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .stButton > button:hover {
        transform: scale(1.1) rotate(2deg);
        box-shadow: 0 10px 20px rgba(255, 175, 189, 0.4) !important;
    }

    /* 最后的圣光卡片 */
    .holy-card {
        background: #fff;
        border-radius: 25px;
        padding: 40px;
        position: relative;
        overflow: hidden;
        border: 2px solid #ff8fab;
        box-shadow: 0 0 30px rgba(255, 143, 171, 0.3);
        animation: holyGlow 2s infinite alternate;
    }
    @keyframes holyGlow {
        from { box-shadow: 0 0 20px rgba(255, 143, 171, 0.2), 0 0 40px rgba(135, 206, 235, 0.2); }
        to { box-shadow: 0 0 40px rgba(255, 143, 171, 0.5), 0 0 60px rgba(135, 206, 235, 0.5); }
    }
    </style>
    <div class="sparkles"></div>
    """, unsafe_allow_html=True)

# 2. 会话管理
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'answers' not in st.session_state:
    st.session_state.answers = []

# 拆分后的 6 个问题
scenes = [
    {"icon": "🌱", "title": "原生底色", "q": "小时候最让你感到安全的一个画面是什么？"},
    {"icon": "✨", "title": "闪光时刻", "q": "哪一刻你觉得自己特别棒，像在发光？"},
    {"icon": "🌑", "title": "至暗瞬间", "q": "哪一刻让你感到特别委屈或无助？"},
    {"icon": "🌡️", "title": "身体警报", "q": "压力大时，身体哪个部位最先‘闹脾气’？"},
    {"icon": "🧸", "title": "重要他人", "q": "谁是那个让你想起来就心情复杂的人？"},
    {"icon": "🌀", "title": "循环怪圈", "q": "有什么不开心的事情是你一直在重复做的？"}
]

# 3. 逻辑渲染
if st.session_state.step < len(scenes):
    s = scenes[st.session_state.step]
    
    st.markdown(f'''
        <div class="sweet-card">
            <div style="font-size: 4rem;">{s['icon']}</div>
            <div class="cute-title">{s['title']}</div>
            <p style="color: #aaa;">{st.session_state.step + 1} / 6</p>
            <h3 style="color: #7d5a5a; margin-bottom: 20px;">{s['q']}</h3>
        </div>
    ''', unsafe_allow_html=True)
    
    ans = st.text_area("", key=f"ans_{st.session_state.step}", height=150, label_visibility="collapsed", placeholder="偷偷告诉我吧...")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("下一道甜点 ✨"):
            if ans:
                st.session_state.answers.append(ans)
                st.session_state.step += 1
                st.rerun()
            else:
                st.warning("还没写完呢~")

else:
    st.markdown('<div class="cute-title" style="text-align:center;">🎉 收集完毕！</div>', unsafe_allow_html=True)
    
    if st.button("生成我的心理魔法卡 ✨"):
        with st.spinner("小精灵正在努力计算中..."):
            try:
                client = OpenAI(api_key=st.secrets["DEEPSEEK_API_KEY"], base_url="https://api.deepseek.com")
                full_context = "\n".join(st.session_state.answers)
                
                prompt = f"""
                你是一个名为 "MindMemo" 的心理分析引擎。
                任务：生成极简心理卡片。
                原则：去聊天化、极简主义。
                输入：{full_context}
                格式：
                ### 🏷️ 智能标签
                ### 🧠 思维侦探 (CBT)
                ### 🍃 接纳与行动 (ACT)
                """
                
                response = client.chat.completions.create(model="deepseek-chat", messages=[{"role": "user", "content": prompt}])
                
                st.markdown(f'''
                    <div class="holy-card">
                        <div style="text-align:center; font-weight:bold; color:#ff8fab; margin-bottom:20px;">🍬 你的心灵魔法卡</div>
                        {response.choices[0].message.content}
                    </div>
                ''', unsafe_allow_html=True)
                
                # 循环逻辑：回到开头
                if st.button("再测一遍 🔄"):
                    st.session_state.step = 0
                    st.session_state.answers = []
                    st.rerun()
            except Exception as e:
                st.error("哎呀，小精灵迷路了，再试一次吧！")
