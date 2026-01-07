import streamlit as st
from openai import OpenAI # DeepSeek API 兼容 OpenAI 库

# --- 页面配置：王家卫风格 ---
st.set_page_config(
    page_title="生命叙事档案馆",
    page_icon="🎞️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 自定义 CSS 注入，打造王家卫电影感
st.markdown("""
    <style>
    /* 全局背景和字体 */
    body {
        background-color: #1a1a1a; /* 深色背景 */
        color: #d4a76c; /* 琥珀色文字 */
        font-family: 'Times New Roman', serif; /* 复古衬线字体 */
    }
    .stApp {
        background-image: url("https://example.com/your_bg_image.jpg"); /* 替换为你的背景图片链接 */
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
    }
    .st-emotion-cache-zt5ig8 { /* Streamlit main container */
        background-color: rgba(0, 0, 0, 0.75); /* 半透明深色背景，突出文字 */
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.4);
    }
    h1, h2, h3, h4, h5, h6 {
        color: #d4a76c; /* 标题琥珀色 */
        font-family: 'Georgia', serif;
        border-bottom: 1px solid rgba(212, 167, 108, 0.3); /* 标题下划线 */
        padding-bottom: 0.5rem;
        margin-bottom: 1.5rem;
    }
    .stTextArea > label {
        color: #d4a76c; /* 输入框标签颜色 */
        font-size: 1.1em;
        font-weight: bold;
    }
    .stTextArea textarea {
        background-color: rgba(30, 30, 30, 0.9); /* 输入框深色背景 */
        color: #f0f0f0; /* 输入文字白色 */
        border: 1px solid #d4a76c;
        border-radius: 5px;
        padding: 10px;
    }
    .stButton > button {
        background-color: #8c2a2a; /* 按钮深红色 */
        color: white;
        border-radius: 5px;
        border: none;
        padding: 10px 20px;
        font-size: 1.1em;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #a03c3c; /* 按钮悬停效果 */
    }
    .stAlert {
        background-color: rgba(200, 50, 50, 0.2);
        color: #d4a76c;
        border-left: 5px solid #d4a76c;
    }
    .report-box {
        background-color: rgba(40, 40, 40, 0.8);
        border: 1px solid #d4a76c;
        border-radius: 8px;
        padding: 1.5rem;
        margin-top: 2rem;
        font-style: italic;
        line-height: 1.6;
        white-space: pre-wrap; /* 保留AI输出的格式 */
    }
    /* Logo 样式 */
    .logo-container {
        text-align: center;
        margin-bottom: 2rem;
    }
    .logo {
        max-width: 150px;
        filter: drop-shadow(0 0 8px rgba(212, 167, 108, 0.6)); /* 琥珀色阴影 */
    }
    </style>
    """, unsafe_allow_html=True)

# --- DeepSeek API 配置 ---
try:
    client = OpenAI(
        api_key=st.secrets["DEEPSEEK_API_KEY"],
        base_url="https://api.deepseek.com"
    )
except KeyError:
    st.error("密钥库尚未开启，请检查后台配置 `DEEPSEEK_API_KEY`。")
    st.stop() # 如果没有Key，停止程序运行
except Exception as e:
    st.error(f"DeepSeek API 连接失败：{e}")
    st.stop()

# --- Logo 和标题 ---
st.markdown('<div class="logo-container"><img src="https://example.com/your_logo.png" class="logo"></div>', unsafe_allow_html=True)
st.title("🎞️ 生命叙事档案馆")
st.markdown("---")
st.markdown("""
    <p style="font-style: italic; text-align: center; color: rgba(212, 167, 108, 0.8);">
    “那些消逝了的岁月，仿佛隔着一块块蒙了尘的玻璃，看得到，抓不着。
    他一直在怀念着过去的一切。如果他能够回去，他不会让这些回忆留下。”
    </p>
    """, unsafe_allow_html=True)
st.markdown("---")

# --- 5 个灵魂拷问 ---
st.header("⏳ 记忆碎片收集")

ans1 = st.text_area("1. 如果现在要把你人生中最快乐的一个瞬间拍成一张照片，那张照片里画的是什么？", height=80)
ans2 = st.text_area("2. 如果有另一个你，他做了当初你‘没敢做’的选择，他现在过着什么样的生活？", height=80)
ans3 = st.text_area("3. 在外面忙碌了一整天，当你回到家关上门，瘫在沙发上，你脑子里跳出的第一个念头是什么？", height=80)
ans4 = st.text_area("4. 大家都觉得你是一个什么样的人？而你觉得，他们其实‘误解’了你的哪一部分？", height=80)
ans5 = st.text_area("5. 如果不考虑钱和时间，在这个周末，你最想去做的一件‘没意义但让你开心’的小事是什么？", height=80)

# --- 提交按钮 ---
st.markdown("---")
if st.button("封存档案，开始重构"):
    if not all([ans1, ans2, ans3, ans4, ans5]):
        st.warning("档案碎片尚不完整，请填写所有问题。")
    else:
        with st.spinner("档案馆正在调取深度数据，光影交错间，记忆被重构..."):
            # DeepSeek 的强大 Prompt 设计 (王家卫风格)
            prompt = f"""
            你是一位深邃的叙事考古学家、电影导演和心理重构师，拥有王家卫电影般的独特视角和文笔。
            用户提供了五个生命碎片：
            1. 记忆闪光：{ans1}
            2. 平行人生：{ans2}
            3. 疲惫瞬间：{ans3}
            4. 自我认知：{ans4}
            5. 微小愿望：{ans5}
            
            请基于这些碎片，生成一份文学化、哲学化、充满破碎感和时间感的叙事报告。
            报告要像一部电影的独白或旁白，用第三人称视角，重构这个人的生命基调和内心世界。
            不要给出任何建议或说教，只呈现故事、情感和未解的悬念。
            用词要富有诗意，带有都市疏离感和淡淡的哀愁，仿佛是在解读一份被时间遗忘的档案。
            篇幅控制在200-300字。
            """
            
            try:
                response = client.chat.completions.create(
                    model="deepseek-chat", # 使用 deepseek-chat 模型
                    messages=[{"role": "user", "content": prompt}],
                    stream=False
                )
                st.markdown("### 🖋️ 重构报告")
                st.markdown(f'<div class="report-box">{response.choices[0].message.content}</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"连接失败，请检查DeepSeek API配置或网络连接：{str(e)}")
