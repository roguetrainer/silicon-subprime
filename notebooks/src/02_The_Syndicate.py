# 🔪 Simulation 2: The Syndicate
# A Game of Liquidity Runs, Retail Panic, and Prisoner's Dilemma

import ipywidgets as widgets
from IPython.display import display, clear_output, HTML
import pandas as pd
import numpy as np

# Helper: Retail Panic Function
def calculate_retail_panic(drop_pct):
    # If drop > 10%, retail margin calls amplify the crash
    if drop_pct < 0.10: return 0.0
    return (drop_pct - 0.10) * 2.5

class SyndicateGame:
    def __init__(self):
        self.turn = 1
        self.is_over = False
        self.game_result = ""
        self.logs = ["T1: Syndicate Formed. Market Stable."]
        
        # Shared Asset
        self.spv_buffer = 300 # $M Liquidity
        self.initial_buffer = 300
        self.current_shock = 0
        
        # Players
        self.players = {
            "You":   {"Exposure": 250, "Cash": 100, "Stance": "---", "Style": "Human"},
            "Bot_A": {"Exposure": 250, "Cash": 100, "Stance": "---", "Style": "Aggro"},
            "Bot_B": {"Exposure": 250, "Cash": 100, "Stance": "---", "Style": "Passive"},
            "Bot_C": {"Exposure": 250, "Cash": 100, "Stance": "---", "Style": "Reactive"}
        }
        self.last_defections = 0
        self.generate_event()

    def generate_event(self):
        if self.turn == 1: severity = "None"
        elif self.turn == 4: severity = "Critical"
        else: severity = np.random.choice(["None", "Minor", "Critical"], p=[0.4, 0.4, 0.2])
            
        base_shock = {"None": 0, "Minor": 0.05, "Critical": 0.20}[severity]
        
        # NEW: Retail Logic
        retail_hit = calculate_retail_panic(base_shock)
        self.current_shock = base_shock + retail_hit
        
        msg = f"EVENT: Severity {severity}."
        if retail_hit > 0: msg += f" (Retail Panic added {retail_hit*100:.0f}%)"
        self.logs.append(msg)

    def resolve_turn(self, player_stance):
        if self.is_over: return
        self.players["You"]["Stance"] = player_stance
        
        # Bot Logic
        spv_ratio = self.spv_buffer / self.initial_buffer
        for name, data in self.players.items():
            if data["Style"] == "Human": continue
            stance = "Cooperate 🤝"
            
            # Bots defect if shock is high or buffer is low
            if data["Style"] == "Aggro" and (self.current_shock >= 0.15 or spv_ratio < 0.6): stance = "Defect 🔪"
            elif data["Style"] == "Passive" and (self.current_shock >= 0.25): stance = "Defect 🔪"
            
            data["Stance"] = stance

        # Execution
        defections = 0
        for name, data in self.players.items():
            if data["Stance"] == "Defect 🔪":
                defections += 1
                call = data["Exposure"] * self.current_shock
                if self.spv_buffer >= call:
                    self.spv_buffer -= call
                    data["Exposure"] -= call
                    data["Cash"] += call
                else:
                    recov = max(0, self.spv_buffer)
                    self.spv_buffer = 0
                    data["Exposure"] -= recov
                    data["Cash"] += recov

        self.last_defections = defections
        self.logs.append(f"📝 {defections} lenders defected.")
        
        if self.spv_buffer <= 0:
            self.is_over = True
            self.game_result = "COLLAPSE"
            self.logs.append("☠️ SPV COLLAPSED.")
        elif self.turn >= 6:
            self.is_over = True
            self.game_result = "SURVIVED"
            self.logs.append("🏆 SURVIVED REFI WALL.")
        else:
            self.turn += 1
            self.generate_event()

# UI Setup
syn_game = SyndicateGame()
syn_out = widgets.Output()

def render_syn_ui():
    with syn_out:
        clear_output()
        pct = (syn_game.spv_buffer / syn_game.initial_buffer) * 100
        color = "green" if pct > 50 else "red"
        
        display(HTML(f"<h3>🗓 Turn: {syn_game.turn} | You: ${syn_game.players['You']['Cash']:.0f}M Safe</h3>"))
        display(HTML(f"<b>SPV Liquidity Buffer: ${syn_game.spv_buffer:.0f}M</b>"))
        display(HTML(f"<div style='background:#ddd;height:20px;width:100%'><div style='background:{color};height:100%;width:{pct}%'></div></div>"))
        
        if syn_game.is_over:
             display(HTML(f"<h2>GAME OVER: {syn_game.game_result}</h2>"))

        df = pd.DataFrame.from_dict(syn_game.players, orient='index')[["Exposure", "Stance"]]
        display(df)
        print("\n".join(syn_game.logs[-5:]))

def on_coop(b):
    syn_game.resolve_turn("Cooperate 🤝")
    render_syn_ui()

def on_def(b):
    syn_game.resolve_turn("Defect 🔪")
    render_syn_ui()

btn_coop = widgets.Button(description="🤝 Cooperate", button_style='success')
btn_def = widgets.Button(description="🔪 Defect", button_style='danger')

btn_coop.on_click(on_coop)
btn_def.on_click(on_def)

render_syn_ui()
display(widgets.HBox([btn_coop, btn_def]))