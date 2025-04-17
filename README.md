# 🧮 Life Insurance Risk Simulation

This project simulates the lifecycle of life insurance policies using classical Monte Carlo methods. It models policyholders, policy terms, and mortality data to estimate insurer risk, expected payouts, and profitability. The simulation engine is designed to later support quantum computing experiments for comparative analysis.

---

## 🚀 Features

- 📊 Classical Monte Carlo simulation of life insurance policies
- 👤 Supports diverse policyholder attributes (age, gender, smoking status, etc.)
- 💰 Tracks premiums, death claims, and insurer net profit
- 📈 Portfolio-scale simulations with summary statistics per demographic group
- 🧠 Designed for future integration with quantum algorithms

---

## 🗂️ Project Structure
life_insurance_sim/
├── models.py                 # Data classes for policies and people
├── mortality.py              # Mortality table loading & lookup
├── simulation.py             # Core simulation logic (one policy run)
├── simulation_batch.py       # Monte Carlo simulation of single profile
├── simulation_portfolio.py   # Diverse portfolio simulation (1000s of runs)
├── main.py                   # Test runner for single policy
└── data/
└── mortality_table.csv   # Sample mortality data (editable)

---

## 🧑‍💼 Policyholder Modeling

Each `Policyholder` is defined by:
- Age at policy issue
- Gender
- Smoker/non-smoker
- Health rating
- Optional: income, occupation risk

Policies include:
- Term length
- Face amount
- Annual premium
- Interest rate (for future enhancements)

---

## 📁 Example Mortality Table (`data/mortality_table.csv`)

```csv
age,gender,smoker,qx
40,M,False,0.002
40,M,True,0.004
40,F,False,0.001
...

You can extend this up to age 100+ or use real actuarial tables.