import tkinter as tk
from tkinter import messagebox, scrolledtext
import pandas as pd
import random
import re
import os

EXCEL_PATH = r"C:\Users\admin\Desktop\处理后的单词表.xlsx"

class WordApp:
    def __init__(self, master):
        self.master = master
        master.title("单词背诵小程序")
        master.geometry("800x520")

        # 数据加载
        try:
            df = pd.read_excel(EXCEL_PATH, header=None, engine="openpyxl")
        except Exception as e:
            messagebox.showerror("读取错误", f"无法读取 Excel 文件：{EXCEL_PATH}\n\n错误信息：{e}")
            raise SystemExit

        # 期望每行: word, definition, sentence
        df = df.fillna('')  # 避免空值
        self.rows = []
        for _, row in df.iterrows():
            word = str(row[0]).strip()
            definition = str(row[1]).strip()
            sentence = str(row[2]).strip()
            if word == '' and definition == '' and sentence == '':
                continue
            self.rows.append({'word': word, 'definition': definition, 'sentence': sentence})

        if not self.rows:
            messagebox.showerror("数据错误", "数据文件没有有效行，请检查文件内容。")
            raise SystemExit

        # 根据单词分组：用于选择题时排除同单词释义
        self.by_word = {}
        for r in self.rows:
            self.by_word.setdefault(r['word'], []).append(r)

        # 建立释义池（所有释义）
        self.all_definitions = [r['definition'] for r in self.rows if r['definition']]

        # 程序状态
        self.mode = 'recite'  # recite / choice / fill
        self.current = None  # 当前条目 dict

        # 顶部按钮区
        top_frame = tk.Frame(master)
        top_frame.pack(fill=tk.X, padx=8, pady=6)

        self.recite_btn = tk.Button(top_frame, text="背诵", command=self.set_recite_mode)
        self.recite_btn.pack(side=tk.LEFT, padx=4)
        self.choice_btn = tk.Button(top_frame, text="选择题", command=self.set_choice_mode)
        self.choice_btn.pack(side=tk.LEFT, padx=4)
        self.fill_btn = tk.Button(top_frame, text="填空题", command=self.set_fill_mode)
        self.fill_btn.pack(side=tk.LEFT, padx=4)
        self.next_btn = tk.Button(top_frame, text="下一题", command=self.next_question)
        self.next_btn.pack(side=tk.RIGHT, padx=4)

        # 中间显示区
        self.display_frame = tk.Frame(master)
        self.display_frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=6)

        # 单词显示（大）
        self.word_label = tk.Label(self.display_frame, text="", font=("Arial", 28))
        self.word_label.pack(pady=8)

        # 释义 / 选项 / 句子显示区
        self.text_area = scrolledtext.ScrolledText(self.display_frame, height=8, wrap=tk.WORD, font=("Arial", 12))
        self.text_area.pack(fill=tk.BOTH, expand=False, padx=6, pady=6)
        self.text_area.configure(state='disabled')

        # 选择题的4个按钮
        self.options_frame = tk.Frame(self.display_frame)
        self.options = []
        for i in range(4):
            b = tk.Button(self.options_frame, text=f"选项 {i+1}", wraplength=350, justify=tk.LEFT, command=lambda idx=i: self.check_choice(idx))
            b.grid(row=i//2, column=i%2, sticky="we", padx=6, pady=6)
            self.options.append(b)
        # 让选项区域水平拉伸
        for i in range(2):
            self.options_frame.grid_columnconfigure(i, weight=1)

        # 填空题输入区
        self.fill_frame = tk.Frame(self.display_frame)
        self.answer_entry = tk.Entry(self.fill_frame, font=("Arial", 14))
        self.answer_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=6)
        self.submit_btn = tk.Button(self.fill_frame, text="提交", command=self.check_fill)
        self.submit_btn.pack(side=tk.LEFT, padx=6)

        # 反馈区
        self.feedback_label = tk.Label(master, text="", font=("Arial", 12))
        self.feedback_label.pack(pady=4)

        # 初始显示
        self.set_recite_mode()
        self.next_question()

    def clear_display(self):
        self.word_label.config(text="")
        self.text_area.configure(state='normal')
        self.text_area.delete('1.0', tk.END)
        self.text_area.configure(state='disabled')
        self.feedback_label.config(text="", fg="black")
        # hide optional frames
        self.options_frame.pack_forget()
        self.fill_frame.pack_forget()

    def set_recite_mode(self):
        self.mode = 'recite'
        self.recite_btn.config(relief=tk.SUNKEN)
        self.choice_btn.config(relief=tk.RAISED)
        self.fill_btn.config(relief=tk.RAISED)
        self.next_question()

    def set_choice_mode(self):
        self.mode = 'choice'
        self.recite_btn.config(relief=tk.RAISED)
        self.choice_btn.config(relief=tk.SUNKEN)
        self.fill_btn.config(relief=tk.RAISED)
        self.next_question()

    def set_fill_mode(self):
        self.mode = 'fill'
        self.recite_btn.config(relief=tk.RAISED)
        self.choice_btn.config(relief=tk.RAISED)
        self.fill_btn.config(relief=tk.SUNKEN)
        self.next_question()

    def pick_random(self):
        return random.choice(self.rows)

    def next_question(self):
        self.clear_display()
        self.current = self.pick_random()

        if self.mode == 'recite':
            self.show_recite()
        elif self.mode == 'choice':
            self.show_choice()
        elif self.mode == 'fill':
            self.show_fill()

    # ============ 背诵模式 ============
    def show_recite(self):
        word = self.current['word']
        definition = self.current['definition']
        sentence = self.current['sentence']
        self.word_label.config(text=word)
        content = f"释义：\n{definition}\n\n例句：\n{sentence}"
        self.text_area.configure(state='normal')
        self.text_area.insert(tk.END, content)
        self.text_area.configure(state='disabled')

    # ============ 选择题模式 ============
    def show_choice(self):
        word = self.current['word']
        correct_def = self.current['definition']
        # 构建干扰释义：从所有释义中抽样，但排除与当前词相同单词的释义
        pool = [d for d in self.all_definitions if d and d != correct_def]
        # 还应排除当前单词其它释义（即使不是完全相等，也尝试基于 by_word）
        same_word_defs = {r['definition'] for r in self.by_word.get(word, [])}
        pool = [d for d in pool if d not in same_word_defs]

        num_needed = 3
        if len(pool) >= num_needed:
            distractors = random.sample(pool, num_needed)
        else:
            # 如果不足，从所有释义（可包含同词释义）中抽取补足
            pool2 = [d for d in self.all_definitions if d and d != correct_def]
            # 允许重复取样以补足
            distractors = []
            while len(distractors) < num_needed:
                if pool2:
                    distractors.append(random.choice(pool2))
                else:
                    distractors.append("（无足够干扰项）")
        options = distractors + [correct_def]
        random.shuffle(options)
        self.correct_index = options.index(correct_def)

        # 显示词与选项
        self.word_label.config(text=word)
        self.text_area.configure(state='normal')
        self.text_area.insert(tk.END, "请选择正确的释义：\n")
        self.text_area.configure(state='disabled')

        # pack options
        self.options_frame.pack(fill=tk.BOTH, padx=6, pady=6)
        for i, b in enumerate(self.options):
            if i < len(options):
                b.config(text=options[i], state=tk.NORMAL)
                b.show_text = options[i]
            else:
                b.config(text="", state=tk.DISABLED)
                b.show_text = ""
        # reset feedback
        self.feedback_label.config(text="", fg="black")

    def check_choice(self, idx):
        # idx 是按钮索引
        # 点击后禁用选项，显示反馈
        for b in self.options:
            b.config(state=tk.DISABLED)
        try:
            chosen_text = self.options[idx].show_text
        except Exception:
            chosen_text = None
        if chosen_text is None:
            return
        if idx == self.correct_index:
            self.feedback_label.config(text="回答正确 ✅", fg="green")
        else:
            correct_text = self.options[self.correct_index].show_text
            self.feedback_label.config(text=f"回答错误 ❌ 正确答案：{correct_text}", fg="red")

    # ============ 填空题模式 ============
    def show_fill(self):
        word = self.current['word']
        sentence = self.current['sentence']
        definition = self.current['definition']   # 加这一行
        self.word_label.config(text="填空题")
        if not sentence:
            display = "(该条目无例句)\n\n释义：\n" + definition
            self.text_area.configure(state='normal')
            self.text_area.insert(tk.END, display)
            self.text_area.configure(state='disabled')
            self.fill_frame.pack_forget()
            return

        # 替换例句中的目标单词
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

        # 显示例句 + 释义
        self.text_area.configure(state='normal')
        self.text_area.insert(tk.END, blanked + "\n\n释义：\n" + definition)  # 这里加释义
        self.text_area.configure(state='disabled')

        self.answer_entry.delete(0, tk.END)
        self.fill_frame.pack(fill=tk.X, padx=6, pady=6)
        self.feedback_label.config(text="", fg="black")


    def check_fill(self):
        user = self.answer_entry.get().strip()
        if not user:
            self.feedback_label.config(text="请输入答案后提交。", fg="orange")
            return
        target = self.current['word'].strip()
        # 比较时忽略大小写，但也允许简单的变形（例如去掉标点）
        def norm(s):
            return re.sub(r'[^A-Za-z]', '', s).lower()
        if norm(user) == norm(target):
            self.feedback_label.config(text="回答正确 ✅", fg="green")
        else:
            self.feedback_label.config(text=f"回答错误 ❌ 正确答案：{target}", fg="red")

if __name__ == "__main__":
    # 检查 pandas 是否可用（提前友好提示）
    try:
        import pandas  # noqa
    except Exception as e:
        messagebox.showerror("依赖缺失", "运行此程序需要安装 pandas 和 openpyxl。\n\n在命令行运行：\n    pip install pandas openpyxl\n\n然后重新运行程序。")
        raise SystemExit

    root = tk.Tk()
    app = WordApp(root)
    root.mainloop()
