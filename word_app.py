import streamlit as st
import pandas as pd
import random
import json
import os
import re

EXCEL_FILE = "处理后的单词表.xlsx"   # 上传到 GitHub 时要放在同一个仓库
PROGRESS_FILE = "progress.json"    # 进度文件（和程序同目录）

# ========== 工具函数 ==========
def load_data():
    df = pd.read_excel(EXCEL_FILE, header=None, names=["word", "definition", "sentence"])
    rows = df.to_dict(orient="records")
    by_word = {}
    for r in rows:
        by_word.setdefault(r['word'], []).append(r)
    return rows, by_word, set(r['word'] for r in rows)

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return set(data.get("learned", [])), set(data.get("mastered", []))
        except Exception:
            return set(), set()
    return set(), set()

def save_progress(learned, mastered):
    data = {
        "learned": list(learned),
        "mastered": list(mastered)
    }
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def pick_random(by_word, all_words, learned_words, mastered_words, from_learned=False):
    if from_learned:
        candidates = list(learned_words - mastered_words)
    else:
        candidates = list(all_words - mastered_words)
    if not candidates:
        return None
    word = random.choice(candidates)
    return random.choice(by_word[word])

# ========== Streamlit 应用 ==========
st.set_page_config(page_title="单词学习工具", layout="centered")

if "rows" not in st.session_state:
    rows, by_word, all_words = load_data()
    learned_words, mastered_words = load_progress()
    st.session_state.rows = rows
    st.session_state.by_word = by_word
    st.session_state.all_words = all_words
    st.session_state.learned_words = learned_words
    st.session_state.mastered_words = mastered_words
    st.session_state.current = None

rows = st.session_state.rows
by_word = st.session_state.by_word
all_words = st.session_state.all_words
learned_words = st.session_state.learned_words
mastered_words = st.session_state.mastered_words

# ========== 顶部进度 ==========
st.markdown(f"### 已学习：{len(learned_words)}/{len(all_words)}　已掌握：{len(mastered_words)}/{len(all_words)}")

# ========== 模式选择 ==========
mode = st.radio("选择模式", ["学习", "选择题", "填空题"], horizontal=True)

# ========== 出题逻辑 ==========
def new_question():
    if mode == "学习":
        q = pick_random(by_word, all_words, learned_words, mastered_words, from_learned=False)
        if q:
            learned_words.add(q['word'])
        return q
    elif mode == "选择题":
        return pick_random(by_word, all_words, learned_words, mastered_words, from_learned=True)
    elif mode == "填空题":
        return pick_random(by_word, all_words, learned_words, mastered_words, from_learned=True)

if st.button("下一题"):
    st.session_state.current = new_question()
    save_progress(learned_words, mastered_words)

current = st.session_state.current

if not current:
    st.info("👉 点击【下一题】开始学习吧！")
else:
    word = current['word']
    definition = str(current['definition'])
    sentence = str(current['sentence']) if pd.notna(current['sentence']) else ""

    if mode == "学习":
        st.subheader(word)
        st.write(f"**释义：** {definition}")
        st.write(f"**例句：** {sentence}")

    elif mode == "选择题":
        st.subheader(word)
        all_defs = [r['definition'] for r in rows if r['word'] != word]
        if len(all_defs) >= 3:
            options = random.sample(all_defs, 3) + [definition]
        else:
            options = all_defs + [definition]
        random.shuffle(options)
        choice = st.radio("请选择正确的释义：", options)
        if st.button("提交答案"):
            if choice == definition:
                st.success("✅ 正确！")
            else:
                st.error(f"❌ 错误，正确答案是：{definition}")

    elif mode == "填空题":
        st.subheader("填空题")
        if not sentence:
            st.warning("(该条目无例句)")
            st.write(f"**释义：** {definition}")
        else:
            pattern = r'\b' + re.escape(word) + r'\b'
            if re.search(pattern, sentence, flags=re.IGNORECASE):
                blanked = re.sub(pattern, '_____ ', sentence, flags=re.IGNORECASE)
            else:
                m = re.search(re.escape(word), sentence, flags=re.IGNORECASE)
                if m:
                    start, end = m.span()
                    blanked = sentence[:start] + '_____ ' + sentence[end:]
                else:
                    blanked = sentence + "\n\n(句子中未找到精确单词匹配，请直接输入目标单词。)"
            st.write(blanked)
            st.write(f"**释义：** {definition}")
            ans = st.text_input("请输入答案：")
            if st.button("提交答案"):
                if ans.strip().lower() == word.lower():
                    st.success("✅ 正确！")
                else:
                    st.error(f"❌ 错误，正确答案是：{word}")

    # 掌握按钮
    if mode in ["选择题", "填空题"]:
        if st.button("掌握"):
            mastered_words.add(word)
            save_progress(learned_words, mastered_words)
            st.success(f"🎉 已掌握：{word}")
