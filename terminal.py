"""
Resolution in Artificial Intelligence - CO3
Terminal Interface | Created by Anmol Rai
Run: python terminal.py
"""

import sys, re, time
from datetime import datetime

# ── ANSI COLOURS ───────────────────────────────────────────────
R    = "\033[0m";  BOLD = "\033[1m"
RED  = "\033[38;2;205;28;24m";   ROSE = "\033[38;2;255;168;150m"
DARK = "\033[38;2;155;19;19m";   IVORY= "\033[38;2;255;232;228m"
MUTED= "\033[38;2;200;144;144m"; GRN  = "\033[38;2;126;216;140m"
ORN  = "\033[38;2;255;170;90m";  DIM  = "\033[38;2;122;64;64m"

def cl(col, txt): return f"{col}{txt}{R}"
def b(txt):       return f"{BOLD}{txt}{R}"
def div(ch="─"):  print(cl(DARK, "  " + ch * 60))

# ── NORMALISE CLAUSE ───────────────────────────────────────────
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

# ── HELPERS ────────────────────────────────────────────────────
def ask(prompt):
    try:
        return input(f"\n  {cl(ROSE, '❯')} {cl(IVORY, prompt)}: ").strip()
    except (EOFError, KeyboardInterrupt):
        print(); sys.exit(0)

def section(title):
    print()
    print(cl(RED, "  ◈ ") + cl(IVORY, b(title)))
    div()

def spin():
    frames = ["⣾","⣽","⣻","⢿","⡿","⣟","⣯","⣷"]
    for i in range(20):
        print(f"\r  {cl(RED, frames[i%8])}  {cl(MUTED, 'Running resolution...')}", end="", flush=True)
        time.sleep(0.06)
    print("\r" + " "*50 + "\r", end="")

# ── OUTPUT ─────────────────────────────────────────────────────
def print_banner():
    print()
    print(cl(RED,  "  ██████╗ ███████╗███████╗ ██████╗ ██╗     ██╗   ██╗████████╗██╗ ██████╗ ███╗  ██╗"))
    print(cl(RED,  "  ██╔══██╗██╔════╝██╔════╝██╔═══██╗██║     ██║   ██║╚══██╔══╝██║██╔═══██╗████╗ ██║"))
    print(cl(DARK, "  ██████╔╝█████╗  ███████╗██║   ██║██║     ██║   ██║   ██║   ██║██║   ██║██╔██╗██║"))
    print(cl(DARK, "  ██╔══██╗██╔══╝  ╚════██║██║   ██║██║     ██║   ██║   ██║   ██║██║   ██║██║╚████║"))
    print(cl(ROSE, "  ██║  ██║███████╗███████║╚██████╔╝███████╗╚██████╔╝   ██║   ██║╚██████╔╝██║ ╚███║"))
    print(cl(ROSE, "  ╚═╝  ╚═╝╚══════╝╚══════╝ ╚═════╝ ╚══════╝╚═════╝    ╚═╝   ╚═╝ ╚═════╝╚═╝  ╚══╝"))
    print()
    print(cl(RED,  "  ╔══════════════════════════════════════════════════════╗"))
    print(cl(RED,  "  ║") + cl(IVORY, "  RESOLUTION IN AI — CO3                           ") + cl(RED, "║"))
    print(cl(RED,  "  ║") + cl(MUTED, "  FOL · CNF · Proof by Contradiction               ") + cl(RED, "║"))
    print(cl(RED,  "  ║") + cl(ROSE,  "  ✦ Created by Anmol Rai                           ") + cl(RED, "║"))
    print(cl(RED,  "  ╚══════════════════════════════════════════════════════╝"))
    print()
    print(cl(MUTED, f"  {datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}"))

def print_menu():
    print()
    print(cl(RED, "  ┌───────────────────────────────────────┐"))
    print(cl(RED, "  │") + cl(IVORY, b("  MENU                                 ")) + cl(RED, "│"))
    print(cl(RED, "  ├───────────────────────────────────────┤"))
    for k, v in PRESETS.items():
        print(cl(RED, "  │") + f"  {cl(ROSE, b(k))}  {cl(IVORY, v['name']):<34}" + cl(RED, "│"))
    print(cl(RED, "  ├───────────────────────────────────────┤"))
    for k, v in [("4", "Enter custom problem"), ("5", "View theory"), ("q", "Quit")]:
        print(cl(RED, "  │") + f"  {cl(ROSE, b(k))}  {cl(IVORY, v):<34}" + cl(RED, "│"))
    print(cl(RED, "  └───────────────────────────────────────┘"))

def print_proof(proved, steps):
    section("PROOF STEPS")
    sn = 0
    for lbl, c1, c2, res, init_list in steps:
        if lbl == "INIT":
            print(cl(ORN, "  ◆ ") + cl(IVORY, b("INITIAL STATE")))
            for i, line in enumerate(init_list):
                print(f"  {cl(DIM, '['+str(i+1)+']')}  {cl(MUTED, line)}")
            print()
        elif lbl in ("STEP", "EMPTY"):
            sn += 1
            if lbl == "EMPTY":
                print(cl(RED, b(f"  ─ Step {sn}:  EMPTY CLAUSE")))
            else:
                print(cl(DIM, f"  ─ Step {sn}:"))
            print(f"    {cl(DIM,'P:')} {cl(IVORY, c1)}")
            print(f"    {cl(DIM,'Q:')} {cl(IVORY, c2)}")
            if lbl == "EMPTY":
                print(f"    {cl(ROSE,'⇒')} {cl(ORN, b('⊥  (Empty Clause — Contradiction!'))} ")
            else:
                print(f"    {cl(ROSE,'⇒')} {cl(ROSE, res)}")
            print()
        elif lbl == "PROVED":
            div("═")
            print(cl(GRN, b("  ✔  GOAL PROVED")) + cl(IVORY, " — Contradiction derived."))
            div("═")
        elif lbl == "FAILED":
            div("═")
            print(cl(RED, b("  ✘  GOAL NOT PROVED")) + cl(MUTED, " — No new clauses."))
            div("═")

