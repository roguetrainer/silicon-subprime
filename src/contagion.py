import pandas as pd
import networkx as nx

def build_lending_network(exposure_data: pd.DataFrame) -> nx.Graph:
    G = nx.Graph()
    lenders = exposure_data.index.tolist()
    spvs = exposure_data.columns.tolist()
    G.add_nodes_from(lenders, type='Lender')
    G.add_nodes_from(spvs, type='SPV')
    for lender in lenders:
        for spv in spvs:
            amount = exposure_data.loc[lender, spv]
            if amount > 0:
                G.add_edge(lender, spv, weight=amount)
    return G

def run_liquidity_spiral(exposure_matrix, shock_target, write_down_pct=0.40, hoarding_multiplier=2.0):
    direct_losses = exposure_matrix[shock_target] * write_down_pct
    total_withdrawal_req = direct_losses * hoarding_multiplier
    healthy_spvs = [col for col in exposure_matrix.columns if col != shock_target]
    impact_report = []

    for spv in healthy_spvs:
        original_funding = exposure_matrix[spv].sum()
        withdrawn_amount = 0
        for lender, withdrawal_needed in total_withdrawal_req.items():
            lender_total_healthy = exposure_matrix.loc[lender, healthy_spvs].sum()
            if lender_total_healthy > 0:
                lender_exposure_here = exposure_matrix.loc[lender, spv]
                fraction = lender_exposure_here / lender_total_healthy
                withdrawn_amount += withdrawal_needed * fraction
        
        impact_report.append({
            "SPV": spv,
            "Original_Funding": original_funding,
            "Liquidity_Pulled": withdrawn_amount,
            "Funding_Gap_Pct": (withdrawn_amount / original_funding) * 100 if original_funding > 0 else 0
        })
        
    return pd.DataFrame(impact_report)
