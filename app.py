import streamlit as st
import pandas as pd
import time
from huggingface_hub import InferenceClient

# 網頁基本設定
st.set_page_config(page_title="HK Finance AI Coach", page_icon="", layout="wide")

# 極致清晰 Apple 黑白風 CSS
st.markdown("""
<style>
    .stApp {
        background-color: #FFFFFF !important;
        color: #111111 !important;
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Helvetica Neue", Arial, sans-serif;
    }
    h1, h2, h3, h4, h5, h6, p, label, span, div {
        color: #111111;
    }
    ::selection {
        background-color: #000000 !important;
        color: #FFFFFF !important;
    }
    [data-testid="stSidebar"] {
        background-color: #FBFBFD !important;
        border-right: 1px solid #D2D2D7 !important;
    }
    [data-testid="stSidebar"] * {
        color: #111111 !important;
    }
    [data-testid="stMetricValue"], [data-testid="stMetricLabel"] {
        color: #000000 !important;
    }
    
    /* Apple 框線卡片：強制等高 + 標題強制不換行防 Bug */
    .apple-card {
        border: 1px solid #111111;
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 24px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        height: 100%;
    }
    .apple-card h4 {
        font-size: 1.1rem !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
        margin-bottom: 4px !important;
    }
    .apple-card * {
        color: #111111 !important;
    }
    
    code, pre {
        background-color: #F1F1F3 !important;
        color: #111111 !important;
        border-radius: 6px;
        padding: 2px 6px;
    }
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
    [data-baseweb="tab-list"] {
        gap: 10px;
    }
    [data-baseweb="tab"] {
        background-color: #F5F5F7 !important;
        border-radius: 8px !important;
        padding: 10px 20px !important;
        border: 1px solid #D2D2D7 !important;
    }
    [aria-selected="true"] {
        background-color: #111111 !important;
        color: #FFFFFF !important;
    }
    [aria-selected="true"] * {
        color: #FFFFFF !important;
    }
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
    input[type="number"]::-webkit-inner-spin-button,
    input[type="number"]::-webkit-outer-spin-button {
        -webkit-appearance: none !important;
        margin: 0 !important;
    }
    input[type="number"] {
        -moz-appearance: textfield !important;
    }
    hr {
        border: none;
        height: 1px;
        background-color: #D2D2D7;
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)

st.title("HK Finance AI 理財教練")
st.write("結合精準數學模型、市場環境趨勢與自動化分帳系統的極簡理財平台。")

default_hf_token = "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"

# 極簡側邊欄：只放系統設定與快速核心參數
with st.sidebar:
    st.header("系統設定")
    api_key = st.text_input("Hugging Face Token", value=default_hf_token, type="password")
    
    st.markdown("<hr>", unsafe_allow_html=True)
    st.header("⚡ 快速現金流微調")
    salary_before_mpf = st.number_input("每月薪金（MPF前 HKD）", value=22000, step=1000)
    monthly_expense = st.number_input("每月總開支 (HKD)", value=15000, step=500)
    past_3yr_stock_return = st.slider("過去 3 年投資平均回報 (%)", min_value=-10.0, max_value=25.0, value=8.5, step=0.5)

if api_key:
    client = InferenceClient(api_key=api_key)
else:
    st.warning("請輸入你的 Hugging Face Token。")

# 計算核心財務數據
mpf_deduction = min(salary_before_mpf * 0.05, 1500) if salary_before_mpf >= 7100 else 0
salary_after_mpf = salary_before_mpf - mpf_deduction
monthly_saving = salary_after_mpf - monthly_expense
savings_rate = (monthly_saving / salary_after_mpf) * 100 if salary_after_mpf > 0 else 0

# 使用 Session State 儲存進階資產數據（避免切換 Tab 時重設）
if 'bank_balance' not in st.session_state: st.session_state.bank_balance = 80400
if 'cash' not in st.session_state: st.session_state.cash = 0
if 'stocks' not in st.session_state: st.session_state.stocks = 0
if 'mpf' not in st.session_state: st.session_state.mpf = 0
if 'liabilities' not in st.session_state: st.session_state.liabilities = 0
if 'age' not in st.session_state: st.session_state.age = "28"
if 'occupation' not in st.session_state: st.session_state.occupation = "Professional / Sales"
if 'short_goal' not in st.session_state: st.session_state.short_goal = "存夠 20 萬備用金"
if 'mid_goal' not in st.session_state: st.session_state.mid_goal = "儲首期買樓／結婚"

total_liquid_assets = st.session_state.bank_balance + st.session_state.cash + st.session_state.stocks
net_worth = total_liquid_assets + st.session_state.mpf - st.session_state.liabilities

# --- 主畫面分頁導航 (Tabs) 徹底解決 Sidebar 疲勞 ---
tab1, tab2, tab3 = st.tabs(["📊 財富儀表板與自動分帳", "⚙️️ 進階資產與目標設定", "🤖 AI 宏觀分析與 3 年預測"])

with tab1:
    st.subheader("📌 核心財務指標")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("每月儲蓄率", f"{savings_rate:.1f}%", f"實收糧 ${salary_after_mpf:,.0f}")
    c2.metric("總流動資產", f"${total_liquid_assets:,.0f}")
    c3.metric("淨資產總值", f"${net_worth:,.0f}")
    c4.metric("過去3年回報參考", f"{past_3yr_stock_return:.1f}% p.a.")

    st.markdown("<hr>", unsafe_allow_html=True)

    st.subheader("💳 自動化多戶口分帳儀表板（動態比例模型）")
    st.write(f"基於你目前實收糧 **${salary_after_mpf:,.0f}** 同開支結構，最佳分配方案如下：")

    recommended_cc = min(monthly_expense * 0.65, monthly_expense)
    weekly_transfer = recommended_cc / 4
    recommended_saving_ac = monthly_saving * 0.75
    recommended_invest_ac = monthly_saving * 0.25

    col_a, col_b, col_c, col_d = st.columns(4)

    with col_a:
        st.markdown("""
        <div class="apple-card">
            <div>
                <h4>銀行 A</h4>
                <p style="font-size: 13px; color: #555;">出糧戶口 ＋ 每日開支</p>
                <hr style="margin: 10px 0;">
                <p style="font-size: 18px; font-weight: bold;">維持水位 $5,000</p>
            </div>
            <p style="font-size: 12px; margin-top: 15px; color: #333;">(月尾多出餘額手動轉走)</p>
        </div>
        """, unsafe_allow_html=True)

    with col_b:
        st.markdown(f"""
        <div class="apple-card">
            <div>
                <h4>銀行 B</h4>
                <p style="font-size: 13px; color: #555;">信用卡自動找數專用</p>
                <hr style="margin: 10px 0;">
                <p style="font-size: 18px; font-weight: bold;">約 ${recommended_cc:,.0f} /月</p>
            </div>
            <p style="font-size: 12px; margin-top: 15px; color: #333;">每週自動: ${weekly_transfer:,.0f} × 4</p>
        </div>
        """, unsafe_allow_html=True)

    with col_c:
        st.markdown(f"""
        <div class="apple-card">
            <div>
                <h4>銀行 C</h4>
                <p style="font-size: 13px; color: #555;">高息儲蓄／備用金</p>
                <hr style="margin: 10px 0;">
                <p style="font-size: 18px; font-weight: bold;">每月轉 ${recommended_saving_ac:,.0f}</p>
            </div>
            <p style="font-size: 12px; margin-top: 15px; color: #333;">(強制鎖定現金資產)</p>
        </div>
        """, unsafe_allow_html=True)

    with col_d:
        st.markdown(f"""
        <div class="apple-card">
            <div>
                <h4>證券 / 銀行 D</h4>
                <p style="font-size: 13px; color: #555;">投資戶口 (VOO月供)</p>
                <hr style="margin: 10px 0;">
                <p style="font-size: 18px; font-weight: bold;">每月轉 ${recommended_invest_ac:,.0f}</p>
            </div>
            <p style="font-size: 12px; margin-top: 15px; color: #333;">(長期資產增長引擎)</p>
        </div>
        """, unsafe_allow_html=True)

with tab2:
    st.subheader("⚙️ 進階資產與個人目標設定")
    st.write("喺呢度輕鬆管理你嘅身家帳目同埋理財里程碑，系統會即時同步到 AI 分析引擎：")

    col_t2_1, col_t2_2 = st.columns(2)
    
    with col_t2_1:
        st.markdown("#### 💰 資產與負債明細")
        st.session_state.bank_balance = st.number_input("銀行戶口及餘額 (HKD)", value=st.session_state.bank_balance, step=1000)
        st.session_state.cash = st.number_input("現金 (HKD)", value=st.session_state.cash, step=500)
        st.session_state.stocks = st.number_input("股票／ETF (HKD)", value=st.session_state.stocks, step=1000)
        st.session_state.mpf = st.number_input("現有強積金總額 (HKD)", value=st.session_state.mpf, step=1000)
        st.session_state.liabilities = st.number_input("負債（卡數／貸款 HKD）", value=st.session_state.liabilities, step=500)

    with col_t2_2:
        st.markdown("#### 🎯 個人檔案與目標")
        st.session_state.age = st.text_input("年齡", value=st.session_state.age)
        st.session_state.occupation = st.text_input("職業", value=st.session_state.occupation)
        st.session_state.short_goal = st.text_input("短期目標（1年內）", value=st.session_state.short_goal)
        st.session_state.mid_goal = st.text_input("中期目標（2-5年）", value=st.session_state.mid_goal)
        risk_tolerance = st.selectbox("風險承受能力", ["保守", "中等", "進取"], index=1)

with tab3:
    st.subheader("🤖 AI 宏觀市況與 36 個月複利預測引擎")
    st.write("結合你過去 3 年投資回報基準、當前 2026 年市況，以及實時現金流，一鍵解鎖深度理財架構：")

    if st.button("執行 AI 理財架構分析與雙線預測", type="primary"):
        if api_key:
            progress_bar = st.progress(0, text="正在初始化理財引擎...")
            time.sleep(0.2)
            progress_bar.progress(30, text="正在擷取過去 3 年回報與現金流數據...")
            time.sleep(0.2)
            progress_bar.progress(60, text="正在結合 2026 最新市況進行宏觀校準...")
            
            try:
                system_persona = f"""
                You are a professional, precise Hong Kong financial coach in year 2026. 
                You must respond in natural, professional Hong Kong Traditional Chinese, using bullet points exclusively for analysis.

                [User Financial Data & Performance]
                - Net Salary (after MPF): ${salary_after_mpf:,.0f}
                - Monthly Expense: ${monthly_expense:,.0f}
                - Monthly Savings: ${monthly_saving:,.0f} (Savings Rate: {savings_rate:.1f}%)
                - Total Liquid Assets: ${total_liquid_assets:,.0f}
                - Past 3-Year Stock Portfolio Return: {past_3yr_stock_return:.1f}% p.a.
                - Net Worth: ${net_worth:,.0f}

                [Rules]
                1. Output concise, meaningful financial analysis structured purely in bullet points (- or *).
                2. Analyze the coming 3-year growth trend by referencing the user's past 3-year performance ({past_3yr_stock_return:.1f}%) and current 2026 macroeconomic market conditions.
                3. Keep it punchy, professional, and entirely free of hallucinated calculations.
                """

                task_prompt = f"""
                請根據用戶的財務數據、過去 3 年投資回報（{past_3yr_stock_return:.1f}%）以及 2026 年當前宏觀市場狀況，以精簡的 Bullet Points 提供商業級分析：
                - 現金流與儲蓄率的強勢點評
                - 綜合過去 3 年表現與 2026 年最新市況對未來 3 年 VOO / 投資增長的趨勢預測
                - 多戶口自動化分帳與長期財富累積的實戰建議
                """
                
                messages = [
                    {"role": "system", "content": system_persona},
                    {"role": "user", "content": task_prompt}
                ]
                
                response = client.chat.completions.create(
                    model="meta-llama/Llama-3.1-8B-Instruct",
                    messages=messages,
                    max_tokens=600,
                    temperature=0.3,
                    extra_body={"repetition_penalty": 1.25}
                )
                
                progress_bar.progress(100, text="完成！")
                time.sleep(0.2)
                progress_bar.empty()
                
                st.success("AI 市況分析與雙線複利預測已完成")
                
                # 顯示 AI 分析報告
                st.markdown(f'<div class="apple-card"><h4>🤖 AI 宏觀市況與 3 年增長分析報告</h4>{response.choices[0].message.content}</div>', unsafe_allow_html=True)
                
                # --- 📈 雙線對比圖表 (Comparison Chart) ---
                st.subheader("📈 36 個月資產累積：AI 複利增長 vs 純現金死儲對比")
                st.write(f"對比展示：一條係結合你過去回報（{past_3yr_stock_return:.1f}%）嘅 **AI 複利增長軌跡**，另一條係完全唔投資嘅 **純現金儲蓄軌跡**：")

                months = list(range(37))
                adjusted_annual_rate = max(min(past_3yr_stock_return / 100.0, 0.20), -0.05)
                monthly_return_rate = (1 + adjusted_annual_rate) ** (1/12) - 1

                projected_assets = []
                pure_cash_assets = []
                current_val = total_liquid_assets
                current_cash = total_liquid_assets

                for m in months:
                    if m == 0:
                        projected_assets.append(current_val)
                        pure_cash_assets.append(current_cash)
                    else:
                        current_val = current_val * (1 + monthly_return_rate) + monthly_saving
                        projected_assets.append(current_val)
                        current_cash = current_cash + monthly_saving
                        pure_cash_assets.append(current_cash)

                df_chart = pd.DataFrame({
                    "月份": months, 
                    "AI 複利投資總資產 (HKD)": projected_assets,
                    "純現金儲蓄軌跡 (HKD)": pure_cash_assets
                })
                df_chart.set_index("月份", inplace=True)

                st.line_chart(df_chart)

                pure_linear_1yr = total_liquid_assets + (monthly_saving * 12)
                pure_linear_3yr = total_liquid_assets + (monthly_saving * 36)
                alpha_1yr = projected_assets[12] - pure_linear_1yr
                alpha_3yr = projected_assets[36] - pure_linear_3yr

                col_p1, col_p2 = st.columns(2)
                with col_p1:
                    st.metric("1 年後預測總資產 (複利 vs 純儲蓄)", f"${projected_assets[12]:,.0f}", f"複利超額收益 (Alpha) +${alpha_1yr:,.0f}")
                with col_p2:
                    st.metric("3 年後預測總資產 (複利 vs 純儲蓄)", f"${projected_assets[36]:,.0f}", f"複利超額收益 (Alpha) +${alpha_3yr:,.0f}")

            except Exception as e:
                progress_bar.empty()
                st.error(f"發生錯誤：{e}")
        else:
            st.error("請先在側邊欄輸入 API Key。")
    else:
        st.info("💡 準備好後請點擊上方按鈕，即時產生 2026 最新市況報告與雙線資產對比圖！")
