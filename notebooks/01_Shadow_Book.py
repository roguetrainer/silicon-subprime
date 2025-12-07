# 🕸️ Simulation 1: The Shadow Book
# A Game of Network Contagion and Information Asymmetry

import ipywidgets as widgets
from IPython.display import display, clear_output, HTML
import pandas as pd
import numpy as np

# --- GAME ENGINE ---
class ShadowNetworkGame:
    def __init__(self):
        self.turn = 1
        self.player_capital = 500
        self.is_alive = True
        self.logs = []
        
        # Players & Assets
        self.lenders = ["Player_Fund", "Blackstone_Bot", "BlueOwl_Bot", "Apollo_Bot"]
        self.spvs = ["SPV_Core", "SPV_Lambda", "SPV_Crusoe"]
        
        # Exposure Matrix (Hidden State)
        # Rows = Lenders, Cols = Borrowers
        data = [
            [300, 100, 50],   # You
            [500, 50,  50],   # Blackstone (The Whale)
            [100, 400, 0],    # BlueOwl
            [50,  0,   400]   # Apollo
        ]
        self.matrix = pd.DataFrame(data, index=self.lenders, columns=self.spvs)
        self.spv_funding_health = {spv: 1.0 for spv in self.spvs} # 1.0 = 100% Funded

    def next_turn(self, action, target_spv=None):
        if not self.is_alive: return
        self.logs = []
        
        # 1. Player Action
        if action == "Hoard (Recall)":
            exposure = self.matrix.loc["Player_Fund", target_spv]
            if exposure > 0:
                pulled = 50
                self.matrix.loc["Player_Fund", target_spv] -= pulled
                self.player_capital += pulled
                self.log(f"🥶 YOU: Recalled ${pulled}M from {target_spv}. (Triggered Contagion)")
                
                # Apply Damage (Self-inflicted contagion)
                current_total = self.matrix[target_spv].sum() + 50
                damage_pct = pulled / current_total
                self.spv_funding_health[target_spv] -= damage_pct

        elif action == "Investigate":
            self.player_capital -= 10
            bot = "Blackstone_Bot" 
            pos = self.matrix.loc[bot, target_spv]
            self.log(f"🕵️ INTEL: {bot} has ${pos}M in {target_spv}.")

        # 2. Events (The Blackwell Shock)
        if self.turn == 3:
            shock_target = "SPV_Core"
            self.log(f"🚨 EVENT: Blackwell Release! {shock_target} devalued.")
            
            # Simulated Contagion: BlueOwl gets scared of Core, pulls from Lambda
            self.spv_funding_health["SPV_Core"] -= 0.30
            self.spv_funding_health["SPV_Lambda"] -= 0.15 
            self.log("📉 CONTAGION: BlueOwl_Bot panicked and pulled funds from SPV_Lambda.")

        # 3. Check Survival
        for spv in self.spvs:
            if self.spv_funding_health[spv] < 0.70:
                loss = self.matrix.loc["Player_Fund", spv]
                if loss > 0:
                    self.player_capital -= loss
                    self.matrix.loc["Player_Fund", spv] = 0
                    self.log(f"☠️ DEFAULT: {spv} Collapsed! You lost ${loss}M.")
        
        if self.player_capital <= 0:
            self.is_alive = False
            self.log("GAME OVER: Fund Insolvent.")
            
        self.turn += 1

    def log(self, msg):
        self.logs.append(f"Month {self.turn}: {msg}")

# --- UI LOGIC ---
game = ShadowNetworkGame()
out = widgets.Output()

def render_ui():
    with out:
        clear_output()
        if not game.is_alive:
            print("💀 GAME OVER: INSOLVENCY")
            for l in game.logs: print(l)
            return

        # Dashboard
        display(HTML(f"<h3>🗓 Month: {game.turn} | 💰 Capital: ${game.player_capital}M</h3>"))
        
        # Portfolio View
        my_pos = game.matrix.loc["Player_Fund"]
        health_data = pd.DataFrame({
            "My Exposure": my_pos,
            "Funding Health": [f"{game.spv_funding_health[spv]*100:.0f}%" for spv in game.spvs]
        })
        
        # Color coding function
        def color_health(val):
            val = int(val.replace("%",""))
            if val < 80: return 'color: red; font-weight: bold'
            return 'color: green'

        display(health_data.style.applymap(color_health, subset=["Funding Health"]))
        
        print("\n--- ACTIVITY LOG ---")
        for l in game.logs[-5:]: print(l)

# Handlers
def on_hoard(b):
    game.next_turn("Hoard (Recall)", dropdown.value)
    render_ui()

def on_scan(b):
    game.next_turn("Investigate", dropdown.value)
    render_ui()

def on_wait(b):
    game.next_turn("Wait")
    render_ui()

# Widgets
dropdown = widgets.Dropdown(options=["SPV_Core", "SPV_Lambda", "SPV_Crusoe"], description="Target:")
btn_hoard = widgets.Button(description="🥶 Hoard Loan", button_style='danger')
btn_scan = widgets.Button(description="🕵️ Investigate", button_style='info')
btn_wait = widgets.Button(description="⏩ Wait")

btn_hoard.on_click(on_hoard)
btn_scan.on_click(on_scan)
btn_wait.on_click(on_wait)

render_ui()
display(widgets.HBox([dropdown]))
display(widgets.HBox([btn_hoard, btn_scan, btn_wait]))