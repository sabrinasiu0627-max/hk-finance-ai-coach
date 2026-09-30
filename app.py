import streamlit as st
import pandas as pd
from huggingface_hub import InferenceClient

# 網頁基本設定
st.set_page_config(page_title="HK Finance AI Coach", page_icon="⚡", layout="wide")

# --- Apple 風格自訂 CSS (極簡黑白、純白背景、幼線外框) ---
st.markdown("""
<style>
    /* 全局 Apple 簡約字體與純白背景 */
    .stApp {
        background-color: #FFFFFF;
        color: #111111;
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Helvetica Neue", Arial, sans-serif;
    }
    
    /* 標題與文字微調 */
    h1, h2, h3, h4 {
        color: #000000;
        font-weight: 600;
        letter-spacing: -0.02em;
    }

    /* 側邊欄風格 */
    [data-testid="stSidebar"] {
        background-color: #FAFAFA;
        border-right: 1px solid #E5E5E7;
    }

    /* 蘋果風線框卡片 (黑線、白底、圓角) */
    .apple-card {
        border: 1px solid #000000;
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 20px;
    }

    /* 按鈕：極簡黑底白字 */
    .stButton > button {
        background-color: #000000 !important;
        color: #FFFFFF !important;
        border: 1px solid #000000 !important;
        border-radius: 6px !important;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    .stButton > button:hover {
        background-color: #333333 !important;
        border-color: #333333 !important;
    }

    /* 輸入框邊框 */
    input, textarea, select {
        border: 1px solid #CCCCCC !important;
        border-radius: 6px !important;
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }
    input:focus {
        border-color: #000000 !important;
        box-shadow: none !important;
    }

    /* 俐落的黑色分隔線 */
    hr {
        border: none;
        height: 1px;
        background-color: #000000;
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)

# 頁面標題
st.title("⚡ HK Finance AI Coach")
st.write("Minimalist & Data-Driven Financial Intelligence.")

# 預設直接使用你提供的 Hugging Face Token
default_hf_token = "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"

with st.sidebar:
    st.header("⚙️ System Settings")
    api_key = st.text_input("Hugging Face Token", value=default_hf_token, type="password")

if api_key:
    client = InferenceClient(api_key=api_key)
else:
    st.warning("⚠️ 請輸入 Hugging Face Token。")

# --- 側邊欄：理財檔案資料輸入 ---
st.sidebar.header("📋 Client Profile")

with st.sidebar.expander("1. 基本資料", expanded=False):
    age = st.text_input("年齡", "28")
    occupation = st.text_input("職業", "文職")
    
with st.sidebar.expander("2. 薪金與現金流", expanded=True):
    salary_before_mpf = st.number_input("薪金（MPF前 HKD）", value=30000, step=1000)
    salary_after_mpf = st.number_input("薪金（MPF後 HKD）", value=28500, step=1000)
    monthly_expense = st.number_input("每月總開支 (HKD)", value=12000, step=500)
    monthly_saving = st.number_input("每月儲蓄 (HKD)", value=16500, step=500)

with st.sidebar.expander("3. 資產與負債", expanded=True):
    bank_balance = st.number_input("銀行戶口及餘額 (HKD)", value=100000)
    cash = st.number_input("現金 (HKD)", value=5000)
    stocks = st.number_input("股票／ETF (HKD)", value=150000)
    mpf = st.number_input("強積金 (HKD)", value=80000)
    liabilities = st.number_input("負債（卡數／貸款 HKD）", value=0)

with st.sidebar.expander("4. 目標與背景", expanded=False):
    short_term_goal = st.text_input("短期目標（1年內）", "存夠 20 萬備用金")
    mid_term_goal = st.text_input("中期目標（2–5年）", "儲首期買樓／結婚")
    family_burden = st.text_input("家庭狀況（家用等）", "每月給家用 5000")
    risk_tolerance = st.selectbox("風險承受能力", ["保守", "中等", "進取"], index=1)

# --- 即時計算核心數據 ---
total_liquid_assets = bank_balance + cash + stocks
net_worth = total_liquid_assets + mpf - liabilities
savings_rate = (monthly_saving / salary_after_mpf) * 100 if salary_after_mpf > 0 else 0

# --- 主畫面儀表板數據展示 (Apple 框線卡片風格) ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("每月儲蓄率", f"{savings_rate:.1f}%")
col2.metric("總流動資產", f"${total_liquid_assets:,.0f}")
col3.metric("淨資產總值", f"${net_worth:,.0f}")
col4.metric("預測1年增長", f"${(monthly_saving * 12):,.0f}")

st.markdown("<hr>", unsafe_allow_html=True)

# --- AI Persona Prompt ---
system_persona = f"""
你現在擔任一個香港理財教練 AI，請用香港繁體中文加適量廣東話回應（例如：用「咁」、「囉」、「冇」、「同埋」、「計計條數」等），幫用戶建立同追蹤理財檔案。

以下係用戶嘅基本資料。請記住呢啲數字同時間線，往後對話直接引用，唔好重複問基本資料：
- 年齡：{age}
- 職業：{occupation}
- 薪金（MPF後）：${salary_after_mpf:,.0f}
- 每月總開支：${monthly_expense:,.0f}
- 每月儲蓄：${monthly_saving:,.0f}（儲蓄率：{savings_rate:.1f}%）
- 總流動資產：${total_liquid_assets:,.0f}
- 負債：${liabilities:,.0f}
- 短期目標：{short_term_goal}
- 中期目標：{mid_term_goal}
- 家庭狀況：{family_burden}
- 風險承受能力：{risk_tolerance}

每次回覆要具體、有數字、可執行，避免空泛建議。
"""

# --- 按鈕觸發：建立檔案與自動化系統設計 ---
if st.button("🚀 啟動 AI 智能理財架構分析", type="primary"):
    if api_key:
        with st.spinner("AI 理財教練正在精密分析資產結構中..."):
            try:
                task_prompt = system_persona + """
                請根據以上用戶資料，立即幫用戶完成以下 3 個指定任務：
                1. 建立理財檔案總結；
                2. 計算儲蓄率同資產增長推算（1年、3年）；
                3. 設計具體嘅自動化儲蓄系統方案（例如出糧自動轉賬分配、各戶口分配比例）。
                """
                messages = [
                    {"role": "system", "content": "你是一個專業、貼地的香港理財教練，請用廣東話同香港繁體中文回答。"},
                    {"role": "user", "content": task_prompt}
                ]
                
                response = client.chat.completions.create(
                    model="meta-llama/Meta-Llama-3-8B-Instruct",
                    messages=messages,
                    max_tokens=1000
                )
                st.success("分析完成！")
                st.markdown(f'<div class="apple-card">{response.choices[0].message.content}</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"發生錯誤：{e}")
    else:
        st.error("請先輸入 API Key！")

st.markdown("<hr>", unsafe_allow_html=True)

# --- AI 互動教練對話區 ---
st.subheader("💬 AI 財務對話空間")
st.write("向你的專屬教練提問，例如：「我呢個洗費水平夠唔夠買樓？」")

user_question = st.text_input("輸入你想問教練的問題：")
if user_question and api_key:
    if st.button("發送查詢"):
        with st.spinner("教練思考中..."):
            try:
                chat_messages = [
                    {"role": "system", "content": system_persona},
                    {"role": "user", "content": user_question}
                ]
                chat_response = client.chat.completions.create(
                    model="meta-llama/Meta-Llama-3-8B-Instruct",
                    messages=chat_messages,
                    max_tokens=1000
                )
                st.markdown(f'<div class="apple-card">{chat_response.choices[0].message.content}</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"發生錯誤：{e}")
