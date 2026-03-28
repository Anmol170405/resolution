# Resolution AI

**Live Demo → [resolutionai.netlify.app](https://resolutionai.netlify.app)**

An interactive automated theorem prover built for the using Artificial Intelligence. Runs entirely in the browser, no installation, no server, no dependencies.

---

## What it does

Resolution AI proves logical statements automatically using the **Resolution inference technique** from AI. You provide a set of facts and a goal — the system negates the goal, converts everything to Conjunctive Normal Form, and applies the resolution rule repeatedly until it either finds a contradiction (goal proved) or exhausts all possibilities (goal not provable).

The entire proof is shown step by step so you can follow exactly how the machine reasoned from facts to conclusion.

---
---

## Features

- **4 preset problems** — West is a Criminal, Socrates is Mortal, John Likes All Food, Anmol is a Coder
- **Custom problem mode** — enter your own CNF clauses one by one and define your own goal
- **Symbol buttons** — insert ∨ ¬ ∀ ∃ ∧ → without copy-pasting
- **Step-by-step proof output** — every resolution step shown with parent clauses and resolvent
- **Live result banner** — green on proved, red on not proved
- **Animated progress bar** while the engine runs
- **Two local interfaces** — `terminal.py` for coloured interactive terminal, `gui.py` for desktop Tkinter window

---

## Tech Stack

| | |
|---|---|
| Browser app | Vanilla HTML, CSS, JavaScript — zero frameworks, zero dependencies |
| Resolution engine | Pure JavaScript — runs entirely client-side |
| Desktop terminal | Python 3 with ANSI 24-bit colour output |
| Desktop GUI | Python 3 + Tkinter |
| Hosting | Netlify (free tier, auto-deploy from GitHub) |

---

## How the algorithm works

Resolution is a proof by contradiction technique from First-Order Logic.

```
1. Convert all knowledge base statements to FOL
2. Negate the goal  →  add ¬GOAL to the knowledge base
3. Convert everything to CNF (Conjunctive Normal Form)
4. Standardize variables to avoid naming conflicts
5. Apply the Resolution Rule repeatedly:
       (A ∨ B)  +  (¬B ∨ C)  →  (A ∨ C)
6. If ⊥ (empty clause) is derived  →  GOAL IS PROVED ✔
   If no new clauses can be derived  →  goal is not provable ✘
```

CNF conversion steps: eliminate biconditionals, eliminate implications (A→B becomes ¬A∨B), move ¬ inward using De Morgan's laws, Skolemize existential quantifiers, drop universal quantifiers, distribute ∧ over ∨.

---

## Example — West is a Criminal

```
Knowledge Base:
  Americans who sell weapons to hostile nations are criminals
  Nano is a hostile nation
  West is an American
  M1 is a missile
  All missiles are weapons
  West sells M1 to Nano

Goal: Prove Criminal(West)

Step 1:  ¬Missile(M1) ∨ Weapon(M1)  +  Missile(M1)
      ⇒  Weapon(M1)

Step 2:  ¬American(West) ∨ ... ∨ Criminal(West)  +  American(West)
      ⇒  ¬Weapon(M1) ∨ ¬Sells(West,M1,Nano) ∨ ¬Hostile(Nano) ∨ Criminal(West)

  ... further steps ...

Final:  ⊥  (empty clause — contradiction found)

✔  GOAL PROVED — West is a Criminal
```

---

## Why it matters

Resolution is the foundation of:

- **Prolog** — the entire logic programming language runs on resolution
- **Expert systems** — automated knowledge base reasoning
- **Formal verification** — tools like Isabelle and ACL2 use resolution-based provers
- **AI planning** — STRIPS and PDDL planners use resolution for inference
- **Natural language processing** — semantic reasoning and question answering

This experiment shows how a machine can derive conclusions from facts with zero human involvement — the core idea behind intelligent reasoning systems.

---

## Run locally

```bash
git clone https://github.com/Anmol170405/resolution.git
cd resolution

# terminal interface
python terminal.py

# desktop GUI
python gui.py
```

Requires Python 3.8+. Tkinter is bundled with Python on Windows and Mac.
Linux: `sudo apt install python3-tk`

---

## Project structure

```
resolution/
├── index.html      browser app — full theorem prover in JS
├── terminal.py     interactive terminal with ANSI colour output
├── gui.py          desktop GUI with crimson theme
└── README.md       this file
```

---

Created by **Anmol Rai** · Artificial Intelligence
