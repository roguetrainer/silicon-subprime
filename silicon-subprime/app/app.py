import gradio as gr
import pandas as pd
import numpy as np

# --- HELPER: Retail Logic ---
def calculate_retail_panic(drop_pct):
    # If drop > 10%, retail margin calls amplify the crash
    if drop_pct < 0.10: return 0.0
    return (drop_pct - 0.10) * 2.5

# ==========================================
# GAME 1: SHADOW BOOK
# ==========================================
class ShadowNetworkGame:
    def __init__(self): self.reset()
    def reset(self):
        self.turn = 1
        self.player_capital = 500
        self.is_alive = True
        self.logs = ["T1: Operations Started."]
        self.lenders = ["Player_Fund", "Blackstone_Bot", "BlueOwl_Bot", "Apollo_Bot"]
        self.spvs = ["SPV_Core", "SPV_Lambda", "SPV_Crusoe"]
        data = [[300, 100, 50], [500, 50, 50], [100, 400, 0], [50, 0, 400]]
        self.matrix = pd.DataFrame(data, index=self.lenders, columns=self.spvs)
        self.spv_funding_health = {spv: 1.0 for spv in self.spvs} 

    def get_status_md(self):
        if not self.is_alive: return f"## 💀 INSOLVENT (Turn {self.turn})"
        return f"### 🗓 Turn: {self.turn}\n### 💰 Capital: ${self.player_capital}M"

    def get_portfolio_df(self):
        df = pd.DataFrame({
            "Exposure": self.matrix.loc["Player_Fund"],
            "Health": [f"{self.spv_funding_health[s]*100:.0f}%" for s in self.spvs]
        })
        return df

    def next_turn(self, action, target=None):
        if not self.is_alive: return self.logs_to_str()
        self.logs.append(f"--- Turn {self.turn} ---")
        
        if action == "Hoard":
            amt = 50
            if self.matrix.loc["Player_Fund", target] > 0:
                self.matrix.loc["Player_Fund", target] -= amt
                self.player_capital += amt
                self.spv_funding_health[target] -= (amt/(self.matrix[target].sum()+amt))
                self.logs.append(f"🥶 Recalled ${amt}M from {target}.")
        elif action == "Scan":
            self.player_capital -= 10
            pos = self.matrix.loc["Blackstone_Bot", target]
            self.logs.append(f"🕵️ INTEL: Blackstone has ${pos}M in {target}.")
            
        if self.turn == 3:
            self.logs.append("🚨 EVENT: Blackwell Release!")
            self.spv_funding_health["SPV_Core"] -= 0.30
            self.spv_funding_health["SPV_Lambda"] -= 0.15
            self.logs.append("📉 CONTAGION: BlueOwl panicked and pulled from Lambda.")
            
        # Check Default
        for spv in self.spvs:
            if self.spv_funding_health[spv] < 0.70:
                loss = self.matrix.loc["Player_Fund", spv]
                if loss > 0:
                    self.player_capital -= loss
                    self.matrix.loc["Player_Fund", spv] = 0
                    self.logs.append(f"☠️ {spv} DEFAULTED! Lost ${loss}M.")
        
        if self.player_capital <= 0: self.is_alive = False; self.logs.append("GAME OVER.")
        self.turn += 1
        return self.logs_to_str()

    def logs_to_str(self): return "\n".join(self.logs[::-1])

