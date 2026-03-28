"""
Resolution in Artificial Intelligence - CO3
GUI Interface | Created by Anmol Rai
Run: python gui.py
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading, re
from datetime import datetime

# ── COLOURS ────────────────────────────────────────────────────
C = {
    "bg":      "#1C0306",
    "surface": "#2A0608",
    "raised":  "#380A0C",
    "input":   "#3D0C10",
    "border":  "#5A1018",
    "accent":  "#CD1C18",
    "salmon":  "#FFA896",
    "dark":    "#9B1313",
    "deep":    "#38000A",
    "text":    "#FFE8E4",
    "muted":   "#C89090",
    "faint":   "#7A4040",
    "green":   "#7ED88C",
    "white":   "#FFF5F3",
}

# ── NORMALISE ──────────────────────────────────────────────────
def norm(clause):
    parts = [p.strip() for p in clause.split("∨")]
    out = []
    for p in parts:
        p = re.sub(r'\s*,\s*', ',', p)
        p = re.sub(r'\(\s+', '(', p)
        p = re.sub(r'\s+\)', ')', p)
        out.append(p.strip())
    return " ∨ ".join(out)

# ── RESOLUTION ENGINE ──────────────────────────────────────────
class ResolutionEngine:
    def resolve_pair(self, c1, c2):
        l1 = [x.strip() for x in c1.split("∨")]
        l2 = [x.strip() for x in c2.split("∨")]
        for lit in l1:
            comp = lit[1:] if lit.startswith("¬") else f"¬{lit}"
            if comp in l2:
                rem = [x for x in l1 if x != lit] + [x for x in l2 if x != comp]
                rem = list(dict.fromkeys(rem))
                return norm(" ∨ ".join(rem)) if rem else "⊥"
        return None

    def prove(self, clauses, neg_goal):
        ws   = [norm(c) for c in clauses]
        ng   = norm(neg_goal)
        if ng not in ws:
            ws.append(ng)
        steps = [("INIT", None, None, None, list(ws))]
        seen  = set(ws)
        for _ in range(200):
            new = []
            for i in range(len(ws)):
                for j in range(i + 1, len(ws)):
                    r = self.resolve_pair(ws[i], ws[j])
                    if r is not None:
                        tag = "EMPTY" if r == "⊥" else "STEP"
                        steps.append((tag, ws[i], ws[j], r, []))
                        if r == "⊥":
                            steps.append(("PROVED", None, None, None, []))
                            return True, steps
                        if r not in seen:
                            new.append(r); seen.add(r)
            if not new:
                steps.append(("FAILED", None, None, None, []))
                return False, steps
            ws.extend(new)
        steps.append(("TIMEOUT", None, None, None, []))
        return False, steps

# ── PRESETS ────────────────────────────────────────────────────
PRESETS = {
    "1": {
        "name": "West is a Criminal",
        "desc": "West sells missiles to Nano (hostile nation). Prove he is a criminal.",
        "fol": [
            "∀x∀y∀z (American(x) ∧ Weapon(y) ∧ Sells(x,y,z) ∧ Hostile(z) → Criminal(x))",
            "Hostile(Nano)",
            "American(West)",
            "Missile(M1)",
            "∀x (Missile(x) → Weapon(x))",
            "Sells(West, M1, Nano)",
        ],
        "clauses": [
            "¬American(West) ∨ ¬Weapon(M1) ∨ ¬Sells(West,M1,Nano) ∨ ¬Hostile(Nano) ∨ Criminal(West)",
            "Hostile(Nano)",
            "American(West)",
            "Missile(M1)",
            "¬Missile(M1) ∨ Weapon(M1)",
            "Sells(West,M1,Nano)",
            "Weapon(M1)",
        ],
        "goal":     "Criminal(West)",
        "neg_goal": "¬Criminal(West)",
    },
    "2": {
        "name": "Socrates is Mortal",
        "desc": "All humans are mortal. Socrates is human. Prove: Socrates is mortal.",
        "fol": [
            "∀x (Human(x) → Mortal(x))",
            "Human(Socrates)",
        ],
        "clauses": [
            "¬Human(Socrates) ∨ Mortal(Socrates)",
            "Human(Socrates)",
        ],
        "goal":     "Mortal(Socrates)",
        "neg_goal": "¬Mortal(Socrates)",
    },
    "3": {
        "name": "John Likes All Food",
        "desc": "John likes every food. Peanuts is food. Prove: John likes peanuts.",
        "fol": [
            "∀x (Food(x) → Likes(John,x))",
            "Food(Peanuts)",
        ],
        "clauses": [
            "¬Food(Peanuts) ∨ Likes(John,Peanuts)",
            "Food(Peanuts)",
        ],
        "goal":     "Likes(John,Peanuts)",
        "neg_goal": "¬Likes(John,Peanuts)",
    },
}

# ── GUI APP ────────────────────────────────────────────────────
class App:
    def __init__(self):
        self.root = tk.Tk()
        self.clauses = []
        self.running = False
        self._setup()
        self._build()
        self._load("1")
        self.root.mainloop()

    def _setup(self):
        self.root.title("Resolution AI  ·  CO3  ·  Anmol Rai")
        self.root.geometry("1300x820")
        self.root.minsize(1000, 640)
        self.root.configure(bg=C["bg"])
        # centre window
        self.root.update_idletasks()
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x  = (sw - 1300) // 2
        y  = (sh - 820)  // 2
        self.root.geometry(f"1300x820+{x}+{y}")

    def _build(self):
        # ── header ──────────────────────────────────────────────
        hdr = tk.Frame(self.root, bg=C["deep"], height=66)
        hdr.pack(fill="x"); hdr.pack_propagate(False)

        lh = tk.Frame(hdr, bg=C["deep"])
        lh.pack(side="left", padx=18, pady=8)
        tk.Label(lh, text="◈  RESOLUTION AI",
                 font=("Consolas", 20, "bold"),
                 bg=C["deep"], fg=C["accent"]).pack(anchor="w")
        tk.Label(lh, text="Automated Theorem Prover  ·  FOL  ·  CNF  ·  CO3",
                 font=("Consolas", 9),
                 bg=C["deep"], fg=C["muted"]).pack(anchor="w")

        rh = tk.Frame(hdr, bg=C["deep"])
        rh.pack(side="right", padx=18, pady=10)
        bdg = tk.Frame(rh, bg=C["accent"], padx=12, pady=6)
        bdg.pack(side="right")
        tk.Label(bdg, text="✦  Anmol Rai",
                 font=("Consolas", 9, "bold"),
                 bg=C["accent"], fg=C["white"]).pack()
        self.status = tk.StringVar(value="● READY")
        tk.Label(rh, textvariable=self.status,
                 font=("Consolas", 10, "bold"),
                 bg=C["deep"], fg=C["salmon"]).pack(side="right", padx=(0,12))

        tk.Frame(self.root, bg=C["accent"], height=2).pack(fill="x")

        # ── toolbar ─────────────────────────────────────────────
        tb = tk.Frame(self.root, bg=C["surface"], pady=8)
        tb.pack(fill="x")

        tk.Label(tb, text="PRESET:", font=("Consolas", 9, "bold"),
                 bg=C["surface"], fg=C["muted"]).pack(side="left", padx=(14, 6))

        self.preset_var = tk.StringVar(value="West is a Criminal")
        cb = ttk.Combobox(tb, textvariable=self.preset_var,
                          values=[v["name"] for v in PRESETS.values()] + ["Custom"],
                          state="readonly", width=26, font=("Consolas", 10))
        cb.pack(side="left", padx=(0, 14))
        cb.bind("<<ComboboxSelected>>", self._on_preset)

        for label, cmd, colour in [
            ("▶  PROVE",      self._prove,      C["accent"]),
            ("⟳  RESET",      self._reset,       C["dark"]),
            ("＋  ADD CLAUSE", self._add_clause,  C["salmon"]),
            ("✕  CLEAR",      self._clear,        C["dark"]),
            ("⬇  EXPORT",     self._export,       C["green"]),
        ]:
            self._btn(tb, label, cmd, colour).pack(side="left", padx=3)

        tk.Frame(self.root, bg=C["border"], height=1).pack(fill="x")

        # ── body ────────────────────────────────────────────────
        body = tk.PanedWindow(self.root, orient="horizontal",
                              bg=C["bg"], sashwidth=4, sashrelief="flat")
        body.pack(fill="both", expand=True, padx=8, pady=6)

        # left panel
        left = tk.Frame(body, bg=C["bg"])
        body.add(left, minsize=330)

        self._section(left, "PROBLEM DESCRIPTION")
        self.desc_box = tk.Text(left, height=4, font=("Consolas", 10),
                                bg=C["surface"], fg=C["muted"],
                                relief="flat", padx=10, pady=8,
                                wrap="word", state="disabled", bd=0,
                                highlightthickness=1,
                                highlightbackground=C["border"])
        self.desc_box.pack(fill="x", padx=5, pady=(0, 7))

        self._section(left, "FIRST-ORDER LOGIC")
        self.fol_box = scrolledtext.ScrolledText(
            left, height=5, font=("Courier New", 10),
            bg=C["surface"], fg=C["salmon"],
            relief="flat", padx=10, pady=8,
            state="disabled", bd=0,
            highlightthickness=1, highlightbackground=C["border"])
        self.fol_box.pack(fill="x", padx=5, pady=(0, 7))

        self._section(left, "CNF CLAUSES")
        clause_frame = tk.Frame(left, bg=C["surface"],
                                highlightthickness=1,
                                highlightbackground=C["border"])
        clause_frame.pack(fill="both", expand=True, padx=5, pady=(0, 7))
        self.clause_lb = tk.Listbox(clause_frame, font=("Courier New", 10),
                                     bg=C["surface"], fg=C["text"],
                                     selectbackground=C["raised"],
                                     selectforeground=C["salmon"],
                                     activestyle="none", relief="flat",
                                     borderwidth=0, highlightthickness=0)
        sc = tk.Scrollbar(clause_frame, command=self.clause_lb.yview,
                          bg=C["raised"], troughcolor=C["surface"])
        self.clause_lb.configure(yscrollcommand=sc.set)
        sc.pack(side="right", fill="y")
        self.clause_lb.pack(fill="both", expand=True, padx=6, pady=6)

        self._section(left, "NEGATED GOAL")
        gf = tk.Frame(left, bg=C["surface"],
                      highlightthickness=1, highlightbackground=C["accent"])
        gf.pack(fill="x", padx=5)
        self.ng_var = tk.StringVar()
        tk.Entry(gf, textvariable=self.ng_var,
                 font=("Courier New", 11),
                 bg=C["input"], fg=C["accent"],
                 insertbackground=C["accent"],
                 relief="flat", bd=7).pack(fill="x", padx=2, pady=2)

        # right panel
        right = tk.Frame(body, bg=C["bg"])
        body.add(right, minsize=430)

        self._section(right, "PROOF STEPS")
        self.proof_box = scrolledtext.ScrolledText(
            right, font=("Courier New", 10),
            bg=C["surface"], fg=C["text"],
            relief="flat", padx=14, pady=10,
            state="disabled", bd=0,
            highlightthickness=1, highlightbackground=C["border"],
            wrap="word")
        self.proof_box.pack(fill="both", expand=True, padx=5, pady=(0, 6))

        # colour tags
        self.proof_box.tag_configure("hdr",  foreground=C["accent"],
                                     font=("Consolas", 11, "bold"))
        self.proof_box.tag_configure("init", foreground=C["salmon"],
                                     font=("Courier New", 10, "bold"))
        self.proof_box.tag_configure("step", foreground=C["muted"])
        self.proof_box.tag_configure("cls",  foreground=C["faint"])
        self.proof_box.tag_configure("res",  foreground=C["salmon"],
                                     font=("Courier New", 10, "bold"))
        self.proof_box.tag_configure("emp",  foreground=C["accent"],
                                     font=("Courier New", 11, "bold"))
        self.proof_box.tag_configure("arr",  foreground=C["dark"])
        self.proof_box.tag_configure("ok",   foreground=C["green"],
                                     font=("Consolas", 12, "bold"))
        self.proof_box.tag_configure("fail", foreground=C["accent"],
                                     font=("Consolas", 12, "bold"))
        self.proof_box.tag_configure("dim",  foreground=C["faint"],
                                     font=("Courier New", 9))

        # result label (replaces buggy progressbar style)
        self.result_lbl = tk.Label(right, text="",
                                   font=("Consolas", 11, "bold"),
                                   bg=C["bg"], fg=C["muted"], pady=6)
        self.result_lbl.pack(fill="x", padx=5)

        # simple canvas progress bar — avoids ttk style bug on Windows
        self.pb_canvas = tk.Canvas(right, height=4,
                                   bg=C["surface"], highlightthickness=0)
        self.pb_canvas.pack(fill="x", padx=5, pady=(0, 4))
        self._pb_rect = None
        self._pb_pos  = 0
        self._pb_running = False

        # ── footer ──────────────────────────────────────────────
        tk.Frame(self.root, bg=C["accent"], height=1).pack(fill="x")
        ft = tk.Frame(self.root, bg=C["deep"], height=26)
        ft.pack(fill="x"); ft.pack_propagate(False)
        tk.Label(ft, text=f"CO3 — Resolution in AI  |  Anmol Rai  |  {datetime.now().year}",
                 font=("Consolas", 8), bg=C["deep"], fg=C["faint"]).pack(side="left", padx=12)

    # ── helpers ────────────────────────────────────────────────
    def _section(self, parent, text):
        f = tk.Frame(parent, bg=C["bg"])
        f.pack(fill="x", padx=5, pady=(5, 2))
        tk.Label(f, text=f"◈  {text}",
                 font=("Consolas", 9, "bold"),
                 bg=C["bg"], fg=C["muted"]).pack(side="left")
        tk.Frame(f, bg=C["border"], height=1).pack(
            side="left", fill="x", expand=True, padx=(8, 0))

    def _btn(self, parent, text, cmd, fg):
        b = tk.Button(parent, text=text, command=cmd,
                      font=("Consolas", 9, "bold"),
                      bg=C["surface"], fg=fg,
                      activebackground=C["raised"], activeforeground=fg,
                      relief="flat", padx=10, pady=5, cursor="hand2",
                      bd=0, highlightthickness=1, highlightbackground=fg)
        b.bind("<Enter>", lambda _: b.config(bg=C["raised"]))
        b.bind("<Leave>", lambda _: b.config(bg=C["surface"]))
        return b

    def _set_text(self, widget, text):
        widget.config(state="normal")
        widget.delete("1.0", "end")
        widget.insert("end", text)
        widget.config(state="disabled")

    # ── progress bar (canvas-based, no ttk style needed) ───────
    def _pb_start(self):
        self._pb_running = True
        self._pb_pos = 0
        self._pb_animate()

    def _pb_stop(self):
        self._pb_running = False
        self.pb_canvas.delete("all")

    def _pb_animate(self):
        if not self._pb_running:
            return
        w = self.pb_canvas.winfo_width() or 400
        self.pb_canvas.delete("all")
        self.pb_canvas.configure(bg=C["surface"])
        # moving block
        block_w = w // 5
        x = self._pb_pos % (w + block_w) - block_w
        self.pb_canvas.create_rectangle(x, 0, x + block_w, 4,
                                         fill=C["accent"], outline="")
        self._pb_pos += 12
        self.root.after(30, self._pb_animate)

    # ── load preset ────────────────────────────────────────────
    def _on_preset(self, _=None):
        name = self.preset_var.get()
        for k, v in PRESETS.items():
            if v["name"] == name:
                self._load(k); return
        # custom mode
        self.clauses = []; self.ng_var.set("")
        self._refresh_clauses()

    def _load(self, key):
        p = PRESETS[key]
        self.clauses = list(p["clauses"])
        self.ng_var.set(p["neg_goal"])
        self.preset_var.set(p["name"])
        self._set_text(self.desc_box, p["desc"])
        fol_str = "\n".join(f"  {i+1}. {f}" for i, f in enumerate(p["fol"]))
        self._set_text(self.fol_box, fol_str)
        self._refresh_clauses()
        self._set_text(self.proof_box,
                       f"\n  '{p['name']}' loaded.  Press ▶ PROVE to run.\n")
        self.result_lbl.config(text="", bg=C["bg"])
        self.status.set("● READY")

    def _refresh_clauses(self):
        self.clause_lb.delete(0, "end")
        for i, c in enumerate(self.clauses):
            self.clause_lb.insert("end", f"  [{i+1}]  {c}")
            self.clause_lb.itemconfig(i,
                fg=C["salmon"] if i % 2 == 0 else C["text"])
        ng = self.ng_var.get()
        if ng:
            self.clause_lb.insert("end", f"  [¬G]  {ng}  ← Negated Goal")
            self.clause_lb.itemconfig(len(self.clauses), fg=C["accent"])

    # ── prove ──────────────────────────────────────────────────
    def _prove(self):
        if self.running: return
        clauses = list(self.clauses)
        ng      = self.ng_var.get().strip()
        if not clauses:
            messagebox.showwarning("No Clauses", "Add at least one CNF clause.")
            return
        if not ng:
            messagebox.showwarning("No Goal", "Enter the negated goal.")
            return

        self.running = True
        self.status.set("⟳ PROVING...")
        self._pb_start()
        self.result_lbl.config(text="", bg=C["bg"])
        self._set_text(self.proof_box, "")

        def task():
            proved, steps = ResolutionEngine().prove(clauses, ng)
            self.root.after(0, lambda: self._show_proof(proved, steps))

        threading.Thread(target=task, daemon=True).start()

    def _show_proof(self, proved, steps):
        self._pb_stop()
        self.running = False
        pt = self.proof_box
        pt.config(state="normal"); pt.delete("1.0", "end")

        ts = datetime.now().strftime("%H:%M:%S")
        pt.insert("end", f"╔{'═'*58}╗\n", "hdr")
        pt.insert("end", f"║  PROOF  —  {ts:<46}║\n", "hdr")
        pt.insert("end", f"╚{'═'*58}╝\n\n", "hdr")

        sn = 0
        for lbl, c1, c2, res, init in steps:
            if lbl == "INIT":
                pt.insert("end", "  ◆ INITIAL STATE\n", "init")
                for i, line in enumerate(init):
                    pt.insert("end", f"    [{i+1}] {line}\n", "cls")
                pt.insert("end", "\n")

            elif lbl in ("STEP", "EMPTY"):
                sn += 1
                tag = "fail" if lbl == "EMPTY" else "step"
                pt.insert("end", f"  ─ Step {sn}:\n", tag)
                pt.insert("end", f"    P: {c1}\n", "cls")
                pt.insert("end", f"    Q: {c2}\n", "cls")
                pt.insert("end", "    ⇒ ", "arr")
                if lbl == "EMPTY":
                    pt.insert("end", "⊥  (Empty Clause — Contradiction!)\n\n", "emp")
                else:
                    pt.insert("end", f"{res}\n\n", "res")

            elif lbl == "PROVED":
                pt.insert("end", f"\n{'─'*60}\n", "dim")
                pt.insert("end", "  ✔  GOAL PROVED — Contradiction found!\n", "ok")
                self.result_lbl.config(
                    text="  ✔  GOAL PROVED  ✔ ",
                    bg=C["green"], fg=C["bg"])
                self.status.set("● PROVED")

            elif lbl == "FAILED":
                pt.insert("end", f"\n{'─'*60}\n", "dim")
                pt.insert("end", "  ✘  GOAL NOT PROVED\n", "fail")
                self.result_lbl.config(
                    text="  ✘  NOT PROVED  ✘",
                    bg=C["accent"], fg=C["white"])
                self.status.set("● FAILED")

        pt.config(state="disabled"); pt.see("end")

    # ── add clause dialog ──────────────────────────────────────
    def _add_clause(self):
        d = tk.Toplevel(self.root)
        d.title("Add Clause"); d.geometry("500x190")
        d.configure(bg=C["bg"]); d.resizable(False, False); d.grab_set()
        x = self.root.winfo_x() + (self.root.winfo_width()  - 500) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - 190) // 2
        d.geometry(f"500x190+{x}+{y}")

        tk.Label(d, text="Add CNF Clause",
                 font=("Consolas", 13, "bold"),
                 bg=C["bg"], fg=C["salmon"]).pack(pady=(14, 2))
        tk.Label(d, text="Use  ∨  between literals  and  ¬  for negation",
                 font=("Consolas", 9), bg=C["bg"], fg=C["muted"]).pack()

        v = tk.StringVar()
        e = tk.Entry(d, textvariable=v, font=("Courier New", 12),
                     bg=C["input"], fg=C["salmon"],
                     insertbackground=C["salmon"],
                     relief="flat", bd=8, width=44)
        e.pack(pady=10); e.focus_set()

        def submit():
            val = v.get().strip()
            if val:
                self.clauses.append(val)
                self._refresh_clauses()
            d.destroy()

        self._btn(d, "ADD", submit, C["salmon"]).pack()
        d.bind("<Return>", lambda _: submit())

    def _clear(self):
        if messagebox.askyesno("Clear", "Remove all clauses?"):
            self.clauses = []; self._refresh_clauses()

    def _reset(self): self._on_preset()

    def _export(self):
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        fn = f"proof_{ts}.txt"
        try:
            content = self.proof_box.get("1.0", "end")
            with open(fn, "w", encoding="utf-8") as f:
                f.write(f"Resolution AI — Proof Log\nCreated by Anmol Rai\n"
                        f"{datetime.now()}\n\n{content}")
            messagebox.showinfo("Saved", f"Saved as:\n{fn}")
        except Exception as ex:
            messagebox.showerror("Error", str(ex))


# ── ENTRY ──────────────────────────────────────────────────────
if __name__ == "__main__":
    App()
