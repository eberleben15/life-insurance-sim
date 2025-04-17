from datetime import timedelta
from models import Policy, Policyholder, MortalityRecord, Gender
from mortality import lookup_qx
from typing import List, Dict

class SimulationResult:
    def __init__(self, policy_id):
        self.policy_id = policy_id
        self.years = []
        self.alive = True
        self.lapsed = False
        self.total_premium_paid = 0.0
        self.claim_paid = 0.0
        self.year_of_death = None

    def add_year(self, year, alive, premium_paid, claim_paid):
        self.years.append({
            "year": year,
            "alive": alive,
            "premium_paid": premium_paid,
            "claim_paid": claim_paid
        })
        self.total_premium_paid += premium_paid
        self.claim_paid += claim_paid

def simulate_policy_lifecycle(
    policyholder: Policyholder,
    policy: Policy,
    mortality_table: List[MortalityRecord]
) -> SimulationResult:
    
    result = SimulationResult(policy.policy_id)
    current_age = policyholder.age_at_issue
    alive = True
    current_year = policy.issue_date.year

    for year in range(policy.term_years):
        if not alive:
            break

        qx = lookup_qx(
            mortality_table,
            age=current_age,
            gender=policyholder.gender,
            smoker=policyholder.smoker
        )

        import random
        death_roll = random.random()
        died = death_roll < qx

        if died:
            result.add_year(current_year, alive=False, premium_paid=policy.annual_premium, claim_paid=policy.face_amount)
            result.alive = False
            result.year_of_death = current_year
            break
        else:
            result.add_year(current_year, alive=True, premium_paid=policy.annual_premium, claim_paid=0.0)

        current_age += 1
        current_year += 1

    return result