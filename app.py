import streamlit as st
from openai import OpenAI

# 1. 视觉黑科技：复古甜点包装盒质感
st.set_page_config(page_title="MindMemo | Dessert Archive", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=ZCOOL+XiaoWei&family=Noto+Serif+SC:wght@300;600&display=swap');

    /* 全局背景：复古丝绒粉 */
    .stApp {
        background-color: #F8E1E7;
        background-image: radial-gradient(#F4CAD6 1px, transparent 1px);
        background-size: 20px 20px;
        color: #7D5A5A;
        font-family: 'Noto Serif SC', serif;
    }

    header, footer, #MainMenu {visibility: hidden;}

    /* 复古包装盒容器 */
    .dessert-box {
        background: #FFFFFF;
        border: 4px double #F4CAD6;
        border-radius: 4px;
        padding: 60px 40px;
        box-shadow: 15px 15px 0px #F4CAD6;
        text-align: center;
        margin-top: 40px;
        position: relative;
    }

    /* 3D 浮动图标 */
    .dessert-icon {
        font-size: 5rem;
        margin-bottom: 20px;
        filter: drop-shadow(0 10px 10px rgba(125, 90, 90, 0.2));
        animation: floating 3s ease-in-out infinite;
    }
    @keyframes floating {
        0%, 100% { transform: translateY(0) rotate(0deg); }
        50% { transform: translateY(-15px) rotate(5deg); }
    }

    .box-title {
        font-family: 'ZCOOL XiaoWei', serif;
        font-size: 2.2rem;
        letter-spacing: 5px;
        color: #7D5A5A;
        margin-bottom: 10px;
    }

    /* 极简输入框：像在信纸上书写 */
    .stTextArea textarea {
        background-color: transparent !important;
        border: none !important;
        border-bottom: 1px dashed #F4CAD6 !important;
        color: #7D5A5A !important;
        font-size: 1.15rem !important;
        text-align: center !important;
        border-radius: 0 !important;
        padding: 20px !important;
    }
    .stTextArea textarea:focus {
        border-bottom: 1px solid #7D5A5A !important;
        box-shadow: none !important;
    }

    /* 按钮：复古火漆印章感 */
    .stButton > button {
        background-color: #7D5A5A !important;
        color: #F8E1E7 !important;
        border: none !important;
        border-radius: 0px !important;
        padding: 12px 40px !important;
        font-family: 'ZCOOL XiaoWei', serif !important;
        letter-spacing: 3px;
        box-shadow: 4px 4px 0px #F4CAD6;
        transition: 0.2s;
        margin-top: 30px;
    }
    .stButton > button:active {
        transform: translate(2px, 2px);
        box-shadow: 2px 2px 0px #F4CAD6;
    }

    /* 圣光闪烁心理卡片：烫金衬纸感 */
    .gold-memo {
        background: #FFF;
        padding: 50px;
        border: 1px solid #F4CAD6;
        box-shadow: 0 0 40px rgba(244, 202, 214, 0.5);
        animation: shine 4s infinite alternate;
        text-align: left;
    }
    @keyframes shine {
        from { box-shadow: 0 0 20px rgba(244, 202, 214, 0.3); }
        to { box-shadow: 0 0 60px rgba(244, 202, 214, 0.7), inset 0 0 20px rgba(244, 202, 214, 0.2); }
    }
    </style>
    """, unsafe_allow_html=True)

# 2. 会话管理
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'answers' not in st.session_state:
    st.session_state.answers = []

scenes = [
    {"icon": "🍮", "title": "原生底色", "q": "童年记忆里，那个最让你安心的味道或画面是什么？"},
    {"icon": "🍰", "title": "闪光瞬间", "q": "哪一次成就感，让你觉得自己像缀满珍珠的蛋糕？"},
    {"icon": "☕", "title": "至暗时刻", "q": "生活什么时候让你尝到了苦涩如隔夜咖啡的味道？"},
    {"icon": "🥨", "title": "身体警报", "q": "焦虑时，身体哪个部位会像烤过头的面团一样紧绷？"},
    {"icon": "🍬", "title": "重要他人", "q": "那个人给你的感觉，是哪种口味的甜蜜或辛辣？"},
    {"icon": "🍩", "title": "循环怪圈", "q": "有什么不开心的行为模式，是你一直在重复品尝的？"}
]

# 3. 逻辑渲染
if st.session_state.step < len(scenes):
    s = scenes[st.session_state.step]
    
    st.markdown(f'''
        <div class="dessert-box">
            <div class="dessert-icon">{s['icon']}</div>
            <div class="box-title">{s['title']}</div>
            <p style="opacity: 0.5; font-size: 0.8rem; letter-spacing: 2px;">MEMORANDUM SCENE 0{st.session_state.step + 1}</p>
            <h3 style="margin-top: 20px;">{s['q']}</h3>
        </div>
    ''', unsafe_allow_html=True)
    
    ans = st.text_area("", key=f"f_{st.session_state.step}", height=150, label_visibility="collapsed", placeholder="在此刻录您的真实叙事...")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("品尝下一幕" if st.session_state.step < 5 else "封存今日报告"):
            if ans:
                st.session_state.answers.append(ans)
                st.session_state.step += 1
                st.rerun()

else:
    st.markdown('<div class="box-title" style="text-align:center; margin-top:50px;">甜品盒已打包</div>', unsafe_allow_html=True)
    
    if st.button("开启您的心理卡片"):
        with st.spinner("MindMemo 正在提取认知脚本..."):
            try:
                client = OpenAI(api_key=st.secrets["DEEPSEEK_API_KEY"], base_url="https://api.deepseek.com")
                full_context = "\n".join(st.session_state.answers)
                
                # 执行 MindMemo 引擎逻辑
                prompt = f"""
                你是一个名为 "MindMemo" 的心理分析引擎。
                任务：生成极其简短、深刻的“心理卡片”。分析：{full_context}
                格式要求：
                ### 🏷️ 智能标签
                ### 🧠 思维侦探 (CBT)
                ### 🍃 接纳与行动 (ACT)
                """
                
                response = client.chat.completions.create(model="deepseek-chat", messages=[{"role": "user", "content": prompt}])
                
                st.markdown(f'''
                    <div class="gold-memo">
                        <div style="text-align:center; font-family:ZCOOL XiaoWei; color:#7D5A5A; border-bottom:1px solid #F4CAD6; padding-bottom:10px; margin-bottom:20px;">MINDMEMO REPORT</div>
                        {response.choices[0].message.content}
                    </div>
                ''', unsafe_allow_html=True)
                
                if st.button("重新入座品尝 🔄"):
                    st.session_state.step = 0
                    st.session_state.answers = []
                    st.rerun()
                    
            except Exception as e:
                st.error("引擎暂时离线。")
