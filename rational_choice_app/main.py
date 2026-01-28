import tkinter as tk
from tkinter import ttk
import numpy as np
from scipy.optimize import linprog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# --- CONSTANTS & STYLES ---
MAIN_COLOR = "#12618C"
OK_COLOR = "#21A659"
BAD_COLOR = "#D93840"
BG_COLOR = "#F4F4F4"

class GameTheoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Duality of Rational Choice")
        self.root.geometry("1000x750")
        self.root.configure(bg=BG_COLOR)

        # State Variables
        self.payoff_matrix = np.array([[4, 0, 2], [3, 3, 1], [0, 4, 0]], dtype=float)
        self.target_row = 2 
        self.domination_type = tk.StringVar(value="Strict")
        
        self._setup_ui()
        self.run_analysis()

    def _setup_ui(self):
        # Styles
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Header.TLabel", font=("Helvetica", 24, "bold"), foreground=MAIN_COLOR, background=BG_COLOR)
        style.configure("Bold.TLabel", font=("Helvetica", 12, "bold"), background="white", foreground="#444")

        # Header
        header = tk.Frame(self.root, bg=BG_COLOR)
        header.pack(fill="x", padx=20, pady=10)
        ttk.Label(header, text="Duality of Rational Choice", style="Header.TLabel").pack(side="left")
        ttk.Label(header, text="Pearce's Lemma Tool", background=BG_COLOR, foreground="#666").pack(side="right", anchor="s")

        # Main Layout
        main_frame = tk.Frame(self.root, bg=BG_COLOR)
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.left_col = tk.Frame(main_frame, bg="white", highlightbackground="#ccc", highlightthickness=1)
        self.left_col.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        self.right_col = tk.Frame(main_frame, bg="white", highlightbackground="#ccc", highlightthickness=1)
        self.right_col.pack(side="right", fill="both", expand=True, padx=(10, 0))

        self._build_input_panel()
        self._build_results_panel()

    def _build_input_panel(self):
        # Controls
        ctrl_frame = tk.Frame(self.left_col, bg="white", padx=15, pady=15)
        ctrl_frame.pack(fill="x")
        
        ttk.Label(ctrl_frame, text="Matrix Configuration", style="Bold.TLabel").pack(anchor="w")
        btn_frame = tk.Frame(ctrl_frame, bg="white", pady=5)
        btn_frame.pack(anchor="w")
        
        for txt, cmd in [("- Row", self.rem_row), ("+ Row", self.add_row), 
                         ("- Col", self.rem_col), ("+ Col", self.add_col)]:
            tk.Button(btn_frame, text=txt, command=cmd, width=6).pack(side="left", padx=2)

        # Matrix Grid
        ttk.Label(self.left_col, text="Payoff Matrix", style="Bold.TLabel").pack(anchor="w", padx=15)
        self.matrix_container = tk.Frame(self.left_col, bg="white")
        self.matrix_container.pack(fill="both", expand=True, padx=15, pady=5)
        self._render_matrix_grid()

        # Domination Type
        type_frame = tk.Frame(self.left_col, bg="white", padx=15, pady=15)
        type_frame.pack(fill="x")
        ttk.Label(type_frame, text="Domination Type", style="Bold.TLabel").pack(anchor="w")
        
        for val, txt in [("Strict", "Strict Domination"), ("Weak", "Weak Domination"), ("Redundant", "Redundancy")]:
            tk.Radiobutton(type_frame, text=txt, variable=self.domination_type, value=val, 
                           bg="white", command=self.run_analysis).pack(anchor="w")

    def _build_results_panel(self):
        res_frame = tk.Frame(self.right_col, bg="white", padx=15, pady=15)
        res_frame.pack(fill="both", expand=True)
        
        ttk.Label(res_frame, text="Analysis Results", style="Bold.TLabel").pack(anchor="w")
        
        # Verdict Box
        self.verdict_frame = tk.Frame(res_frame, bg="#ccc", padx=10, pady=10)
        self.verdict_frame.pack(fill="x", pady=10)
        
        self.lbl_verdict = tk.Label(self.verdict_frame, font=("Helvetica", 16, "bold"), fg="white", bg="#ccc")
        self.lbl_verdict.pack()
        self.lbl_desc = tk.Label(self.verdict_frame, font=("Helvetica", 10), fg="white", bg="#ccc")
        self.lbl_desc.pack()
        self.lbl_val = tk.Label(self.verdict_frame, font=("Helvetica", 9), fg="#eee", bg="#ccc")
        self.lbl_val.pack()

        # Plots
        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(5, 3.5))
        self.fig.tight_layout(pad=3.0)
        self.canvas = FigureCanvasTkAgg(self.fig, master=res_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def _render_matrix_grid(self):
        for w in self.matrix_container.winfo_children(): w.destroy()
        
        rows, cols = self.payoff_matrix.shape
        for j in range(cols):
            tk.Label(self.matrix_container, text=f"Opp {j+1}", bg="white", fg="#888").grid(row=0, column=j+1)

        for i in range(rows):
            style = "sunken" if i == self.target_row else "raised"
            bg = MAIN_COLOR if i == self.target_row else "#eee"
            fg = "white" if i == self.target_row else "black"
            
            cmd = lambda r=i: self.set_target(r)
            tk.Button(self.matrix_container, text=f"Action {i+1}", bg=bg, fg=fg, relief=style, command=cmd).grid(row=i+1, column=0, sticky="ew")
            
            for j in range(cols):
                sv = tk.StringVar(value=str(self.payoff_matrix[i, j]))
                sv.trace_add("write", lambda n, x, m, r=i, c=j, v=sv: self.on_change(r, c, v))
                tk.Entry(self.matrix_container, textvariable=sv, width=6, justify="center").grid(row=i+1, column=j+1, padx=2, pady=2)

    def on_change(self, r, c, var):
        try:
            self.payoff_matrix[r, c] = float(var.get())
            self.run_analysis()
        except ValueError: pass

    def set_target(self, r):
        self.target_row = r
        self._render_matrix_grid()
        self.run_analysis()

    def add_row(self):
        self.payoff_matrix = np.vstack([self.payoff_matrix, np.zeros(self.payoff_matrix.shape[1])])
        self._render_matrix_grid()
        self.run_analysis()

    def rem_row(self):
        if self.payoff_matrix.shape[0] > 2:
            self.payoff_matrix = self.payoff_matrix[:-1]
            self.target_row = min(self.target_row, self.payoff_matrix.shape[0]-1)
            self._render_matrix_grid()
            self.run_analysis()

    def add_col(self):
        self.payoff_matrix = np.hstack([self.payoff_matrix, np.zeros((self.payoff_matrix.shape[0], 1))])
        self._render_matrix_grid()
        self.run_analysis()

    def rem_col(self):
        if self.payoff_matrix.shape[1] > 2:
            self.payoff_matrix = self.payoff_matrix[:, :-1]
            self._render_matrix_grid()
            self.run_analysis()

    def solve(self):
        M = self.payoff_matrix
        target = self.target_row
        d_type = self.domination_type.get()
        n_rows, n_cols = M.shape
        u_target = M[target]

        # Primal Solver (Domination)
        # Using simplified logic for brevity while maintaining correctness
        c = np.zeros(n_rows + 1)
        c[-1] = -1 # Maximize eps/delta
        
        A_ub, bounds, A_eq = [], [], []
        
        if d_type == "Strict" or d_type == "Redundant":
            # eps - Sum(p*M) <= -u_target
            for j in range(n_cols):
                row = list(-M[:, j]) + [1]
                A_ub.append(row)
            b_ub = -u_target
            A_eq = [np.append(np.ones(n_rows), 0)]
            bounds = [(0, None)] * n_rows + [(None, None)]
            
            if d_type == "Redundant": bounds[target] = (0, 0)
            
            res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=[1], bounds=bounds, method='highs')
            dom = res.success and res.x[-1] > (1e-7 if d_type == "Strict" else -1e-7)
            strat = res.x[:n_rows] if res.success else np.zeros(n_rows)
            val = res.x[-1] if res.success else 0

        else: # Weak
            # Max sum(deltas)
            num_vars = n_rows + n_cols
            c = np.zeros(num_vars)
            c[n_rows:] = -1
            
            for j in range(n_cols):
                row = np.zeros(num_vars)
                row[:n_rows] = -M[:, j]
                row[n_rows+j] = 1
                A_ub.append(row)
            b_ub = -u_target
            A_eq = [np.pad(np.ones(n_rows), (0, n_cols))]
            bounds = [(0, None)] * num_vars
            
            res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=[1], bounds=bounds, method='highs')
            dom = res.success and np.sum(res.x[n_rows:]) > 1e-7
            strat = res.x[:n_rows] if res.success else np.zeros(n_rows)
            val = np.sum(res.x[n_rows:]) if res.success else 0

        # Dual Solver (Belief)
        belief = np.zeros(n_cols)
        if not dom:
            d_c = np.zeros(n_cols + (1 if d_type != "Strict" else 0))
            if d_type != "Strict": d_c[-1] = -1
            
            d_A_ub, d_b_ub = [], []
            
            # (u_i - u_target).q <= 0 (+ eps if redundant)
            for i in range(n_rows):
                if d_type == "Redundant" and i == target: continue
                row = M[i] - u_target
                if d_type == "Redundant": row = np.append(row, 1)
                elif d_type == "Weak": row = np.append(row, 0)
                d_A_ub.append(row)
                d_b_ub.append(0)

            if d_type == "Weak": # q >= eps
                for j in range(n_cols):
                    row = np.zeros(n_cols + 1)
                    row[j], row[-1] = -1, 1
                    d_A_ub.append(row)
                    d_b_ub.append(0)

            d_A_eq = [np.ones(n_cols)]
            if d_type != "Strict": d_A_eq[0] = np.append(d_A_eq[0], 0)
            
            d_bounds = [(0, None)] * len(d_c)
            if d_type == "Redundant": d_bounds[-1] = (None, None)
            
            res_d = linprog(d_c, A_ub=d_A_ub, b_ub=d_b_ub, A_eq=d_A_eq, b_eq=[1], bounds=d_bounds, method='highs')
            if res_d.success: belief = res_d.x[:n_cols]

        return dom, val, strat, belief

    def run_analysis(self):
        dom, val, strat, belief = self.solve()
        
        # Update Verdict
        color = BAD_COLOR if dom else OK_COLOR
        self.verdict_frame.config(bg=color)
        self.lbl_verdict.config(bg=color, text=f"Action {self.target_row+1} is {'Dominated' if dom else 'Justifiable'}")
        self.lbl_val.config(bg=color, text=f"Primal Val: {val:.5f}")
        
        msgs = {
            "Strict": ("Strictly dominated", "Best response exists"),
            "Weak": ("Weakly dominated", "Full-support best response exists"),
            "Redundant": ("Better strategy exists elsewhere", "Unique best response exists")
        }
        self.lbl_desc.config(bg=color, text=msgs[self.domination_type.get()][0 if dom else 1])

        # Charts
        self.ax1.clear(); self.ax2.clear()
        
        if dom:
            self.ax1.bar(range(len(strat)), strat, color="#B3CDE0")
            self.ax1.set_title("Dominating Strategy")
            self.ax2.text(0.5, 0.5, "No Belief", ha='center')
        else:
            self.ax1.text(0.5, 0.5, "No Dom Strategy", ha='center')
            self.ax2.bar(range(len(belief)), belief, color="#CDE0B3")
            self.ax2.set_title("Rationalizing Belief")
            
        self.canvas.draw()

def main():
    root = tk.Tk()
    GameTheoryApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
