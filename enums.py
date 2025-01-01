from enum import Enum

class VehicleType(Enum):
    CAR = 1
    TRUCK = 2
    VAN = 3
    MOTORBIKE = 4

class ParkingSpotType(Enum):
    COMPACT = 1
    LARGE = 2
    MOTORBIKE = 3

class ParkingTicketStatus(Enum):
    ACTIVE = 1
    PAID = 2
    LOST = 3
