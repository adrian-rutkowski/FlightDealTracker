from dataclasses import dataclass
from typing import Optional

@dataclass
class DestinationModel:
    fly_from: str
    fly_to: str
    stay_min: int
    stay_max: int
    acceptable_price: int
    ret_to_diff_city: bool
    max_stopovers: int
    ret_from_diff_city: Optional[bool] = None
    date_from: Optional[str] = None
    date_to: Optional[str] = None


@dataclass
class TripModel:
    fly_from: str
    fly_to: str
    departure_date: str
    length_of_stay: int
    price: int
    airline: str
    url: Optional[str] = None

@dataclass
class AirlineModel:
    code: str
    name: str
