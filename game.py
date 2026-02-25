import scipy.io as sio
import numpy as np
import streamlit as st

# 預先載入 .mat 檔案（只載入一次）
if 'ref_table' not in st.session_state:
    mat_data = sio.loadmat('Ref_Table.mat')
    st.session_state.ref_table = mat_data['Ref_Table']  # 確認這是正確的 key 名稱
    st.session_state.num_cols = st.session_state.ref_table.shape[1]
    st.session_state.seed_list = np.random.choice(
        st.session_state.num_cols, 
        st.session_state.num_cols, 
        replace=True
    )

# 初始化遊戲狀態
if 's' not in st.session_state:
    st.session_state.s = -1  # -1 表示還沒開始

if 'current_hint' not in st.session_state:
    st.session_state.current_hint = None

if 'current_ans' not in st.session_state:
    st.session_state.current_ans = None

if 'guess_submitted' not in st.session_state:
    st.session_state.guess_submitted = False

# 標題
st.title("猜字遊戲")

# 按鈕：開始新的一輪 / 下一題
if st.button("開始新的一輪 / 下一題"):
    st.session_state.s += 1
    s = st.session_state.s
    item_idx = st.session_state.seed_list[s % len(st.session_state.seed_list)]  # 避免 index out of range

    # 取出這一組的 Phrase 和 Word（根據你的 .mat 結構調整）
    current_item = st.session_state.ref_table[0][item_idx]
    phrase = current_item['Phrase'][0]           # 假設是 1D cell array 或 string array
    ans   = current_item['Word'][0][0]           # 假設是單一字串

    # 隨機選 4 個不重複的位置
    phrase_size = len(phrase)
    idx = np.random.choice(phrase_size, 4, replace=False)

    # 產生 Hint（list of strings）
    hint_list = [str(phrase[i]) for i in idx]

    # 存到 session_state
    st.session_state.current_hint = hint_list
    st.session_state.current_ans   = ans
    st.session_state.guess_submitted = False   # 重置檢查狀態
    st.rerun()  # 可選：立即刷新畫面，讓輸入框清空

# 顯示 Hint（只要有題目就一直顯示）
if st.session_state.current_hint is not None:
    st.markdown("**Hint：** " + "　".join(st.session_state.current_hint))

    # 輸入框（用 key 避免重跑時值被清掉）
    user_guess = st.text_input(
        "猜猜上面要接什麼字？",
        key="current_guess",
        value="" if not st.session_state.guess_submitted else st.session_state.get("current_guess", "")
    )

    # 檢查答案按鈕
    if st.button("檢查答案"):
        st.session_state.guess_submitted = True
        st.rerun()  # 強制重跑以顯示結果

    # 只在提交後顯示判斷結果
    if st.session_state.guess_submitted:
        correct_ans = st.session_state.current_ans
        if user_guess.strip() == correct_ans:
            st.success(f"正確！答案就是：{correct_ans}")
        else:
            st.error(f"錯了～ 正解是：{correct_ans}")

        # 可選：看完後直接給下一題的按鈕
        if st.button("下一題"):
            st.session_state.s += 1
            st.session_state.guess_submitted = False
            st.rerun()

else:
    st.info("請按「開始新的一輪 / 下一題」開始遊戲～")
