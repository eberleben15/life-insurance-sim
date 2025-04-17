from models import Policyholder, Policy, Gender, HealthRating, PolicyType
from mortality import load_mortality_table
from simulation import simulate_policy_lifecycle
import uuid
from datetime import date

def run_single_test():
    mortality_table = load_mortality_table("data/mortality_table.csv")

    ph = Policyholder(
        id=uuid.uuid4(),
        age_at_issue=40,
        gender=Gender.MALE,
        smoker=False,
        health_rating=HealthRating.STANDARD
    )

    policy = Policy(
        policy_id=uuid.uuid4(),
        policyholder_id=ph.id,
        issue_date=date(2020, 1, 1),
        term_years=20,
        face_amount=500_000,
        annual_premium=1200.0,
        policy_type=PolicyType.TERM,
        interest_rate=0.03
    )

    result = simulate_policy_lifecycle(ph, policy, mortality_table)
    
    print(f"Policy ID: {result.policy_id}")
    print(f"Total Premiums Paid: {result.total_premium_paid}")
    print(f"Claim Paid: {result.claim_paid}")
    print(f"Year of Death: {result.year_of_death}")
    print(f"Alive at End?: {result.alive}")
    print("Yearly Breakdown:")
    for year_info in result.years:
        print(year_info)

if __name__ == "__main__":
    run_single_test()