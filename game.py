import streamlit as st
import numpy as np
import scipy.io as sio

# 載入資料（只執行一次）
if 'ref_table' not in st.session_state:
    mat_data = sio.loadmat('Ref_Table.mat')
    st.session_state.ref_table = mat_data['Ref_Table']  # 依你的實際變數名調整
    st.session_state.num_items = st.session_state.ref_table.shape[1]
    st.session_state.seed_list = np.random.choice(
        st.session_state.num_items, 
        st.session_state.num_items, 
        replace=True
    )

# 初始化遊戲狀態
if 's' not in st.session_state:
    st.session_state.s = -1          # -1 表示還沒開始
if 'current_hint' not in st.session_state:
    st.session_state.current_hint = None
if 'current_ans' not in st.session_state:
    st.session_state.current_ans = None
if 'guess_submitted' not in st.session_state:
    st.session_state.guess_submitted = False

st.title("猜字遊戲")

# 按鈕：開始新的一輪 / 下一題
if st.button("開始新的一輪 / 下一題"):
    st.session_state.s += 1
    idx = st.session_state.s % len(st.session_state.seed_list)  # 循環使用
    item_idx = st.session_state.seed_list[idx]
    
    # 假設你的結構是 ref_table[0, item_idx] 是 struct
    phrase = st.session_state.ref_table[0, item_idx]['Phrase'][0]
    word   = st.session_state.ref_table[0, item_idx]['Word'][0]
    
    # 隨機選 4 個位置
    pos = np.random.choice(len(phrase), 4, replace=False)
    hint_list = [phrase[i] for i in pos]
    
    st.session_state.current_hint = hint_list
    st.session_state.current_ans   = word
    st.session_state.guess_submitted = False   # 重置提交狀態
    st.rerun()   # 立即刷新畫面（可選，但可讓介面更乾淨）

# 顯示目前的 Hint
if st.session_state.current_hint is not None:
    st.write("**Hint：**", "　".join(st.session_state.current_hint))
    
    user_guess = st.text_input("請輸入你要接的字：", key="guess_input")
    
    if st.button("檢查答案"):
        st.session_state.guess_submitted = True
        st.rerun()   # 強制重新執行以顯示結果

    # 只在提交後顯示結果（避免按檢查時又產生新題）
    if st.session_state.guess_submitted:
        if user_guess.strip() == st.session_state.current_ans:
            st.success(f"正確！答案就是：{st.session_state.current_ans}")
        else:
            st.error(f"錯了～ 正解是：{st.session_state.current_ans}")
        
        # 可選：顯示正確答案後自動準備下一題的提示
        if st.button("看完答案 → 下一題"):
            st.session_state.s += 1
            # ... 同上面的出題邏輯 ...
            st.rerun()

else:
    st.info("請先按「開始新的一輪 / 下一題」開始遊戲～")