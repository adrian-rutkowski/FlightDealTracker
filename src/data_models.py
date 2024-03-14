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
    only_kiwi: Optional[bool] = False


@dataclass
class TripModel:
    fly_from: Optional[str] = None
    fly_to: Optional[str] = None
    departure_date: Optional[str] = None
    length_of_stay: Optional[int] = None
    price: Optional[int] = None
    airline: Optional[str] = None
    url: Optional[str] = None

@dataclass
class AirlineModel:
    code: str
    name: str
