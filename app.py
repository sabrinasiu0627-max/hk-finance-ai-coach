%%writefile app.py
import streamlit as st
import pandas as pd
from huggingface_hub import InferenceClient

# 網頁基本設定
st.set_page_config(page_title="HK Finance AI Coach", page_icon="■", layout="wide")

# --- Apple 極簡黑白風自訂 CSS (強制修復字體顏色與純白背景) ---
st.markdown("""
<style>
    /* 全局強制純白背景與深黑字體 */
    .stApp {
        background-color: #FFFFFF !important;
        color: #111111 !important;
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Helvetica Neue", Arial, sans-serif;
    }
    
    /* 強制所有文字、標題、標籤為黑灰色，杜絕白字隱形 */
    h1, h2, h3, h4, h5, h6, p, span, label, div {
        color: #111111 !important;
    }

    /* 側邊欄風格：淺灰底色、極細右邊框 */
    [data-testid="stSidebar"] {
        background-color: #FBFBFD !important;
        border-right: 1px solid #D2D2D7 !important;
    }
    [data-testid="stSidebar"] * {
        color: #111111 !important;
    }

    /* 數據儀表板數字與標籤強力修正 */
    [data-testid="stMetricValue"], [data-testid="stMetricLabel"] {
        color: #000000 !important;
    }

    /* Apple 風格線框卡片 (黑線、白底、圓角) */
    .apple-card {
        border: 1px solid #111111;
        background-color: #FFFFFF;
        padding: 24px;
        border-radius: 12px;
        margin-bottom: 24px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    }

    /* 按鈕：極簡黑底白字，Hover 時反轉為白底黑字 */
    .stButton > button {
        background-color: #000000 !important;
        color: #FFFFFF !important;
        border: 1px solid #000000 !important;
        border-radius: 8px !important;
        padding: 0.5rem 1.2rem;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    .stButton > button:hover {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 1px solid #000000 !important;
    }

    /* 輸入框與文字欄位幼線設計 */
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

    /* 俐落的極細分隔線 */
    hr {
        border: none;
        height: 1px;
        background-color: #D2D2D7;
        margin: 2.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# 頁面標題 (完全移除 Emoji)
st.title("HK Finance AI Coach")
st.write("Minimalist & Data-Driven Financial Intelligence.")

# 預設直接使用你提供的 Hugging Face Token
default_hf_token = "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"

with st.sidebar:
    st.header("System Settings")
    api_key = st.text_input("Hugging Face Token", value=default_hf_token, type="password")

if api_key:
    client = InferenceClient(api_key=api_key)
else:
    st.warning("Please enter your Hugging Face Token.")

# --- 側邊欄：理財檔案資料輸入 ---
st.sidebar.header("Client Profile")

with st.sidebar.expander("1. Basic Information", expanded=False):
    age = st.text_input("Age", "28")
    occupation = st.text_input("Occupation", "Office Professional")
    
with st.sidebar.expander("2. Income & Cash Flow", expanded=True):
    salary_before_mpf = st.number_input("Salary (Before MPF HKD)", value=30000, step=1000)
    salary_after_mpf = st.number_input("Salary (After MPF HKD)", value=28500, step=1000)
    monthly_expense = st.number_input("Monthly Expenses (HKD)", value=12000, step=500)
    monthly_saving = st.number_input("Monthly Savings (HKD)", value=16500, step=500)

with st.sidebar.expander("3. Assets & Liabilities", expanded=True):
    bank_balance = st.number_input("Bank Balance (HKD)", value=100000)
    cash = st.number_input("Cash (HKD)", value=5000)
    stocks = st.number_input("Stocks / ETFs (HKD)", value=150000)
    mpf = st.number_input("MPF (HKD)", value=80000)
    liabilities = st.number_input("Liabilities / Debt (HKD)", value=0)

with st.sidebar.expander("4. Goals & Background", expanded=False):
    short_term_goal = st.text_input("Short-term Goal (1 Year)", "Build 200k emergency fund")
    mid_term_goal = st.text_input("Mid-term Goal (2-5 Years)", "Save for property down payment / marriage")
    family_burden = st.text_input("Family Obligations", "Monthly family allowance 5000")
    risk_tolerance = st.selectbox("Risk Tolerance", ["Conservative", "Moderate", "Aggressive"], index=1)

# --- 即時計算核心數據 ---
total_liquid_assets = bank_balance + cash + stocks
net_worth = total_liquid_assets + mpf - liabilities
savings_rate = (monthly_saving / salary_after_mpf) * 100 if salary_after_mpf > 0 else 0

# --- 主畫面儀表板數據展示 (Apple 框線卡片風格) ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Savings Rate", f"{savings_rate:.1f}%")
col2.metric("Liquid Assets", f"${total_liquid_assets:,.0f}")
col3.metric("Net Worth", f"${net_worth:,.0f}")
col4.metric("Est. 1Y Growth", f"${(monthly_saving * 12):,.0f}")

st.markdown("<hr>", unsafe_allow_html=True)

# --- AI Persona Prompt ---
system_persona = f"""
You are a professional, pragmatic Hong Kong financial coach AI. Respond in traditional Chinese combined with natural conversational Cantonese terms (such as '咁', '囉', '冇', '同埋', '計計條數') to help the user track and build their financial profile.

User Profile:
- Age: {age}
- Occupation: {occupation}
- Salary (After MPF): ${salary_after_mpf:,.0f}
- Monthly Expenses: ${monthly_expense:,.0f}
- Monthly Savings: ${monthly_saving:,.0f} (Savings Rate: {savings_rate:.1f}%)
- Total Liquid Assets: ${total_liquid_assets:,.0f}
- Liabilities: ${liabilities:,.0f}
- Short-term Goal: {short_term_goal}
- Mid-term Goal: {mid_term_goal}
- Family Obligations: {family_burden}
- Risk Tolerance: {risk_tolerance}

Keep responses precise, data-driven, and actionable. Avoid vague advice.
"""

# --- 按鈕觸發：建立檔案與自動化系統設計 ---
if st.button("Run AI Financial Analysis"):
    if api_key:
        with st.spinner("Analyzing asset structure..."):
            try:
                task_prompt = system_persona + """
                Please complete the following 3 tasks based on the user's profile:
                1. Establish a financial profile summary;
                2. Calculate savings rate and asset growth projections (1 year, 3 years);
                3. Design a concrete automated savings system (e.g., auto-transfer proportions across accounts upon payday).
                """
                messages = [
                    {"role": "system", "content": "You are a professional, pragmatic Hong Kong financial coach, responding in Cantonese and Traditional Chinese."},
                    {"role": "user", "content": task_prompt}
                ]
                
                response = client.chat.completions.create(
                    model="meta-llama/Meta-Llama-3-8B-Instruct",
                    messages=messages,
                    max_tokens=1000
                )
                st.success("Analysis Complete")
                st.markdown(f'<div class="apple-card">{response.choices[0].message.content}</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.error("Please enter your API Key.")

st.markdown("<hr>", unsafe_allow_html=True)

# --- AI 互動教練對話區 ---
st.subheader("AI Financial Consultation")
st.write("Ask your dedicated coach a question, e.g., 'Do I have enough savings to buy a flat?'")

user_question = st.text_input("Enter your question:")
if user_question and api_key:
    if st.button("Submit Query"):
        with st.spinner("Thinking..."):
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
                st.error(f"Error: {e}")
