from dataclasses import dataclass


@dataclass
class Package:
    package_id: int
    address: str
    city: str
    state: str
    zip: int
    delivery_deadline: str
    weight: int
    special_notes: str = ""
