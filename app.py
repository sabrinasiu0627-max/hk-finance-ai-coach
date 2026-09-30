import streamlit as st
import pandas as pd
import time
from huggingface_hub import InferenceClient

# 網頁基本設定
st.set_page_config(page_title="HK Finance AI Coach", page_icon="", layout="wide")

# 極致清晰 Apple 黑白風 CSS (徹底解決 Highlight 變黑、Hover 顏色、按鈕與選取反白問題)
st.markdown("""
<style>
    /* 全局純白背景與深黑清晰字體 */
    .stApp {
        background-color: #FFFFFF !important;
        color: #111111 !important;
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Helvetica Neue", Arial, sans-serif;
    }
    
    /* 文字、標題與標籤顏色鎖死清晰 */
    h1, h2, h3, h4, h5, h6, p, label, span, div {
        color: #111111;
    }

    /* 徹底修正反白選取顏色 (避免選取時變黑色搞到乜都睇唔到) */
    ::selection {
        background-color: #000000 !important;
        color: #FFFFFF !important;
    }

    /* 側邊欄風格 */
    [data-testid="stSidebar"] {
        background-color: #FBFBFD !important;
        border-right: 1px solid #D2D2D7 !important;
    }
    [data-testid="stSidebar"] * {
        color: #111111 !important;
    }

    /* 數據儀表板數字與標籤 */
    [data-testid="stMetricValue"], [data-testid="stMetricLabel"] {
        color: #000000 !important;
    }

    /* Apple 框線卡片：白底填色 + 黑色幼線外框 */
    .apple-card {
        border: 1px solid #111111;
        background-color: #FFFFFF;
        padding: 24px;
        border-radius: 12px;
        margin-bottom: 24px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02);
    }
    .apple-card * {
        color: #111111 !important;
    }

    /* 修正 Code 區塊與 Highlight 顏色，確保字體清晰可見 */
    code, pre {
        background-color: #F1F1F3 !important;
        color: #111111 !important;
        border-radius: 6px;
        padding: 2px 6px;
    }

    /* === 按鈕設定：未 hover 前純白底 + 黑色幼邊框；Hover 時極淺灰，文字永久清晰 === */
    div.stButton > button, 
    div.stFormSubmitButton > button {
        background-color: #FFFFFF !important;
        color: #111111 !important;
        border: 1px solid #111111 !important;
        border-radius: 8px !important;
        padding: 0.5rem 1.2rem !important;
        font-weight: 500 !important;
        box-shadow: none !important;
        outline: none !important;
        transition: all 0.2s ease !important;
    }
    
    div.stButton > button:hover, 
    div.stFormSubmitButton > button:hover {
        background-color: #F5F5F7 !important;
        color: #111111 !important;
        border: 1px solid #111111 !important;
        box-shadow: none !important;
    }
    
    div.stButton > button:focus, 
    div.stButton > button:active,
    div.stFormSubmitButton > button:focus, 
    div.stFormSubmitButton > button:active {
        background-color: #FFFFFF !important;
        color: #111111 !important;
        border: 1px solid #111111 !important;
        box-shadow: none !important;
        outline: none !important;
    }

    /* 側邊欄與主畫面 Expander (摺疊選單) 樣式 */
    [data-testid="stExpander"] {
        border: 1px solid #D2D2D7 !important;
        border-radius: 8px !important;
        background-color: #FFFFFF !important;
        margin-bottom: 10px;
    }
    [data-testid="stExpander"] summary {
        background-color: #FFFFFF !important;
        color: #111111 !important;
        border-radius: 8px !important;
    }
    [data-testid="stExpander"] summary:hover {
        background-color: #F5F5F7 !important;
        color: #111111 !important;
    }
    [data-testid="stExpander"] summary * {
        color: #111111 !important;
    }

    /* 輸入框幼線設計 */
    input, textarea, select {
        border: 1px solid #D2D2D7 !important;
        border-radius: 8px !important;
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }
    input:focus {
        border-color: #000000 !important;
        box-shadow: none !important;
    }

    /* 極細分隔線 */
    hr {
        border: none;
        height: 1px;
        background-color: #D2D2D7;
        margin: 2.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

st.title("HK Finance AI 理財教練")
st.write("結合個人資產數據與智能分析的極簡理財系統。")

default_hf_token = "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"

with st.sidebar:
    st.header("系統設定")
    api_key = st.text_input("Hugging Face Token", value=default_hf_token, type="password")

if api_key:
    client = InferenceClient(api_key=api_key)
else:
    st.warning("請輸入你的 Hugging Face Token。")

st.sidebar.header("客戶理財檔案")

with st.sidebar.expander("1. 基本資料", expanded=False):
    age = st.text_input("年齡", "28")
    occupation = st.text_input("職業", "文職")
    
with st.sidebar.expander("2. 薪金與現金流 (MPF自動計算)", expanded=True):
    salary_before_mpf = st.number_input("每月薪金（MPF前 HKD）", value=30000, step=1000)
    
    # 香港 MPF 自動計算邏輯：5% 供款，最高入息水平 $30,000 對應上限 $1,500（註：實報最高上限以 30000 計算為 1500）
    mpf_deduction = min(salary_before_mpf * 0.05, 1500) if salary_before_mpf >= 7100 else 0
    salary_after_mpf = salary_before_mpf - mpf_deduction
    
    st.caption(f"自動計算 MPF 扣除: ${mpf_deduction:,.0f}")
    st.markdown(f"**實收薪金 (MPF後): ${salary_after_mpf:,.0f}**")
    
    monthly_expense = st.number_input("每月總開支 (HKD)", value=12000, step=500)
    monthly_saving = salary_after_mpf - monthly_expense
    st.info(f"自動計算每月淨儲蓄: ${monthly_saving:,.0f}")

with st.sidebar.expander("3. 資產與負債", expanded=True):
    bank_balance = st.number_input("銀行戶口及餘額 (HKD)", value=100000)
    cash = st.number_input("現金 (HKD)", value=5000)
    stocks = st.number_input("股票／ETF (HKD)", value=150000)
    mpf = st.number_input("現有強積金總額 (HKD)", value=80000)
    liabilities = st.number_input("負債（卡數／貸款 HKD）", value=0)

with st.sidebar.expander("4. 目標與背景", expanded=False):
    short_term_goal = st.text_input("短期目標（1年內）", "存夠 20 萬備用金")
    mid_term_goal = st.text_input("中期目標（2-5年）", "儲首期買樓／結婚")
    family_burden = st.text_input("家庭狀況（家用等）", "每月給家用 5000")
    risk_tolerance = st.selectbox("風險承受能力", ["保守", "中等", "進取"], index=1)

total_liquid_assets = bank_balance + cash + stocks
net_worth = total_liquid_assets + mpf - liabilities
savings_rate = (monthly_saving / salary_after_mpf) * 100 if salary_after_mpf > 0 else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("每月儲蓄率", f"{savings_rate:.1f}%")
col2.metric("總流動資產", f"${total_liquid_assets:,.0f}")
col3.metric("淨資產總值", f"${net_worth:,.0f}")
col4.metric("預測1年資產增長", f"${(monthly_saving * 12):,.0f}")

st.markdown("<hr>", unsafe_allow_html=True)

# 嚴格約束 AI 計算與回覆風格，防止 9 唔搭八
system_persona = f"""
你是一個極度精準、專業且貼地的香港持牌理財教練。
請嚴格使用以下提供的實質數據進行財務分析與推算，絕對不可胡亂猜測或給出與數據不符的數學計算：

【用戶財務硬數據】
- 年齡：{age}
- 職業：{occupation}
- 薪金（MPF前）：${salary_before_mpf:,.0f}
- MPF扣除：${mpf_deduction:,.0f}
- 薪金（MPF後實收）：${salary_after_mpf:,.0f}
- 每月總開支：${monthly_expense:,.0f}
- 每月淨儲蓄：${monthly_saving:,.0f} （儲蓄率：{savings_rate:.1f}%）
- 總流動資產（現金+銀行+股票）：${total_liquid_assets:,.0f}
- 強積金(MPF)總額：${mpf:,.0f}
- 負債：${liabilities:,.0f}
- 淨資產總值：${net_worth:,.0f}
- 短期目標：{short_term_goal}
- 中期目標：{mid_term_goal}
- 家庭負擔：{family_burden}
- 風險承受能力：{risk_tolerance}

【回覆規則】
1. 必須使用廣東話與香港繁體中文（例如：「咁」、「囉」、「同埋」、「計計條數」）。
2. 所有涉及的金額與增長計算必須與上方提供的數據 100% 吻合，絕不能虛構數字。
3. 語氣要專業、實際、直接點出痛點並給出具體可執行建議。
"""

if st.button("執行 AI 理財架構分析"):
    if api_key:
        # 進度條實作
        progress_bar = st.progress(0, text="正在初始化理財引擎...")
        time.sleep(0.2)
        progress_bar.progress(30, text="正在讀取用戶資產與自動計算現金流...")
        time.sleep(0.3)
        progress_bar.progress(60, text="AI 教練正在進行精準財務模型運算...")
        
        try:
            task_prompt = system_persona + """
            請根據以上真實數據，為用戶完成以下 3 個指定任務：
            1. 理財健康狀況總結（點評儲蓄率與資產結構）；
            2. 資產增長推算（精確計算 1 年後及 3 年後的淨資產總值增長）；
            3. 具體自動化儲蓄分配方案（建議出糧後各戶口的分帳比例）。
            """
            messages = [
                {"role": "system", "content": "你是一個專業、數學精確的香港理財教練，嚴格依賴用戶給出的數字回答。"},
                {"role": "user", "content": task_prompt}
            ]
            
            progress_bar.progress(85, text="正在生成貼地廣東話分析報告...")
            response = client.chat.completions.create(
                model="meta-llama/Llama-3.1-8B-Instruct",
                messages=messages,
                max_tokens=1000
            )
            
            progress_bar.progress(100, text="分析完成！")
            time.sleep(0.3)
            progress_bar.empty()
            
            st.success("分析完成")
            st.markdown(f'<div class="apple-card">{response.choices[0].message.content}</div>', unsafe_allow_html=True)
        except Exception as e:
            progress_bar.empty()
            st.error(f"發生錯誤：{e}")
    else:
        st.error("請先輸入 API Key。")

st.markdown("<hr>", unsafe_allow_html=True)

st.subheader("AI 財務諮詢對話")
st.write("向你的專屬教練提問，例如：「我呢個洗費水平夠唔夠買樓？」")

user_question = st.text_input("輸入你的問題：")
if user_question and api_key:
    if st.button("發送查詢"):
        chat_progress = st.progress(0, text="教練思考中...")
        chat_progress.progress(50, text="正在分析您的提問與理財檔案...")
        try:
            chat_messages = [
                {"role": "system", "content": system_persona},
                {"role": "user", "content": user_question}
            ]
            chat_response = client.chat.completions.create(
                model="meta-llama/Llama-3.1-8B-Instruct",
                messages=chat_messages,
                max_tokens=1000
            )
            chat_progress.progress(100, text="完成！")
            time.sleep(0.2)
            chat_progress.empty()
            
            st.markdown(f'<div class="apple-card">{chat_response.choices[0].message.content}</div>', unsafe_allow_html=True)
        except Exception as e:
            chat_progress.empty()
            st.error(f"發生錯誤：{e}")
