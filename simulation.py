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
        self.pv_premiums = 0.0
        self.pv_claims = 0.0
        self.year_of_death = None

    def add_year(self, year, year_index, interest_rate, alive, premium_paid, claim_paid):
        # Compute present value at issue (year 0)
        pv_premium = premium_paid / ((1 + interest_rate) ** year_index)
        pv_claim = claim_paid / ((1 + interest_rate) ** year_index)

        self.pv_premiums += pv_premium
        self.pv_claims += pv_claim
        self.total_premium_paid += premium_paid
        self.claim_paid += claim_paid

        self.years.append({
            "year": year,
            "alive": alive,
            "premium_paid": premium_paid,
            "claim_paid": claim_paid,
            "pv_premium": pv_premium,
            "pv_claim": pv_claim
        })

    def add_year(self, year, year_index, interest_rate, alive, premium_paid, claim_paid):
        # Compute present value at issue (year 0)
        pv_premium = premium_paid / ((1 + interest_rate) ** year_index)
        pv_claim = claim_paid / ((1 + interest_rate) ** year_index)

        self.pv_premiums += pv_premium
        self.pv_claims += pv_claim
        self.total_premium_paid += premium_paid
        self.claim_paid += claim_paid

        self.years.append({
            "year": year,
            "alive": alive,
            "premium_paid": premium_paid,
            "claim_paid": claim_paid,
            "pv_premium": pv_premium,
            "pv_claim": pv_claim
        })

def simulate_policy_lifecycle(policyholder, policy, mortality_table):
    result = SimulationResult(policy.policy_id)
    current_age = policyholder.age_at_issue
    alive = True
    current_year = policy.issue_date.year

    for year_index in range(policy.term_years):
        if not alive:
            break

        qx = lookup_qx(mortality_table, current_age, policyholder.gender, policyholder.smoker)
        import random
        died = random.random() < qx

        if died:
            result.add_year(current_year, year_index, policy.interest_rate, False, policy.annual_premium, policy.face_amount)
            result.alive = False
            result.year_of_death = current_year
            break
        else:
            result.add_year(current_year, year_index, policy.interest_rate, True, policy.annual_premium, 0.0)

        current_age += 1
        current_year += 1

    return result