# silicon-subprime 📉
### A Quantitative Risk Simulation of the AI "Refinancing Wall"

> *"History doesn't repeat itself, but it rhymes."* — A structural analysis of Duration Mismatch in GPU-backed Private Credit.

![System Topology](https://via.placeholder.com/800x400?text=Network+Contagion+Topology+Map) 
*(Place the network topology visualization here)*

## 🏛️ The Thesis
The current AI infrastructure boom is being funded by a "Shadow Banking" system that mirrors the pre-2008 Mortgage-Backed Securities market. 
- **The Asset:** H100 GPUs (Rapidly Depreciating)
- **The Liability:** 5-Year Private Credit Loans (Bullet Maturity)
- **The Risk:** A "Refinancing Wall" in 2027-2028 where collateral value falls below the loan principal, triggering a liquidity spiral.

This repository contains numerical experiments that model this **Asset-Liability Mismatch (ALM)** using the IMF's "Four L's" of systemic risk.

## 🧮 The Experiments

### 1. `asset_shock.py` (The "Moore's Law" Decay)
A Monte Carlo simulation stressing the **Loan-to-Value (LTV)** covenants of a hypothetical AI Special Purpose Vehicle (SPV).
* **Input:** Historical depreciation curves of A100 vs. H100 rental rates.
* **Method:** Applies a "Technological Obsolescence" decay function ($\lambda$) to collateral value.
* **Output:** Probability of Default (PD) curves showing insolvency occurring at Month 18, well before loan maturity.

### 2. `contagion_matrix.py` (The "Club Deal" Network)
A Bipartite Graph projection modeling the **Private Credit Syndicate**.
* **Method:** Reconstructs the lending network based on public "tombstones" (e.g., Blackstone, Blue Owl, CoreWeave deals).
* **Mechanism:** Implements a "Hoarding Multiplier." When a lender takes a mark-to-market loss on a toxic vintage (SPV 1), they withdraw liquidity from healthy vintages (SPV 2).
* **Result:** Demonstrates how a specific asset shock becomes a systemic credit crunch.

## 📊 Key Findings from the Model
1.  **The Leverage Trap:** At a 0.50 decay rate (simulating the Blackwell release), LTV breaches 100% in **1.5 years**, rendering the 5-year loan structure structurally unsound.
2.  **The Liquidity Gap:** The average SPV faces a **~60% refinancing gap** at maturity, requiring massive equity injections to prevent default.
3.  **Syndicate Fragility:** Due to high overlap in "Club Deals," a default in the largest borrower transmits shockwaves to >70% of the peripheral network.

## 🛠️ Usage
```bash
# Clone the repo
git clone [https://github.com/yourusername/silicon-subprime.git](https://github.com/yourusername/silicon-subprime.git)

# Run the Asset Shock Simulation
python asset_shock.py --decay_rate 0.55 --leverage 0.80

# Run the Contagion Matrix
python contagion_matrix.py --hoarding_multiplier 2.0
```

## 📚 References & Inspiration
* Paul Kedrosky (SK Ventures): The "Meta-Bubble" Thesis.
* Odd Lots Podcast: "Why AI Is Like Every Bubble All Rolled Into One"
* Center for Public Enterprise: "Bubble or Nothing"
* Goldman Sachs: "Gen AI: Too Much Spend, Too Little Benefit?"

Disclaimer: This project is a theoretical risk modeling exercise for educational purposes. It does not constitute financial advice or an actual prediction of specific company defaults.