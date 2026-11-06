from typing import Optional, List
from datetime import datetime
from enum import Enum
from pydantic import Field, BaseModel, ValidationError, model_validator


class Rank(str, Enum):
    CADET = "cadet"
    OFFICER = "officer"
    LIEUTENANT = "lieutenant"
    CAPTAIN = "captain"
    COMMANDER = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = True


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: List[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: Optional[str] = Field(default="planned")
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode='after')
    def validation_rulrs(self) -> "SpaceMission":
        if not self.mission_id.startswith("M"):
            raise ValueError("Mission ID must start with 'M'")
        if not any(m.rank in (Rank.COMMANDER, Rank.CAPTAIN)
                   for m in self.crew):
            raise ValueError(
                "Mission must have at least one Commander or Captain")
        if self.duration_days > 365 and sum(m.years_experience >= 5 for
                                            m in self.crew) > len(self.crew):
            raise ValueError(
                "Long missions (> 365 days) need 50%"
                "experienced crew (5+ years)")
        if not all(m.is_active for m in self.crew):
            raise ValueError("All crew members must be active")
        return self


def main() -> None:
    print("Space Mission Crew Validation")

    try:
        crew_members = [
            CrewMember(
                member_id="CM001",
                name="Sarah Connor",
                rank=Rank.COMMANDER,
                age=45,
                specialization="Mission Command",
                years_experience=15,
                is_active=True,
            ),
            CrewMember(
                member_id="CM002",
                name="John Smith",
                rank=Rank.LIEUTENANT,
                age=35,
                specialization="Navigation",
                years_experience=8,
                is_active=True,
            ),
            CrewMember(
                member_id="CM003",
                name="Alice Johnson",
                rank=Rank.OFFICER,
                age=28,
                specialization="Engineering",
                years_experience=3,
                is_active=True,
            ),
        ]

        valid_mission = SpaceMission(
            mission_id="M2024_MARS",
            mission_name="Mars Colony Establishment",
            destination="Mars",
            launch_date=datetime.now(),
            duration_days=900,
            crew=crew_members,
            budget_millions=2500.0,
        )

        print("Valid mission created:")
        print(f"Mission: {valid_mission.mission_name}")
        print(f"ID: {valid_mission.mission_id}")
        print(f"Destination: {valid_mission.destination}")
        print(f"Duration: {valid_mission.duration_days} days")
        print(f"Budget: ${valid_mission.budget_millions:.1f}M")
        print(f"Crew size: {len(valid_mission.crew)}")
        print("Crew members:")
        for member in valid_mission.crew:
            print(
                f"{member.name} ({member.rank.value})"
                f" - {member.specialization}"
            )
    except ValidationError as e:
        print(f"Unexpected error: {e}")

    print("Expected validation error:")
    try:
        invalid_crew = [
            CrewMember(
                member_id="CM004",
                name="Bob Wilson",
                rank=Rank.OFFICER,
                age=30,
                specialization="Engineering",
                years_experience=5,
                is_active=True,
            ),
            CrewMember(
                member_id="CM005",
                name="Carol White",
                rank=Rank.LIEUTENANT,
                age=32,
                specialization="Science",
                years_experience=6,
                is_active=True,
            ),
        ]

        SpaceMission(
            mission_id="M2024_TEST",
            mission_name="Test Mission",
            destination="Moon",
            launch_date=datetime.now(),
            duration_days=100,
            crew=invalid_crew,
            budget_millions=500.0,
        )
    except ValidationError as e:
        msg = e.errors()[0]["msg"].removeprefix("Value error, ")
        print(msg)


if __name__ == "__main__":
    main()
