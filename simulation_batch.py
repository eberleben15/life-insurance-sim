from simulation import simulate_policy_lifecycle
from models import Policyholder, Policy, Gender, HealthRating, PolicyType
from mortality import load_mortality_table
from datetime import date
import uuid
import statistics

def run_monte_carlo_simulation(n_runs: int = 1000):
    mortality_table = load_mortality_table("data/mortality_table.csv")

    # Create a single test policyholder and policy
    policyholder = Policyholder(
        id=uuid.uuid4(),
        age_at_issue=40,
        gender=Gender.MALE,
        smoker=False,
        health_rating=HealthRating.STANDARD
    )

    policy = Policy(
        policy_id=uuid.uuid4(),
        policyholder_id=policyholder.id,
        issue_date=date(2020, 1, 1),
        term_years=20,
        face_amount=500_000,
        annual_premium=1200.0,
        policy_type=PolicyType.TERM,
        interest_rate=0.03
    )

    total_premiums = []
    total_claims = []
    death_count = 0
    survival_count = 0

    for _ in range(n_runs):
        result = simulate_policy_lifecycle(policyholder, policy, mortality_table)
        total_premiums.append(result.total_premium_paid)
        total_claims.append(result.claim_paid)
        if not result.alive:
            death_count += 1
        else:
            survival_count += 1

    print(f"📊 Monte Carlo Summary ({n_runs} runs):")
    print(f"Avg Premiums Paid: {statistics.mean(total_premiums):,.2f}")
    print(f"Avg Claims Paid: {statistics.mean(total_claims):,.2f}")
    print(f"Death Rate: {100 * death_count / n_runs:.2f}%")
    print(f"Survival Rate: {100 * survival_count / n_runs:.2f}%")
    print(f"Avg Net Profit for Insurer: {statistics.mean([p - c for p, c in zip(total_premiums, total_claims)]):,.2f}")

if __name__ == "__main__":
    run_monte_carlo_simulation(n_runs=1000)