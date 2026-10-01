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
st.write("結合合規模型資產配置、現金流自動分帳與宏觀複利預測的極簡理財平台。")

default_hf_token = "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"

# 極簡側邊欄
with st.sidebar:
    st.header("系統設定")
    api_key = st.text_input("Hugging Face Token", value=default_hf_token, type="password")
    
    st.markdown("<hr>", unsafe_allow_html=True)
    st.header("⚡ 快速現金流微調")
    salary_before_mpf = st.number_input("每月薪金（MPF前 HKD）", value=22000, step=1000)
    monthly_expense = st.number_input("每月總開支 (HKD)", value=15000, step=500)

if api_key:
    client = InferenceClient(api_key=api_key)
else:
    st.warning("請輸入你的 Hugging Face Token。")

# 計算核心財務數據
mpf_deduction = min(salary_before_mpf * 0.05, 1500) if salary_before_mpf >= 7100 else 0
salary_after_mpf = salary_before_mpf - mpf_deduction
monthly_saving = salary_after_mpf - monthly_expense
savings_rate = (monthly_saving / salary_after_mpf) * 100 if salary_after_mpf > 0 else 0

# Session State
if 'bank_balance' not in st.session_state: st.session_state.bank_balance = 80400
if 'cash' not in st.session_state: st.session_state.cash = 0
if 'stocks' not in st.session_state: st.session_state.stocks = 0
if 'mpf' not in st.session_state: st.session_state.mpf = 0
if 'liabilities' not in st.session_state: st.session_state.liabilities = 0
if 'risk_tolerance' not in st.session_state: st.session_state.risk_tolerance = "中等 (Moderate)"

total_liquid_assets = st.session_state.bank_balance + st.session_state.cash + st.session_state.stocks
net_worth = total_liquid_assets + st.session_state.mpf - st.session_state.liabilities

# --- 主畫面分頁導航 ---
tab1, tab2, tab3 = st.tabs(["📊 財富儀表板與自動分帳", "⚙ 模型資產配置與設定", "🤖 AI 宏觀分析與 3 年預測"])