def run_preset(key):
    p = PRESETS[key]
    print(); div("═")
    print(f"  {cl(ROSE, b(p['name']))}")
    print(f"  {cl(MUTED, p['desc'])}")
    div("═")

    section("FIRST-ORDER LOGIC")
    for i, f in enumerate(p["fol"]):
        print(f"  {cl(DIM, str(i+1)+'.')} {cl(ROSE, f)}")

    section("CNF CLAUSES")
    for i, c in enumerate(p["clauses"]):
        print(f"  {cl(DARK,'['+str(i+1)+']')}  {cl(IVORY, c)}")
    print(f"  {cl(DARK,'[¬G]')}  {cl(RED, p['neg_goal'])}  {cl(DIM,'← Negated Goal')}")

    print(f"\n  {cl(MUTED,'Goal to prove:')} {cl(ROSE, b(p['goal']))}")

    if ask("Press ENTER to run  (or 's' to skip)").lower() == "s":
        return

    spin()
    proved, steps = ResolutionEngine().prove(p["clauses"], p["neg_goal"])
    print_proof(proved, steps)

    if ask("Save proof to file? (y/n)").lower() == "y":
        save_log(p["name"], p["clauses"], p["neg_goal"], proved, steps)

def run_custom():
    print(); div("═")
    print(f"  {cl(ROSE, b('CUSTOM PROBLEM'))}")
    div("═")
    print(cl(MUTED, f"  Use {cl(ROSE,'∨')} between literals and {cl(ROSE,'¬')} for negation."))
    print(cl(MUTED, f"  Example: {cl(ROSE,'¬Human(Socrates) ∨ Mortal(Socrates)')}"))
    print(cl(MUTED,  "  Type 'done' when finished.\n"))

    clauses, i = [], 1
    while True:
        val = ask(f"Clause [{i}]  (or 'done')")
        if val.lower() == "done":
            break
        if val:
            clauses.append(val); i += 1

    if not clauses:
        print(f"\n  {cl(RED,'✘')} No clauses entered."); return

    ng = ask("Negated goal  e.g. ¬Mortal(Socrates)")
    if not ng:
        print(f"\n  {cl(RED,'✘')} No goal entered."); return

    section("YOUR CLAUSES")
    for idx, c in enumerate(clauses):
        print(f"  {cl(DARK,f'[{idx+1}]')}  {cl(IVORY, c)}")
    print(f"  {cl(DARK,'[¬G]')}  {cl(RED, ng)}")

    if ask("Run proof? (y/n)").lower() != "y":
        return

    spin()
    proved, steps = ResolutionEngine().prove(clauses, ng)
    print_proof(proved, steps)

    if ask("Save proof to file? (y/n)").lower() == "y":
        save_log("Custom", clauses, ng, proved, steps)

def save_log(name, clauses, ng, proved, steps):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    fn = f"proof_{name.lower().replace(' ','_')}_{ts}.txt"
    with open(fn, "w", encoding="utf-8") as f:
        f.write(f"Resolution AI — {name}\nCreated by Anmol Rai\n{datetime.now()}\n\n")
        f.write("CLAUSES:\n")
        for i, c in enumerate(clauses): f.write(f"  [{i+1}] {c}\n")
        f.write(f"  [¬G] {ng}\n\nSTEPS:\n")
        sn = 0
        for lbl, c1, c2, res, init in steps:
            if lbl == "INIT":
                for l in init: f.write(f"  {l}\n")
                f.write("\n")
            elif lbl in ("STEP", "EMPTY"):
                sn += 1
                f.write(f"  Step {sn}: {c1}  +  {c2}  =>  {res}\n")
            elif lbl == "PROVED": f.write("\n✔ GOAL PROVED\n")
            elif lbl == "FAILED": f.write("\n✘ NOT PROVED\n")
    print(f"\n  {cl(GRN,'✔')} Saved: {cl(ROSE, fn)}")

def show_theory():
    section("RESOLUTION THEORY")
    rows = [
        (ROSE,  "DEFINITION"),
        (MUTED, "  Proof by Contradiction: negate goal, add to KB, derive ⊥."),
        ("", ""),
        (ROSE,  "RESOLUTION RULE"),
        (IVORY, "  (A ∨ B)  +  (¬B ∨ C)  →  (A ∨ C)"),
        ("", ""),
        (ROSE,  "ALGORITHM"),
        (MUTED, "  1. Convert to FOL"),
        (MUTED, "  2. Negate the goal"),
        (MUTED, "  3. Convert to CNF"),
        (MUTED, "  4. Standardize variables"),
        (MUTED, "  5. Unification"),
        (MUTED, "  6. Apply resolution repeatedly"),
        (MUTED, "  7. ⊥ → PROVED  |  no new clauses → NOT PROVED"),
    ]
    for col, txt in rows:
        if not col: print()
        else: print(f"  {cl(col, txt)}")

# ── MAIN ───────────────────────────────────────────────────────
if __name__ == "__main__":
    print_banner()
    while True:
        print_menu()
        ch = ask("Choose option")
        if   ch in PRESETS:     run_preset(ch)
        elif ch == "4":         run_custom()
        elif ch == "5":         show_theory()
        elif ch.lower() == "q":
            print(f"\n  {cl(ROSE,'Goodbye — Anmol Rai')}\n")
            sys.exit(0)
        else:
            print(f"\n  {cl(RED,'✘')} Invalid. Try 1–5 or q.")