# ==========================================
# GAME 2: THE SYNDICATE (Updated with Retail)
# ==========================================
class SyndicateGame:
    def __init__(self): self.reset()
    def reset(self):
        self.turn = 1
        self.is_over = False
        self.game_result = ""
        self.logs = ["T1: Syndicate Formed."]
        self.spv_buffer = 300
        self.initial_buffer = 300
        self.current_shock = 0
        self.players = {
            "You":   {"Exp": 250, "Cash": 100, "Stance": "-", "Style": "Human"},
            "Bot_A": {"Exp": 250, "Cash": 100, "Stance": "-", "Style": "Aggro"},
            "Bot_B": {"Exp": 250, "Cash": 100, "Stance": "-", "Style": "Passive"},
            "Bot_C": {"Exp": 250, "Cash": 100, "Stance": "-", "Style": "Reactive"}
        }
        self.generate_event()

    def generate_event(self):
        sev = "None"
        if self.turn == 4: sev = "Critical"
        elif self.turn > 1: sev = np.random.choice(["None", "Minor", "Major", "Critical"], p=[0.3, 0.4, 0.2, 0.1])
        
        base_shock = {"None": 0, "Minor": 0.05, "Major": 0.15, "Critical": 0.30}[sev]
        self.logs.append(f"EVENT: Severity {sev} (Base Shock: {base_shock*100:.0f}%)")
        
        # --- NEW: RETAIL FEEDBACK LOOP ---
        retail_damage = calculate_retail_panic(base_shock)
        if retail_damage > 0:
            self.logs.append(f"📉 MARGIN CALL: Retail Panic! Extra {retail_damage*100:.0f}% drop.")
            
        self.current_shock = base_shock + retail_damage

    def resolve_turn(self, stance):
        if self.is_over: return
        self.players["You"]["Stance"] = stance
        
        # Bot Logic (Twitchier due to retail risk)
        ratio = self.spv_buffer / self.initial_buffer
        for n, d in self.players.items():
            if d["Style"] != "Human":
                bot_choice = "Cooperate"
                # If retail panic is active (shock > 15%), Bots flee faster
                if d["Style"] == "Aggro" and (self.current_shock > 0.10 or ratio < 0.6): bot_choice = "Defect"
                elif d["Style"] == "Passive" and (self.current_shock > 0.25): bot_choice = "Defect"
                d["Stance"] = bot_choice
                
        defects = 0
        for n, d in self.players.items():
            if d["Stance"] == "Defect":
                defects += 1
                call = d["Exp"] * self.current_shock
                recov = min(call, self.spv_buffer)
                self.spv_buffer -= recov
                d["Exp"] -= recov
                d["Cash"] += recov
                
        self.logs.append(f"📝 {defects} lenders defected.")
        if self.spv_buffer <= 0: self.is_over=True; self.game_result="COLLAPSE"; self.logs.append("☠️ SPV COLLAPSED.")
        elif self.turn >= 6: self.is_over=True; self.game_result="SURVIVED"; self.logs.append("🏆 SURVIVED.")
        else: self.turn += 1; self.generate_event()

    def get_ui(self):
        pct = (self.spv_buffer/self.initial_buffer)*100
        html = f"<div style='background:#ddd;height:15px'><div style='background:{'green' if pct>50 else 'red'};height:100%;width:{pct}%'></div></div>"
        df = pd.DataFrame.from_dict(self.players, orient='index')[["Exp", "Stance"]]
        return html, df, "\n".join(self.logs[::-1])

# ==========================================
# GAME 3: TRANCHE DEFENSE
# ==========================================
class TrancheGame:
    def __init__(self): self.reset()
    def reset(self):
        self.turn=1; self.is_over=False; self.logs=["Q1: Started."]
        self.sen=500; self.mezz=200; self.eq=100; self.cash=50; self.rev=80
        self.snap=None
    
    def next_turn(self, act):
        if self.is_over: return
        if act=="DeLev" and self.cash>=50: self.mezz-=50; self.cash-=50; self.logs.append("🔧 De-Levered.")
        elif act=="Div" and self.cash>=20: self.cash-=20; self.eq-=10; self.logs.append("💸 Dividend.")
        
        inc = max(0, (self.rev*(0.95**self.turn)) + (-30 if self.turn==5 else np.random.normal(0,5)))
        curr = inc
        s = {"Inc": inc, "Sen": False, "Mezz": False, "Eq": 0}
        
        # Waterfall
        if curr >= 20: curr -= 20 # Opex
        else: self.fail("Opex Fail"); return
        
        i_sen = self.sen*0.05/4
        if curr >= i_sen: curr-=i_sen; s["Sen"]=True
        elif self.cash >= (i_sen-curr): self.cash-=(i_sen-curr); curr=0; s["Sen"]=True
        else: self.fail("Senior Default"); return
        
        i_mezz = self.mezz*0.12/4
        if curr >= i_mezz: curr-=i_mezz; s["Mezz"]=True
        elif self.cash >= (i_mezz-curr): self.cash-=(i_mezz-curr); curr=0; s["Mezz"]=True
        else: self.fail("Mezz Default"); return
        
        s["Eq"] = curr; self.cash+=curr; self.snap=s
        self.logs.append(f"🌊 Rev: ${inc:.1f}M. Equity: +${curr:.1f}M")
        
        if self.turn >= 8: self.is_over=True; self.logs.append("🏆 IPO!")
        else: self.turn += 1

    def fail(self, r): self.is_over=True; self.logs.append(f"☠️ {r}")
    
    def get_ui(self):
        h = "<div>No Data</div>"
        if self.snap:
            s=self.snap
            h=f"<div>1. Sen: {s['Sen']} | 2. Mezz: {s['Mezz']} | ⬇ Eq: ${s['Eq']:.1f}M</div>"
        return f"Reserves: ${self.cash:.1f}M", h, "\n".join(self.logs[::-1])

