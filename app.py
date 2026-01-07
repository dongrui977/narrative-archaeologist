import streamlit as st
from openai import OpenAI

# 1. 顶级视觉工程：动态甜点背景 + 磨砂玻璃质感
st.set_page_config(page_title="MindMemo | 甜品档案馆", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=ZCOOL+XiaoWei&display=swap');

    /* 动态甜点背景层 */
    .stApp {
        background-color: #fff9f5;
        background-image: 
            url("https://img.icons8.com/fluency/48/000000/macaron.png"),
            url("https://img.icons8.com/fluency/48/000000/cupcake.png"),
            url("https://img.icons8.com/fluency/48/000000/doughnut.png"),
            url("https://img.icons8.com/fluency/48/000000/croissant.png");
        background-repeat: repeat;
        background-attachment: fixed;
        animation: bgMove 60s linear infinite;
        font-family: 'sans-serif';
    }

    @keyframes bgMove {
        from { background-position: 0 0; }
        to { background-position: 500px 1000px; }
    }

    header, footer, #MainMenu {visibility: hidden;}

    /* 磨砂玻璃卡片 */
    .glass-card {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(15px);
        border-radius: 40px;
        padding: 50px;
        border: 2px solid rgba(255, 255, 255, 0.5);
        box-shadow: 0 25px 50px rgba(0,0,0,0.05);
        text-align: center;
        margin-bottom: 30px;
    }

    .cute-title {
        font-family: 'ZCOOL XiaoWei', serif;
        font-size: 2.8rem;
        color: #d4a76c;
        margin-bottom: 10px;
        letter-spacing: 5px;
    }

    /* 输入框：极简呼吸感 */
    .stTextArea textarea {
        background-color: rgba(255, 255, 255, 0.8) !important;
        border: 2px solid #f2e1d1 !important;
        border-radius: 25px !important;
        color: #7d5a5a !important;
        font-size: 1.2rem !important;
        padding: 25px !important;
        transition: 0.3s;
    }
    .stTextArea textarea:focus {
        border-color: #d4a76c !important;
        box-shadow: 0 0 20px rgba(212, 167, 108, 0.2) !important;
    }

    /* 按钮：马卡龙色系豪华版 */
    .stButton > button {
        background: linear-gradient(135deg, #f2e1d1 0%, #d4a76c 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 15px 60px !important;
        font-size: 1.1rem !important;
        letter-spacing: 3px;
        box-shadow: 0 10px 20px rgba(212, 167, 108, 0.3) !important;
    }
    .stButton > button:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 30px rgba(212, 167, 108, 0.5) !important;
    }

    /* 圣光闪烁心理卡片 */
    .divine-card {
        background: white;
        border-radius: 30px;
        padding: 50px;
        color: #634d34;
        border: 1px solid #f2e1d1;
        position: relative;
        animation: divineGlow 3s infinite alternate;
    }
    @keyframes divineGlow {
        from { box-shadow: 0 0 20px rgba(212, 167, 108, 0.2); }
        to { box-shadow: 0 0 60px rgba(212, 167, 108, 0.6), 0 0 20px rgba(255, 255, 255, 1); }
    }
    </style>
    """, unsafe_allow_html=True)

# 2. 会话管理
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'answers' not in st.session_state:
    st.session_state.answers = []

scenes = [
    {"icon": "🥧", "title": "原生底色", "q": "童年记忆里，那个最让你安心的味道或画面是什么？"},
    {"icon": "🧁", "title": "闪光时刻", "q": "哪一刻，你觉得自己像刚出炉的甜点一样备受瞩目？"},
    {"icon": "☕", "title": "至暗瞬间", "q": "有没有什么时候，生活让你尝到了烧焦般的苦涩？"},
    {"icon": "🥐", "title": "身体警报", "q": "当你感到压力时，身体哪个部位会先绷得紧紧的？"},
    {"icon": "🍩", "title": "重要他人", "q": "生命中那个让你爱恨交织的人，他像哪种味道的甜品？"},
    {"icon": "🥨", "title": "循环怪圈", "q": "有什么不开心的行为模式，是你一直在重复品尝的？"}
]

# 3. 逻辑渲染
if st.session_state.step < len(scenes):
    s = scenes[st.session_state.step]
    
    st.markdown(f'''
        <div class="glass-card">
            <div style="font-size: 5rem; margin-bottom: 20px;">{s['icon']}</div>
            <div class="cute-title">{s['title']}</div>
            <p style="color: #d4a76c; font-weight: bold; margin-bottom: 20px;">{st.session_state.step + 1} / 6</p>
            <h3 style="color: #634d34; line-height: 1.5;">{s['q']}</h3>
        </div>
    ''', unsafe_allow_html=True)
    
    ans = st.text_area("", key=f"ans_{st.session_state.step}", height=150, label_visibility="collapsed", placeholder="请品尝并记录...")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("继续品尝 ✨"):
            if ans:
                st.session_state.answers.append(ans)
                st.session_state.step += 1
                st.rerun()
            else:
                st.warning("请留下您的品鉴词...")

else:
    st.markdown('<div class="cute-title" style="text-align:center; margin-top:50px;">档案馆封存完成</div>', unsafe_allow_html=True)
    
    if st.button("读取我的甜品报告 📖"):
        with st.spinner("MindMemo 正在冲洗您的心理胶片..."):
            try:
                client = OpenAI(api_key=st.secrets["DEEPSEEK_API_KEY"], base_url="https://api.deepseek.com")
                full_context = "\n".join(st.session_state.answers)
                
                prompt = f"""
                你是一个名为 "MindMemo" 的后台心理分析引擎。
                任务：根据输入生成一张极其深刻、简短的“心理卡片”。
                分析视角：ACT + CBT。
                输入：{full_context}
                格式：
                ### 🏷️ 智能标签
                ### 🧠 思维侦探 (CBT视角)
                ### 🍃 接纳与行动 (ACT视角)
                """
                
                response = client.chat.completions.create(model="deepseek-chat", messages=[{"role": "user", "content": prompt}])
                
                st.markdown(f'''
                    <div class="divine-card">
                        <div style="text-align:center; font-family:ZCOOL XiaoWei; font-size:1.5rem; color:#d4a76c; margin-bottom:30px;">🍮 您的心理考古卡片</div>
                        {response.choices[0].message.content}
                    </div>
                ''', unsafe_allow_html=True)
                
                # 重新测试按钮：回到开头
                if st.button("重新入座品尝 🔄"):
                    st.session_state.step = 0
                    st.session_state.answers = []
                    st.rerun()
            except Exception as e:
                st.error("引擎暂时离线，请重新尝试。")
