import scipy.io as sio
import numpy as np
import streamlit as st

# 預先載入.mat檔案（假設檔案在同目錄）
ref_table = sio.loadmat('Ref_Table.mat')['Ref_Table']

# 初始化（類似MATLAB的預先執行）
num_cols = ref_table.shape[1]  # Ref_Table的列數
seed_list = np.random.choice(num_cols, num_cols, replace=True)  # 隨機樣本

# Streamlit網頁介面
st.title("猜字遊戲")

# 使用session state來追蹤遊戲狀態（類似你的s）
if 's' not in st.session_state:
    st.session_state.s = 0

if st.button("開始新的一輪"):
    st.session_state.s += 1
    s = st.session_state.s
    phrase_size = ref_table[0][seed_list[s-1]]['Phrase'].shape[1]  # 調整存取方式
    idx = np.random.choice(phrase_size, 4, replace=False)  # 隨機選4個不重複
    
    # 取出Hint和Ans（需根據結構調整）
    hint = ref_table[0][seed_list[s-1]]['Phrase'][0][idx]  # 假設是cell array
    ans = ref_table[0][seed_list[s-1]]['Word'][0][0]  # 假設是單一字串

    st.write("Hint:", hint)
    user_guess = st.text_input("猜猜上面要接什麼字？")
    
    if st.button("檢查答案"):
        if user_guess == ans:
            st.success("正確！")
        else:
            st.error("錯了，正解是: " + ans)