# ==========================================
# GRADIO INTERFACE
# ==========================================
with gr.Blocks(theme=gr.themes.Monochrome()) as demo:
    gr.Markdown("# 📉 Silicon Subprime")
    
    with gr.Tabs():
        # TAB 1
        with gr.TabItem("1. Shadow Book"):
            g1 = gr.State(ShadowNetworkGame())
            with gr.Row():
                with gr.Column():
                    g1_dd = gr.Dropdown(["SPV_Core", "SPV_Lambda", "SPV_Crusoe"], label="Target")
                    g1_b1 = gr.Button("Hoard", variant="stop")
                    g1_b2 = gr.Button("Scan")
                    g1_b3 = gr.Button("Wait")
                    g1_b4 = gr.Button("Reset")
                with gr.Column():
                    g1_st = gr.Markdown()
                    g1_df = gr.Dataframe()
                    g1_lg = gr.Textbox(lines=5)
            def u1(g): return [g, g.get_status_md(), g.get_portfolio_df(), g.logs_to_str()]
            g1_b1.click(lambda g,t: (g.next_turn("Hoard",t), *u1(g)[1:]), [g1, g1_dd], [g1, g1_st, g1_df, g1_lg])
            g1_b2.click(lambda g,t: (g.next_turn("Scan",t), *u1(g)[1:]), [g1, g1_dd], [g1, g1_st, g1_df, g1_lg])
            g1_b3.click(lambda g: (g.next_turn("Wait"), *u1(g)[1:]), [g1], [g1, g1_st, g1_df, g1_lg])
            g1_b4.click(lambda: u1(ShadowNetworkGame()), None, [g1, g1_st, g1_df, g1_lg])
            demo.load(lambda: u1(ShadowNetworkGame()), None, [g1, g1_st, g1_df, g1_lg])

        # TAB 2
        with gr.TabItem("2. The Syndicate (Retail Risk)"):
            g2 = gr.State(SyndicateGame())
            gr.Markdown("Includes **Retail Margin Logic**: Shocks >15% trigger automated liquidations.")
            g2_html = gr.HTML()
            with gr.Row():
                g2_b1 = gr.Button("Cooperate")
                g2_b2 = gr.Button("Defect", variant="stop")
                g2_b3 = gr.Button("Reset")
            g2_df = gr.Dataframe()
            g2_lg = gr.Textbox(lines=5)
            def u2(g): h,d,l=g.get_ui(); return [g,h,d,l]
            g2_b1.click(lambda g: (g.resolve_turn("Cooperate"), *u2(g)[1:]), [g2], [g2, g2_html, g2_df, g2_lg])
            g2_b2.click(lambda g: (g.resolve_turn("Defect"), *u2(g)[1:]), [g2], [g2, g2_html, g2_df, g2_lg])
            g2_b3.click(lambda: u2(SyndicateGame()), None, [g2, g2_html, g2_df, g2_lg])
            demo.load(lambda: u2(SyndicateGame()), None, [g2, g2_html, g2_df, g2_lg])

        # TAB 3
        with gr.TabItem("3. Tranche Defense"):
            g3 = gr.State(TrancheGame())
            with gr.Row():
                g3_b1 = gr.Button("Next Q")
                g3_b2 = gr.Button("DeLev")
                g3_b3 = gr.Button("Div")
                g3_b4 = gr.Button("Reset")
            g3_st = gr.Markdown()
            g3_html = gr.HTML()
            g3_lg = gr.Textbox(lines=5)
            def u3(g): s,h,l=g.get_ui(); return [g,s,h,l]
            g3_b1.click(lambda g: (g.next_turn("Next"), *u3(g)[1:]), [g3], [g3, g3_st, g3_html, g3_lg])
            g3_b2.click(lambda g: (g.next_turn("DeLev"), *u3(g)[1:]), [g3], [g3, g3_st, g3_html, g3_lg])
            g3_b3.click(lambda g: (g.next_turn("Div"), *u3(g)[1:]), [g3], [g3, g3_st, g3_html, g3_lg])
            g3_b4.click(lambda: u3(TrancheGame()), None, [g3, g3_st, g3_html, g3_lg])
            demo.load(lambda: u3(TrancheGame()), None, [g3, g3_st, g3_html, g3_lg])

if __name__ == "__main__":
    demo.launch()
