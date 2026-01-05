import tkinter as tk
from tkinter import ttk, messagebox

class DiagonalValidatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("The 'Landlord' Trade Validator")
        self.root.geometry("600x650")
        
        # Styles
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TLabel", font=("Helvetica", 11))
        style.configure("Header.TLabel", font=("Helvetica", 14, "bold"), foreground="#006400")
        style.configure("SubHeader.TLabel", font=("Helvetica", 10, "bold"), foreground="gray")
        
        # Main Container
        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Header
        header = ttk.Label(main_frame, text="The 'Landlord' Trade Validator", style="Header.TLabel")
        header.pack(pady=(0, 5))
        desc = ttk.Label(main_frame, text="Validate Diagonal Spreads / PMCCs before you buy.", font=("Helvetica", 9))
        desc.pack(pady=(0, 20))

        # --- INPUTS ---
        input_frame = ttk.LabelFrame(main_frame, text="Trade Inputs", padding="15")
        input_frame.pack(fill=tk.X, pady=10)

        # Grid layout for inputs
        # Row 0: Ticker & Current Price
        ttk.Label(input_frame, text="Ticker Symbol:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.ticker_var = tk.StringVar(value="MSFT")
        ttk.Entry(input_frame, textvariable=self.ticker_var, width=15).grid(row=0, column=1, pady=5)

        ttk.Label(input_frame, text="Current Stock Price ($):").grid(row=0, column=2, sticky=tk.W, pady=5, padx=(20, 0))
        self.current_price_var = tk.DoubleVar(value=473.00)
        ttk.Entry(input_frame, textvariable=self.current_price_var, width=15).grid(row=0, column=3, pady=5)

        # Row 1: Long Strike & Cost
        ttk.Label(input_frame, text="Long Strike (The House) $:", foreground="blue").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.long_strike_var = tk.DoubleVar(value=455.00)
        ttk.Entry(input_frame, textvariable=self.long_strike_var, width=15).grid(row=1, column=1, pady=5)

        ttk.Label(input_frame, text="Long Option Cost ($):", foreground="blue").grid(row=1, column=2, sticky=tk.W, pady=5, padx=(20, 0))
        self.long_cost_var = tk.DoubleVar(value=33.75)
        ttk.Entry(input_frame, textvariable=self.long_cost_var, width=15).grid(row=1, column=3, pady=5)

        # Row 2: Short Strike & Credit
        ttk.Label(input_frame, text="Short Strike (The Rent) $:", foreground="green").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.short_strike_var = tk.DoubleVar(value=490.00)
        ttk.Entry(input_frame, textvariable=self.short_strike_var, width=15).grid(row=2, column=1, pady=5)

        ttk.Label(input_frame, text="Premium Received ($):", foreground="green").grid(row=2, column=2, sticky=tk.W, pady=5, padx=(20, 0))
        self.short_credit_var = tk.DoubleVar(value=1.50)
        ttk.Entry(input_frame, textvariable=self.short_credit_var, width=15).grid(row=2, column=3, pady=5)

        # Calculate Button
        btn = ttk.Button(main_frame, text="RUN VALIDATION", command=self.calculate)
        btn.pack(pady=20, ipadx=10, ipady=5)

        # --- RESULTS ---
        self.result_frame = tk.Frame(main_frame, bg="#f0f0f0", bd=2, relief=tk.GROOVE)
        self.result_frame.pack(fill=tk.X, pady=10, ipady=10)

        self.status_label = tk.Label(self.result_frame, text="Ready to Calculate", font=("Helvetica", 14, "bold"), bg="#f0f0f0", fg="#333")
        self.status_label.pack(pady=5)
        
        self.msg_label = tk.Label(self.result_frame, text="", font=("Helvetica", 10), bg="#f0f0f0", wraplength=500)
        self.msg_label.pack(pady=5)

        # --- METRICS DISPLAY ---
        metrics_frame = ttk.Frame(main_frame)
        metrics_frame.pack(fill=tk.X, pady=10)
        
        # Columns for metrics
        self.metric_debit = self.create_metric_box(metrics_frame, "Total Risk (Debit)", 0)
        self.metric_profit = self.create_metric_box(metrics_frame, "Golden Rule Profit", 1)
        self.metric_breakeven = self.create_metric_box(metrics_frame, "Breakeven Price", 2)

        # Initial Calculation
        self.calculate()

    def create_metric_box(self, parent, title, col):
        frame = ttk.Frame(parent, padding=10, relief=tk.RIDGE, borderwidth=1)
        frame.grid(row=0, column=col, padx=5, sticky="ew")
        parent.columnconfigure(col, weight=1)
        
        ttk.Label(frame, text=title, font=("Helvetica", 8)).pack()
        value_label = ttk.Label(frame, text="---", font=("Courier", 12, "bold"))
        value_label.pack()
        return value_label

    def calculate(self):
        try:
            # Get Inputs
            current = self.current_price_var.get()
            l_strike = self.long_strike_var.get()
            l_cost = self.long_cost_var.get()
            s_strike = self.short_strike_var.get()
            s_credit = self.short_credit_var.get()

            # Math
            width = s_strike - l_strike
            net_debit = l_cost - s_credit
            profit_assigned = width - net_debit
            breakeven = l_strike + net_debit

            # Update Metrics
            self.metric_debit.config(text=f"${net_debit * 100:.0f}")
            self.metric_profit.config(text=f"${profit_assigned * 100:.0f}", foreground="green" if profit_assigned > 0 else "red")
            self.metric_breakeven.config(text=f"${breakeven:.2f}")

            # Validation Logic
            if s_strike <= l_strike:
                self.set_status("CRITICAL ERROR", "Short Strike must be HIGHER than Long Strike.", "red")
            elif profit_assigned < 0:
                self.set_status("TRAP DETECTED", "If the stock rallies, you will LOCK IN A LOSS. Raise your short strike.", "orange")
            elif s_strike < breakeven:
                self.set_status("CAUTION", "Selling below breakeven. Ensure you are willing to cap profit here.", "#d4af37") # Gold color
            else:
                self.set_status("TRADE APPROVED", "Green Light: Structure is sound. Upside is uncapped or profitable.", "green")

        except tk.TclError:
            messagebox.showerror("Input Error", "Please enter valid numbers only.")

    def set_status(self, title, msg, color):
        self.status_label.config(text=title, fg=color)
        self.msg_label.config(text=msg)
        # Light background tint based on status
        bg_color = "#e8f5e9" if color == "green" else "#ffebee" if color == "red" else "#fff3e0"
        self.result_frame.config(bg=bg_color)
        self.status_label.config(bg=bg_color)
        self.msg_label.config(bg=bg_color)

if __name__ == "__main__":
    root = tk.Tk()
    app = DiagonalValidatorApp(root)
    root.mainloop()