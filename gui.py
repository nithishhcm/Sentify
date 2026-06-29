import customtkinter as ctk
from tkinter import messagebox
import threading
from sentify.scraper import get_reviews
from sentify.analyzer import analyze_sentiment

# Setup dark theme and general aesthetics
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class SentifyGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Sentify - Sentiment Analyzer")
        self.geometry("600x700")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        # Header
        self.header = ctk.CTkLabel(self, text="Sentify Analyzer", font=ctk.CTkFont(size=32, weight="bold"))
        self.header.grid(row=0, column=0, padx=20, pady=(30, 20))
        
        # Input Frame (Card-like appearance)
        self.input_frame = ctk.CTkFrame(self, corner_radius=15)
        self.input_frame.grid(row=1, column=0, padx=40, pady=10, sticky="nsew")
        self.input_frame.grid_columnconfigure(1, weight=1)
        
        # Title Input
        self.title_label = ctk.CTkLabel(self.input_frame, text="Title:", font=ctk.CTkFont(size=14, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")
        self.title_entry = ctk.CTkEntry(self.input_frame, placeholder_text="e.g. Dune", width=250, height=35)
        self.title_entry.grid(row=0, column=1, padx=20, pady=(20, 10), sticky="ew")
        
        # Type Dropdown
        self.type_label = ctk.CTkLabel(self.input_frame, text="Type:", font=ctk.CTkFont(size=14, weight="bold"))
        self.type_label.grid(row=1, column=0, padx=20, pady=10, sticky="w")
        self.type_menu = ctk.CTkOptionMenu(self.input_frame, values=["movie", "book"], height=35)
        self.type_menu.grid(row=1, column=1, padx=20, pady=10, sticky="ew")
        
        # Model Dropdown
        self.model_label = ctk.CTkLabel(self.input_frame, text="Model:", font=ctk.CTkFont(size=14, weight="bold"))
        self.model_label.grid(row=2, column=0, padx=20, pady=10, sticky="w")
        self.model_menu = ctk.CTkOptionMenu(self.input_frame, values=["textblob", "distilbert"], height=35)
        self.model_menu.grid(row=2, column=1, padx=20, pady=10, sticky="ew")
        
        # Limit Input
        self.limit_label = ctk.CTkLabel(self.input_frame, text="Limit:", font=ctk.CTkFont(size=14, weight="bold"))
        self.limit_label.grid(row=3, column=0, padx=20, pady=(10, 20), sticky="w")
        self.limit_entry = ctk.CTkEntry(self.input_frame, placeholder_text="30", width=100, height=35)
        self.limit_entry.insert(0, "30")
        self.limit_entry.grid(row=3, column=1, padx=20, pady=(10, 20), sticky="w")
        
        # Results Frame
        self.results_frame = ctk.CTkFrame(self, corner_radius=15)
        self.results_frame.grid(row=2, column=0, padx=40, pady=20, sticky="nsew")
        self.results_frame.grid_columnconfigure(0, weight=1)
        self.results_frame.grid_rowconfigure(1, weight=1)
        
        # Action Area (Button + Progress bar side by side)
        self.action_frame = ctk.CTkFrame(self.results_frame, fg_color="transparent")
        self.action_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        self.action_frame.grid_columnconfigure(1, weight=1)
        
        self.analyze_btn = ctk.CTkButton(self.action_frame, text="Analyze Sentiment", font=ctk.CTkFont(size=15, weight="bold"), height=40, command=self.start_analysis)
        self.analyze_btn.grid(row=0, column=0, sticky="w")
        
        self.progress = ctk.CTkProgressBar(self.action_frame, mode="indeterminate", width=150)
        self.progress.grid(row=0, column=1, padx=20, sticky="e")
        self.progress.set(0)
        
        # Results Text
        self.result_text = ctk.CTkTextbox(self.results_frame, font=ctk.CTkFont(family="Courier", size=14), state="disabled", fg_color="#1E1E1E", text_color="#A9B7C6")
        self.result_text.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        
    def start_analysis(self):
        title = self.title_entry.get().strip()
        if not title:
            messagebox.showwarning("Input Error", "Please enter a title.")
            return
            
        try:
            limit = int(self.limit_entry.get())
        except ValueError:
            messagebox.showwarning("Input Error", "Limit must be a number.")
            return
            
        # UI State update for loading
        self.analyze_btn.configure(state="disabled", text="Analyzing...")
        self.result_text.configure(state="normal")
        self.result_text.delete("0.0", "end")
        self.result_text.configure(state="disabled")
        
        self.progress.start()
        
        # Run backend logic in a thread to keep GUI smooth and animated
        threading.Thread(target=self.run_analysis, args=(title, self.type_menu.get(), self.model_menu.get(), limit), daemon=True).start()
        
    def run_analysis(self, title, item_type, model, limit):
        try:
            reviews = get_reviews(title, item_type, limit)
            if not reviews:
                self.update_ui_results("No reviews found.")
                return
                
            analysis = analyze_sentiment(reviews, model)
            
            # Format results
            total = analysis["reviews_analyzed"]
            pos = analysis["positive"]
            neg = analysis["negative"]
            neu = analysis["neutral"]
            
            pos_pct = int((pos / total) * 100) if total > 0 else 0
            neg_pct = int((neg / total) * 100) if total > 0 else 0
            neu_pct = int((neu / total) * 100) if total > 0 else 0
            
            pos_bar = "█" * int((pos_pct / 100) * 16)
            neg_bar = "█" * int((neg_pct / 100) * 16)
            neu_bar = "█" * int((neu_pct / 100) * 16)
            
            res_str = f"╭─ {title} ({item_type.capitalize()}) ─╮\n"
            res_str += f" Model: {model.capitalize()}\n"
            res_str += f" Reviews analyzed: {total}\n\n"
            res_str += f" ✅ Positive : {pos:<3} ({pos_pct:>2}%) {pos_bar}\n"
            res_str += f" ❌ Negative : {neg:<3} ({neg_pct:>2}%) {neg_bar}\n"
            res_str += f" ⬜ Neutral  : {neu:<3} ({neu_pct:>2}%) {neu_bar}\n\n"
            res_str += f" Avg sentiment score: {analysis['avg_score']:.2f}\n"
            res_str += f"╰{'─'*30}╯\n"
            
            # Use typewriter animation to display results
            self.typewriter_effect(res_str)
            
        except Exception as e:
            self.update_ui_results(f"An error occurred:\n{str(e)}")
            
    def update_ui_results(self, text):
        self.after(0, self._finish_analysis, text)
        
    def _finish_analysis(self, text):
        self.progress.stop()
        self.analyze_btn.configure(state="normal", text="Analyze Sentiment")
        self.result_text.configure(state="normal")
        self.result_text.insert("end", text)
        self.result_text.configure(state="disabled")

    def typewriter_effect(self, text, index=0):
        # Initial cleanup step
        if index == 0:
            self.after(0, lambda: self.progress.stop())
            self.after(0, lambda: self.analyze_btn.configure(state="normal", text="Analyze Sentiment"))
            self.after(0, lambda: self.result_text.configure(state="normal"))
            
        # Recursive typing animation
        if index < len(text):
            self.result_text.insert("end", text[index])
            self.result_text.see("end")
            self.after(10, self.typewriter_effect, text, index+1) # 10ms delay between characters
        else:
            self.result_text.configure(state="disabled")

def main():
    app = SentifyGUI()
    app.mainloop()

if __name__ == "__main__":
    main()