with tab1:
    st.subheader("📌 核心財務指標")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("每月儲蓄率", f"{savings_rate:.1f}%", f"實收糧 ${salary_after_mpf:,.0f}")
    c2.metric("總流動資產", f"${total_liquid_assets:,.0f}")
    c3.metric("淨資產總值", f"${net_worth:,.0f}")
    c4.metric("當前投資策略", st.session_state.risk_tolerance)

    st.markdown("<hr>", unsafe_allow_html=True)

    st.subheader("💳 自動化多戶口分帳儀表板")
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
                <p style="font-size: 13px; color: #555;">模型資產月供戶口</p>
                <hr style="margin: 10px 0;">
                <p style="font-size: 18px; font-weight: bold;">每月轉 ${recommended_invest_ac:,.0f}</p>
            </div>
            <p style="font-size: 12px; margin-top: 15px; color: #333;">(對應下方風險配置)</p>
        </div>
        """, unsafe_allow_html=True)

with tab2:
    st.subheader("⚙️ 資產設定與模型投資組合選擇")
    st.write("為避免直接推介單一股票嘅法律合規風險，系統採用**「機構級資產配置模型（Model Portfolios）」**。選擇你嘅風險承受能力，系統會自動對應相應嘅 ETF 組合與歷史增長率：")

    col_t2_1, col_t2_2 = st.columns(2)
    
    with col_t2_1:
        st.markdown("#### 💰 現有資產與負債")
        st.session_state.bank_balance = st.number_input("銀行戶口及餘額 (HKD)", value=st.session_state.bank_balance, step=1000)
        st.session_state.cash = st.number_input("現金 (HKD)", value=st.session_state.cash, step=500)
        st.session_state.stocks = st.number_input("現有股票／ETF (HKD)", value=st.session_state.stocks, step=1000)
        st.session_state.mpf = st.number_input("現有強積金總額 (HKD)", value=st.session_state.mpf, step=1000)
        st.session_state.liabilities = st.number_input("負債（卡數／貸款 HKD）", value=st.session_state.liabilities, step=500)

    with col_t2_2:
        st.markdown("#### ⚖️ 風險承受能力與模型配置")
        st.session_state.risk_tolerance = st.selectbox(
            "選擇風險偏好（決定模型資產與增長率）", 
            ["保守 (Conservative)", "中等 (Moderate)", "進取 (Aggressive)"],
            index=1
        )
        
        # 根據選擇顯示對應嘅模型組合細節（話畀用戶知組合買緊乜）
        if "保守" in st.session_state.risk_tolerance:
            st.info("**組合成分**：80% 短期國債 ETF / 定存現金 ＋ 20% 高息盈富基金 (2800.HK)\n\n**預期年化回報**：約 4.5%")
            model_return = 0.045
        elif "中等" in st.session_state.risk_tolerance:
            st.info("**組合成分**：70% VOO (標普 500 ETF) / 2800.HK 盈富基金 ＋ 30% 環球債券 ETF\n\n**預期年化回報**：約 8.5%")
            model_return = 0.085
        else:
            st.info("**組合成分**：85% QQQ (納指 100 ETF) / 環球科技增長股 ＋ 15% 核心防守資產\n\n**預期年化回報**：約 12.0%")
            model_return = 0.12

with tab3:
    st.subheader("🤖 AI 宏觀市況與 36 個月模型複利預測")
    
    # 根據用戶選嘅風險偏好取得預期回報
    if "保守" in st.session_state.risk_tolerance:
        active_return = 4.5
    elif "中等" in st.session_state.risk_tolerance:
        active_return = 8.5
    else:
        active_return = 12.0

    st.write(f"當前選擇模型：**{st.session_state.risk_tolerance}**（模擬年化回報基準：**{active_return}%**）。系統將以呢個資產組合軌跡為核心進行 36 個月推演：")

    if st.button("執行 AI 模型複利與宏觀分析", type="primary"):
        if api_key:
            progress_bar = st.progress(0, text="正在載入合規模型配置...")
            time.sleep(0.2)
            progress_bar.progress(40, text="正在計算模型資產複利軌跡...")
            time.sleep(0.2)
            progress_bar.progress(70, text="正在結合 2026 最新宏觀市況生成評語...")
            
            try:
                system_persona = f"""
                You are a professional, precise Hong Kong financial coach in year 2026. 
                You must respond in natural, professional Hong Kong Traditional Chinese, using bullet points exclusively for analysis.

                [User Financial & Portfolio Data]
                - Net Salary (after MPF): ${salary_after_mpf:,.0f}
                - Monthly Expense: ${monthly_expense:,.0f}
                - Monthly Savings: ${monthly_saving:,.0f} (Savings Rate: {savings_rate:.1f}%)
                - Total Liquid Assets: ${total_liquid_assets:,.0f}
                - Selected Risk Profile: {st.session_state.risk_tolerance} (Model Return: {active_return}%)
                - Net Worth: ${net_worth:,.0f}

                [Rules]
                1. Output concise financial analysis structured purely in bullet points (- or *).
                2. Evaluate the chosen model portfolio's suitability against the user's cash flow and 2026 macroeconomic conditions.
                3. Keep it professional, objective, and include a polite educational disclaimer that this is a model simulation, not direct financial advice.
                """

                task_prompt = f"""
                請根據用戶的現金流狀況與選定的資產配置模型（{st.session_state.risk_tolerance}，基準回報 {active_return}%），結合 2026 年最新宏觀市況，以精簡的 Bullet Points 提供分析：
                - 現金流與儲蓄率評估
                - 該模型資產配置（如 VOO / 盈富 / 債券等組合）在當前市況下的表現潛力
                - 長期紀律執行的實戰建議與合規提示
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
                
                st.success("AI 模型分析與複利預測已完成")
                
                # 顯示 AI 分析報告
                st.markdown(f'<div class="apple-card"><h4>🤖 AI 模型資產與市況分析報告</h4>{response.choices[0].message.content}</div>', unsafe_allow_html=True)
                
                # --- 📈 雙線對比圖表 (Comparison Chart) ---
                st.subheader("📈 36 個月資產累積：模型資產複利增長 vs 純現金儲蓄")
                st.write(f"對比展示：基於 **{st.session_state.risk_tolerance}** 模型軌跡（年化 {active_return}%）與 **純現金死儲** 嘅 36 個月對比：")

                months = list(range(37))
                monthly_return_rate = (1 + (active_return / 100.0)) ** (1/12) - 1

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
                    "模型資產複利總值 (HKD)": projected_assets,
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
                    st.metric("1 年後預測總資產 (模型 vs 純儲蓄)", f"${projected_assets[12]:,.0f}", f"複利超額收益 +${alpha_1yr:,.0f}")
                with col_p2:
                    st.metric("3 年後預測總資產 (模型 vs 純儲蓄)", f"${projected_assets[36]:,.0f}", f"複利超額收益 +${alpha_3yr:,.0f}")

                st.caption("⚠️ **免責聲明**：以上數據與資產組合模型僅作教育、模擬與財務規劃參考，不構成任何具體證券買賣建議或金融服務邀約。")

            except Exception as e:
                progress_bar.empty()
                st.error(f"發生錯誤：{e}")
        else:
            st.error("請先在側邊欄輸入 API Key。")
    else:
        st.info("💡 準備好後請點擊上方按鈕，即時產生模型複利模擬與宏觀市況報告！")
