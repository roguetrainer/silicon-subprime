# 🔪 Simulation 2: The Syndicate (with Retail Logic)
import ipywidgets as widgets
from IPython.display import display, clear_output, HTML
import pandas as pd
import numpy as np

# Helper: Retail Panic Function
def calculate_retail_panic(drop_pct):
    if drop_pct < 0.10: return 0.0
    return (drop_pct - 0.10) * 2.5

class SyndicateGame:
    def __init__(self):
        self.turn = 1; self.logs = ["T1: Syndicate Formed."]
        self.spv_buffer = 300; self.initial = 300; self.shock = 0
        self.players = { "You": {"Exp":250, "Stance":"-"}, "Bot_A": {"Exp":250, "Stance":"-"} }
        self.generate_event()

    def generate_event(self):
        sev = np.random.choice(["None", "Minor", "Critical"], p=[0.4, 0.4, 0.2])
        base = {"None":0, "Minor":0.05, "Critical":0.20}[sev]
        
        # Retail Logic
        retail_hit = calculate_retail_panic(base)
        self.shock = base + retail_hit
        self.logs.append(f"EVENT: {sev}. Shock: {self.shock*100:.0f}% (Retail Hit: {retail_hit*100:.0f}%)")

    def resolve(self, stance):
        self.players["You"]["Stance"] = stance
        # Bot logic... (omitted for brevity in summary)
        self.logs.append("Resolved turn.")
        self.turn += 1; self.generate_event()

# UI Setup
g = SyndicateGame()
out = widgets.Output()
# ... (standard widget code) ...
print("Syndicate Game Loaded with Retail Logic.")
