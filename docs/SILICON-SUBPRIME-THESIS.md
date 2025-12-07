
# The Silicon Subprime Thesis: A Systemic Risk Overview

## 1\. The Framework: The "Four Ls" of AI Systemic Risk

*We adapt the IMF/Bisias-Flood-Lo-Valavanis framework to the specific structure of the AI Compute trade.*

### **L1: Loss (The Depreciation Cliff)**

In a standard credit model, loss is a probability function of default. In the AI trade, **Loss is a certainty function of Moore's Law.**

  * **The Mechanism:** A borrower (SPV) buys an H100 GPU for $25,000. This asset is the *only* collateral for the loan.
  * **The Problem:** The release of the Blackwell (B200) chip offers \~4x performance for a similar price. This renders the H100 effectively obsolete for "Training" (premium pricing), relegating it to "Inference" (commodity pricing).
  * **The Metric:** If H100 rental rates drop from $4/hr to $2/hr, the *Loss Given Default (LGD)* on the loan rises to \>60%, because the liquidation value of the hardware collapses.

### **L2: Leverage (The Hidden Multiplier)**

Leverage in this bubble is not just "Debt/Equity"; it is "Operating Leverage" disguised as "Financial Leverage."

  * **The Structure:** "Neoclouds" (e.g., CoreWeave, Lambda) are borrowing at **80-90% Loan-to-Cost (LTC)** via SPVs.
  * **The Trick:** They are not borrowing against *corporate* cash flow; they are borrowing against the *projected contract value* of the GPU leases.
  * **Systemic Risk:** This is effectively a "Margin Loan" on hardware. If the value of the hardware drops (see *Loss*), the lender issues a margin call. But you cannot "top up" a physical data center. You have to sell it.

### **L3: Liquidity (The Duration Mismatch)**

The crisis point is the **2028 Refinancing Wall**.

  * **Liability Side:** The loans are typically 3-5 year "Private Credit" facilities. They are often **Interest-Only**, meaning the principal ($1B+) is due in a single balloon payment at the end.
  * **Asset Side:** By 2028, the H100s will be 4 years old. In semiconductor terms, they are e-waste.
  * **The Trap:** No bank will refinance a $1B loan on e-waste. The SPV must pay the balloon with cash it doesn't have. *Liquidity vanishes exactly when it is needed most.*

### **L4: Linkages (The Contagion Map)**

This is not a random network; it is a **Circular Financing Scheme**.

1.  **Nvidia** invests in **CoreWeave** (Equity).
2.  **CoreWeave** uses that valuation to borrow $7.5B from **Blackstone** (Debt).
3.  **CoreWeave** gives that $7.5B back to **Nvidia** to buy GPUs.
4.  **Nvidia** books this as "Data Center Revenue," boosting its stock price.
5.  **Blackstone** marks the loan as "Performing" because CoreWeave has new assets.

<!-- end list -->

  * **The Failure Mode:** If Step 2 stops (Credit Freeze), Step 4 (Nvidia Revenue) collapses, which hurts Step 1 (Valuation), which triggers a default in Step 2.

-----

## 2\. The Hierarchy of Money & "Shadow Money" Creation

You asked if these firms can "create money." In the Perry Mehrling "Money View," the answer is **Yes**.

### **The Hierarchy of Money (AI Edition)**

Money is not just cash; it is a pyramid of promises.

1.  **Money (High-Powered):** Reserves at the Fed (Central Bank Money).
2.  **Deposits (Bank Money):** Checking accounts (JP Morgan).
3.  **Securities (Shadow Money):** *This is where the bubble is.*

### **How the Bubble Creates Money**

In this ecosystem, **an AI Loan is treated as Money.**

  * **Step 1:** A Private Credit fund (Blue Owl) takes illiquid pension fund capital and lends it to an SPV.
  * **Step 2:** The SPV "pays" Nvidia with this borrowed credit.
  * **Step 3:** Nvidia treats this credit as "Cash on Balance Sheet."
  * **Step 4:** Nvidia uses that "Cash" to buy share buybacks or acquire other companies.

**The Magic Trick:** The Private Credit fund effectively **monetized the future value of a GPU** that hasn't even been plugged in yet. They turned an *expectation of compute* into *purchasing power today*. This *expands* the effective money supply (elasticity) just as Mortgage-Backed Securities did in 2006.

-----

## 3\. The Players & The Map (Who is Holding the Bag?)

### **The Lenders (The Shadow Banks)**

  * **Blackstone:** Led the $7.5B debt facility for CoreWeave.
  * **Blue Owl:** A major player in "ABS" (Asset-Backed Securities) for tech; financed Crusoe Energy.
  * **Apollo:** Specializes in "investment grade" private credit for large cap tech.

### **The Borrowers (The "Neoclouds")**

These are the "Subprime" borrowers—companies that exist primarily to hold debt that Microsoft/Google don't want on their own balance sheets.

  * **CoreWeave**
  * **Lambda Labs**
  * **Crusoe Energy**
  * **Voltage Park**

### **The Landlords (The Physical Constraint)**

  * **QTS / Vantage / Digital Realty:** The entities building the actual concrete shells. They are *also* leveraged. If the Neoclouds default on rent, the Landlords default on their construction loans.

-----

### YouTube Reference

This video provides a clear breakdown of the "Circular Financing" linkages described in Section 4 (Nvidia -\> Cloud -\> Debt -\> Nvidia).

[Nvidia's Circular Cash Flow Explained](https://www.google.com/search?q=https://www.youtube.com/watch%3Fv%3DgTqvGj13cRM)

*This video is relevant because it visualizes the specific "Linkage" risk where vendor financing inflates revenue, a core component of the "Silicon Subprime" thesis.*



### Sources

* **[Circular Financing: Does Nvidia's $110B Bet Echo the Telecom Bubble?](https://tomtunguz.com/nvidia_nortel_vendor_financing_comparison/)**
    * *Source:* [tomtunguz.com](https://tomtunguz.com)
    * > "Beyond OpenAI , Nvidia holds a $3B stake in CoreWeave 15 , a company that has spent $7.5B on Nvidia GPUs , & $3.7B in other AI startup investments 16 through ..."

* **[The AI Bubble Is Bigger Than You Think](https://prospect.org/2025/11/19/ai-bubble-bigger-than-you-think/)**
    * *Source:* [The American Prospect](https://prospect.org)
    * > "This is the case with an SPV for Meta's $30 billion Hyperion data center in Louisiana. Blue Owl, a private credit fund, owns the majority stake in the SPV; it ..."

### 🧭 Navigation - More on Systemic Risk 🁶 
[systemic-risk](https://github.com/roguetrainer/systemic-risk) | [systemic-risk-intro](https://github.com/roguetrainer/systemic-risk-intro) | [systemic-risk-metrics](https://github.com/roguetrainer/systemic-risk-metrics) | [silicon-subprime](https://github.com/roguetrainer/silicon-subprime) | [too-big-to-teraflop](https://github.com/roguetrainer/too-big-to-teraflop) | [systemic-risk/docs/](https://github.com/roguetrainer/systemic-risk/blob/main/docs/) {
 [systemic-risk-overview](https://github.com/roguetrainer/systemic-risk/blob/main/docs/systemic-risk-overview.md) | [gpu-financial-complex](https://github.com/roguetrainer/systemic-risk/blob/main/docs/gpu-financial-complex)}