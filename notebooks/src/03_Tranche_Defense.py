# 🌊 Simulation 3: Tranche Defense
# A Game of Capital Waterfalls and Asset Depreciation

import ipywidgets as widgets
from IPython.display import display, clear_output, HTML
import numpy as np

class TrancheGame:
    def __init__(self):
        self.turn = 1
        self.is_over = False
        self.logs = ["Q1: Operations Started."]
        
        # Capital Stack
        self.debt_senior, self.debt_mezz, self.equity = 500, 200, 100
        self.cash, self.base_rev, self.opex = 50, 80, 20
        self.decay = 0.95
        self.snapshot = None

    def next_turn(self, action):
        if self.is_over: return
        
        # Action Processing
        if action == "De-Leverage" and self.cash >= 50:
            self.debt_mezz -= 50; self.cash -= 50
            self.logs.append("🔧 Paid down Mezz debt.")
        elif action == "Dividend" and self.cash >= 20:
            self.cash -= 20; self.equity -= 10
            self.logs.append("💸 Dividend extracted.")

        # Revenue
        rev = max(0, (self.base_rev * (self.decay ** self.turn)) + np.random.normal(0, 5))
        if self.turn == 5: rev -= 30 # DeepSeek Shock
        
        # Waterfall
        s = {"Inflow": rev, "Opex": False, "Senior": False, "Mezz": False, "Equity": 0}
        curr = rev
        
        # 1. Opex
        if curr >= self.opex: curr -= self.opex; s["Opex"] = True
        else: self.fail("Opex Unpaid")
        
        # 2. Senior Interest
        int_sen = self.debt_senior * 0.05 / 4
        if not self.is_over:
            if curr >= int_sen: curr -= int_sen; s["Senior"] = True
            elif self.cash >= (int_sen - curr): self.cash -= (int_sen - curr); s["Senior"] = True; curr = 0
            else: self.fail("Senior Default")

        # 3. Mezz Interest
        int_mezz = self.debt_mezz * 0.12 / 4
        if not self.is_over:
            if curr >= int_mezz: curr -= int_mezz; s["Mezz"] = True
            elif self.cash >= (int_mezz - curr): self.cash -= (int_mezz - curr); s["Mezz"] = True; curr = 0
            else: self.fail("Mezz Default")

        # 4. Equity
        if not self.is_over:
            s["Equity"] = curr; self.cash += curr
            self.snapshot = s
            self.logs.append(f"🌊 Rev: ${rev:.1f}M. Equity: +${curr:.1f}M")
            
        if self.turn >= 8 and not self.is_over: self.is_over = True; self.logs.append("🏆 IPO SUCCESS!")
        if not self.is_over: self.turn += 1

    def fail(self, reason):
        self.is_over = True; self.logs.append(f"☠️ {reason}")

# UI
td = TrancheGame()
out_td = widgets.Output()

def render_td():
    with out_td:
        clear_output()
        display(HTML(f"<h3>🗓 Quarter: {td.turn} | Reserves: ${td.cash:.1f}M</h3>"))
        
        if td.snapshot:
            s = td.snapshot
            def bar(label, paid): return f"<div style='border:1px solid #ccc; padding:2px; background:{'#cfc' if paid else '#fcc'}'>{label}</div>"
            display(HTML(bar("1. OPEX", s["Opex"])))
            display(HTML(bar("2. Senior Interest", s["Senior"])))
            display(HTML(bar("3. Mezz Interest", s["Mezz"])))
            display(HTML(f"<div style='color:green'><b>⬇ Equity Received: ${s['Equity']:.1f}M</b></div>"))
            
        print("\n".join(td.logs[-5:]))

def act(b):
    act_map = {"Next": "Wait", "DeLev": "De-Leverage", "Div": "Dividend"}
    td.next_turn(act_map.get(b.description[:5].strip(), "Wait"))
    render_td()

b1 = widgets.Button(description="Next Quarter"); b1.on_click(act)
b2 = widgets.Button(description="DeLev ($50M)"); b2.on_click(act)
b3 = widgets.Button(description="Div ($20M)"); b3.on_click(act)

render_td()
display(widgets.HBox([b1, b2, b3]))# Code for Game 3