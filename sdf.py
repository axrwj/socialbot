import tkinter as tk
from tkinter import scrolledtext, messagebox
import re
import webbrowser
from datetime import datetime


class SupportChatBot:
    def __init__(self, root):
        self.root = root
        self.root.title("Добро поговорить 💬")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f2f5")

        # Кризисные триггеры (самоповреждение, суицид)
        self.crisis_keywords = [
            r'\b(конец|повеситься|вскрыться|бросили|все надоело|убить себя|суицид|повешусь|отравлюсь|смерть|не хочу жить|конец всему)\b',
            r'\b(ненавижу себя|бесполезный|никому не нужен)\b'
        ]

        # Эмпатичные шаблоны ответов
        self.response_patterns = [
            (r'.*(грустно|печально|одиноко).*',
             "Мне жаль, что вам сейчас грустно. Важно позволить себе чувствовать эти эмоции. Вы не одни — я здесь, чтобы выслушать."),

            (r'.*(тревожно|боюсь|страшно).*',
             "Тревога — тяжёлое чувство. Попробуйте глубоко вдохнуть и выдохнуть несколько раз. Я рядом, давайте поговорим об этом."),

            (r'.*(устал|выгорание|сил нет).*',
             "Выгорание изматывает. Пожалуйста, дайте себе разрешение отдохнуть — даже 10 минут тишины могут помочь. Что именно вас выматывает?"),

            (r'.*(спасибо|благодарю).*',
             "Рад был поддержать вас. Помните: обращаться за помощью — это признак силы, а не слабости."),

            (r'.*(изменила|изменил).*',
             "Измена - очень тяжелый момент, вам стоит постараться любым способом отвлечься от этого чтобы боль утихла."),
        ]

        self._create_ui()
        self._show_welcome()

    def _create_ui(self):
        self.chat_area = scrolledtext.ScrolledText(
            self.root, wrap=tk.WORD, font=("Arial", 12),
            bg="white", fg="#333", padx=15, pady=10
        )
        self.chat_area.pack(expand=True, fill='both', padx=10, pady=10)
        self.chat_area.config(state=tk.DISABLED)

        input_frame = tk.Frame(self.root, bg="#f0f2f5")
        input_frame.pack(fill='x', padx=10, pady=(0, 10))

        self.input_field = tk.Entry(
            input_frame, font=("Arial", 12), bd=2, relief=tk.GROOVE
        )
        self.input_field.pack(side=tk.LEFT, expand=True, fill='x', padx=(0, 10))
        self.input_field.bind("<Return>", lambda e: self.send_message())

        send_btn = tk.Button(
            input_frame, text="Отправить", font=("Arial", 11, "bold"),
            bg="#4CAF50", fg="white", relief=tk.FLAT, padx=20,
            command=self.send_message
        )
        send_btn.pack(side=tk.RIGHT)

        footer = tk.Label(
            self.root, text="❗ В кризисной ситуации обратитесь в службы поддержки:",
            fg="#d32f2f", bg="#f0f2f5", font=("Arial", 9, "bold"), cursor="hand2"
        )
        footer.pack(pady=(0, 5))
        footer.bind("<Button-1>", lambda e: self.show_crisis_contacts())

    def _show_welcome(self):
        self._add_message(
            "🤖 Бот поддержки",
            "Здравствуйте. Я здесь, чтобы выслушать вас без осуждения.\n\n"
            "⚠️ Важно: я не заменяю психолога или врача. При острых состояниях "
            "обратитесь к специалистам — контакты доступны по клику внизу окна.\n\n"
            "Как вы себя чувствуете сегодня?",
            sender_type="bot"
        )

    def send_message(self):
        user_text = self.input_field.get().strip()
        if not user_text:
            return

        self._add_message("👤 Вы", user_text, sender_type="user")
        self.input_field.delete(0, tk.END)

        if self._is_crisis(user_text):
            self._show_crisis_response()
            return

        bot_response = self._generate_response(user_text)
        self.root.after(800, lambda: self._add_message("🤖 Бот поддержки", bot_response, sender_type="bot"))

    def _is_crisis(self, text):
        text_lower = text.lower()
        return any(re.search(pattern, text_lower, re.IGNORECASE) for pattern in self.crisis_keywords)

    def _show_crisis_response(self):
        crisis_msg = (
            "🚨 Я заметил(а) слова, которые могут говорить о кризисном состоянии.\n\n"
            "Пожалуйста, обратитесь за помощью СЕЙЧАС:\n"
            "• Единый номер помощи при кризисных состояниях: 8-800-700-54-52 (бесплатно)\n"
            "• Телефон доверия для детей и подростков: 8-800-200-01-22\n"
            "• Служба психологической помощи МЧС: 8-800-100-72-30\n\n"
            "Вы не одни. Специалисты готовы поддержать вас 24/7."
        )
        self._add_message("🆘 ВАЖНО", crisis_msg, sender_type="bot")
        self.show_crisis_contacts()

    def _generate_response(self, text):
        text_lower = text.lower()

        for pattern, response in self.response_patterns:
            if re.search(pattern, text_lower, re.IGNORECASE):
                return response

        return (
            "Спасибо, что поделились этим со мной. Ваши чувства важны и заслуживают внимания.\n\n"
            "Хотите рассказать подробнее? Иногда проговаривание вслух уже помогает почувствовать себя легче."
        )

    def _add_message(self, sender, message, sender_type="user"):
        self.chat_area.config(state=tk.NORMAL)
        timestamp = datetime.now().strftime("%H:%M")

        if sender_type == "bot":
            self.chat_area.insert(tk.END, f"\n[{timestamp}] {sender}\n", "bot_header")
            self.chat_area.insert(tk.END, f"{message}\n", "bot_msg")
            self.chat_area.tag_config("bot_header", foreground="#1976d2", font=("Arial", 10, "bold"))
            self.chat_area.tag_config("bot_msg", foreground="#333", lmargin1=10, lmargin2=10)

        elif sender_type == "crisis":
            self.chat_area.insert(tk.END, f"\n[{timestamp}] {sender}\n", "crisis_header")
            self.chat_area.insert(tk.END, f"{message}\n", "crisis_msg")
            self.chat_area.tag_config("crisis_header", foreground="#d32f2f", font=("Arial", 11, "bold"))
            self.chat_area.tag_config("crisis_msg", foreground="#d32f2f", background="#ffebee", lmargin1=10,
                                      lmargin2=10)

        else:
            self.chat_area.insert(tk.END, f"\n[{timestamp}] {sender}\n", "user_header")
            self.chat_area.insert(tk.END, f"{message}\n", "user_msg")
            self.chat_area.tag_config("user_header", foreground="#388e3c", font=("Arial", 10, "bold"), justify='right')
            self.chat_area.tag_config("user_msg", foreground="#333", justify='right', lmargin1=100, rmargin=10)

        self.chat_area.insert(tk.END, "\n")
        self.chat_area.see(tk.END)
        self.chat_area.config(state=tk.DISABLED)

    def show_crisis_contacts(self):
        contacts = (
            "СПИСОК ЭКСТРЕННЫХ СЛУЖБ ПОДДЕРЖКИ (Россия):\n\n"
            "🔹 Единый номер помощи при суицидальных мыслях: 8-800-700-54-52\n"
            "🔹 Телефон доверия для детей и подростков: 8-800-200-01-22\n"
            "🔹 Служба психологической помощи МЧС: 8-800-100-72-30\n"
            "🔹 Линия помощи по зависимостям: 8-800-200-02-01\n"
            "🔹 Кризисная служба помощи женщинам: 8 (495) 915-80-80\n\n"
            "🌐 Международные ресурсы:\n"
            "• Find A Helpline (поиск служб по стране): https://findahelpline.com\n"
            "• Crisis Text Line (англ.): Text HOME to 741741\n\n"
            "💡 Совет: Сохраните эти номера в телефоне заранее."
        )

        messagebox.showinfo("Экстренные контакты", contacts)


if __name__ == "__main__":
    root = tk.Tk()
    app = SupportChatBot(root)
    root.mainloop()