import numpy as np
import pandas as pd
from typing import Tuple, Dict

def calculate_retail_panic(current_drop_pct: float, retail_leverage_ratio: float = 2.5) -> float:
    """
    Simulates the 'Gamma Squeeze' or Margin Call Cascade.
    Retail traders often hold unsecured leverage (margin loans). 
    If the market drops >10%, forced liquidations amplify the crash.
    
    Args:
        current_drop_pct: The fundamental drop (e.g., 0.15 for 15%)
        retail_leverage_ratio: Multiplier for forced selling.
    """
    panic_threshold = 0.10
    
    if current_drop_pct < panic_threshold:
        return 0.0
    
    # Non-linear feedback loop
    margin_call_impact = (current_drop_pct - panic_threshold) * retail_leverage_ratio
    return margin_call_impact

def simulate_depreciation_cliff(
    initial_asset_value: float = 500e6,
    initial_debt: float = 400e6,
    maturity_years: int = 3,
    scenarios: Dict[str, float] = None
) -> pd.DataFrame:
    """
    Simulates the Mark-to-Market LTV of an SPV under different 
    technological obsolescence scenarios.
    """
    if scenarios is None:
        scenarios = {"Soft Landing": 0.20, "Blackwell Shock": 0.55}
        
    months = np.linspace(0, maturity_years, maturity_years * 12 + 1)
    results = pd.DataFrame(index=months)
    results.index.name = "Years_Elapsed"
    
    for name, decay_rate in scenarios.items():
        curr_asset_val = initial_asset_value * np.exp(-decay_rate * months)
        ltv = (initial_debt / curr_asset_val) * 100
        results[name] = ltv
        
    return results
