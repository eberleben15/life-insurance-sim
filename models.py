from dataclasses import dataclass
from datetime import date
from enum import Enum
from typing import Optional
import uuid

class Gender(str, Enum):
    MALE = 'M'
    FEMALE = 'F'

class HealthRating(str, Enum):
    PREFERRED = 'Preferred'
    STANDARD = 'Standard'
    SUBSTANDARD = 'Substandard'

class PolicyType(str, Enum):
    TERM = 'Term'
    WHOLE = 'Whole'
    UNIVERSAL = 'Universal'

@dataclass
class Policyholder:
    id: uuid.UUID
    age_at_issue: int
    gender: Gender
    smoker: bool
    health_rating: HealthRating
    occupation_risk: Optional[str] = None
    annual_income: Optional[float] = None

@dataclass
class Policy:
    policy_id: uuid.UUID
    policyholder_id: uuid.UUID
    issue_date: date
    term_years: int
    face_amount: float
    annual_premium: float
    policy_type: PolicyType
    interest_rate: float

@dataclass
class MortalityRecord:
    age: int
    gender: Gender
    smoker: bool
    qx: float  # Probability of death