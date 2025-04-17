from simulation import simulate_policy_lifecycle
from models import Policyholder, Policy, Gender, HealthRating, PolicyType
from mortality import load_mortality_table
from datetime import date
import uuid
import statistics
from collections import defaultdict

def generate_portfolio():
    """Create a list of diverse policyholders and policies."""
    portfolio = []
    ages = [30, 40, 50, 60]
    genders = [Gender.MALE, Gender.FEMALE]
    smoking_statuses = [True, False]
    face_amounts = [250_000, 500_000, 1_000_000]
    premiums = [600.0, 1200.0, 2400.0]

    for age in ages:
        for gender in genders:
            for smoker in smoking_statuses:
                for i in range(len(face_amounts)):
                    ph = Policyholder(
                        id=uuid.uuid4(),
                        age_at_issue=age,
                        gender=gender,
                        smoker=smoker,
                        health_rating=HealthRating.STANDARD
                    )

                    policy = Policy(
                        policy_id=uuid.uuid4(),
                        policyholder_id=ph.id,
                        issue_date=date(2020, 1, 1),
                        term_years=20,
                        face_amount=face_amounts[i],
                        annual_premium=premiums[i],
                        policy_type=PolicyType.TERM,
                        interest_rate=0.03
                    )

                    portfolio.append((ph, policy))
    return portfolio

def run_simulation_on_portfolio(portfolio, mortality_table, runs_per_policy=500):
    print(f"🧾 Simulating {len(portfolio)} unique policies × {runs_per_policy} runs each...")
    
    summary = defaultdict(list)

    for idx, (ph, policy) in enumerate(portfolio):
        for _ in range(runs_per_policy):
            result = simulate_policy_lifecycle(ph, policy, mortality_table)
            key = (ph.age_at_issue, ph.gender.value, ph.smoker, policy.face_amount)
            summary[key].append({
                "premiums": result.total_premium_paid,
                "claims": result.claim_paid,
                "died": not result.alive
            })

    print(f"\n📊 Results Summary:")
    for key, results in summary.items():
        age, gender, smoker, face = key
        premiums = [r["premiums"] for r in results]
        claims = [r["claims"] for r in results]
        deaths = sum(1 for r in results if r["died"])

        print(f"\n🧑‍🤝‍🧑 Profile: Age {age}, Gender {gender}, Smoker: {smoker}, Face: ${face:,}")
        print(f"  Death Rate: {100 * deaths / len(results):.1f}%")
        print(f"  Avg Premiums Paid: ${statistics.mean(premiums):,.2f}")
        print(f"  Avg Claims Paid: ${statistics.mean(claims):,.2f}")
        print(f"  Avg Net Profit: ${statistics.mean([p - c for p, c in zip(premiums, claims)]):,.2f}")

if __name__ == "__main__":
    portfolio = generate_portfolio()
    mortality_table = load_mortality_table("data/mortality_table.csv")
    run_simulation_on_portfolio(portfolio, mortality_table, runs_per_policy=500)