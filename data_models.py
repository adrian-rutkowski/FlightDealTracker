from dataclasses import dataclass
from typing import Optional
import constants

@dataclass
class DestinationModel:
    fly_from: str
    fly_to: str
    stay_min: int
    stay_max: int
    acceptable_price: int
    max_stopovers: Optional[int] = 0
    ret_to_diff_city: Optional[bool] = False
    ret_from_diff_city: Optional[bool] = False
    date_from: Optional[str] = constants.DATE_FROM
    date_to: Optional[str] = constants.DATE_TO


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
