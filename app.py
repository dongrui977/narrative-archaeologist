import streamlit as st
from openai import OpenAI

# 1. 基础配置与王家卫风格 CSS
st.set_page_config(page_title="生命叙事档案馆", page_icon="🎞️", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #d4a76c; }
    /* 隐藏所有多余的 Streamlit 组件 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* 电影感文字样式 */
    .movie-text {
        font-family: 'Courier New', Courier, monospace;
        font-size: 1.5rem;
        line-height: 2;
        text-align: center;
        margin-top: 100px;
        color: #d4a76c;
        text-shadow: 0 0 10px rgba(212, 167, 108, 0.5);
    }
    
    /* 输入框样式微调 */
    .stTextArea textarea {
        background-color: transparent !important;
        color: #f0f0f0 !important;
        border: none !important;
        border-bottom: 1px solid #d4a76c !important;
        text-align: center;
        font-size: 1.2rem;
    }
    
    /* 下一幕按钮样式 */
    .stButton>button {
        background-color: transparent !important;
        color: #d4a76c !important;
        border: 1px solid #d4a76c !important;
        border-radius: 0px !important;
        width: 150px;
        margin: 0 auto;
        display: block;
    }
    .stButton>button:hover {
        background-color: #d4a76c !important;
        color: black !important;
    }
    
    .report-box {
        border: 1px solid #d4a76c;
        padding: 30px;
        font-style: italic;
        line-height: 2;
        margin-top: 50px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. 初始化状态
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'answers' not in st.session_state:
    st.session_state.answers = []

questions = [
    "第一幕：\n如果现在要把你人生中最快乐的一个瞬间拍成一张照片，\n那张照片里画的是什么？",
    "第二幕：\n如果有一个平行世界里的你，\n做了那个你当初‘没敢做’的选择，他现在过着什么样的生活？",
    "第三幕：\n当你忙碌一天回到家关上门，瘫在沙发上，\n脑子里跳出的第一个念头是什么？",
    "第四幕：\n外界总觉得你理智，但你觉得，\n他们其实‘误解’了你的哪一部分？",
    "第五幕：\n如果不考虑钱和时间，在这个周末，\n你最想去做的一件‘没意义但让你开心’的小事是什么？"
]

# 3. 逻辑分屏
try:
    client = OpenAI(api_key=st.secrets["DEEPSEEK_API_KEY"], base_url="https://api.deepseek.com")
except:
    st.error("密钥未配置")
    st.stop()

# --- 场景渲染 ---
if st.session_state.step < len(questions):
    # 显示当前问题
    st.markdown(f'<div class="movie-text">{questions[st.session_state.step]}</div>', unsafe_allow_html=True)
    
    # 输入框
    ans = st.text_area("", placeholder="请在这里输入记忆的碎片...", key=f"input_{st.session_state.step}", label_visibility="collapsed")
    
    # 按钮居中
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        btn_label = "封存档案" if st.session_state.step == 4 else "下一幕"
        if st.button(btn_label):
            if ans:
                st.session_state.answers.append(ans)
                st.session_state.step += 1
                st.rerun()
            else:
                st.warning("请留下些什么...")

# --- 最终封存场景 ---
else:
    st.markdown('<div class="movie-text">. . . 档案馆正在封存 . . .</div>', unsafe_allow_html=True)
    
    # 放置封存图标 (使用 Emoji 模拟仪式感)
    st.markdown("<h1 style='text-align: center; cursor: pointer;'>🧧</h1>", unsafe_allow_html=True)
    
    if st.button("查看重构报告"):
        with st.spinner("光影交错间，记忆正在被重编..."):
            all_ans = st.session_state.answers
            prompt = f"""
            你是一位王家卫风格的叙事重构师。
            碎片如下：快乐瞬间:{all_ans[0]}, 平行世界:{all_ans[1]}, 归家念头:{all_ans[2]}, 真实自我:{all_ans[3]}, 隐秘渴望:{all_ans[4]}。
            请用第三人称电影旁白的形式，写一段200字左右的叙事报告。要破碎、要诗意，不要建议。
            """
            
            try:
                response = client.chat.completions.create(model="deepseek-chat", messages=[{"role": "user", "content": prompt}])
                st.markdown(f'<div class="report-box">{response.choices[0].message.content}</div>', unsafe_allow_html=True)
                
                # 重来一次
                if st.button("重启档案"):
                    st.session_state.step = 0
                    st.session_state.answers = []
                    st.rerun()
            except Exception as e:
                st.error(f"连接失败: {e}")
