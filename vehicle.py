import math
import config
from datetime import datetime
from abc import ABC, abstractmethod
from enums import VehicleType, ParkingTicketStatus, ParkingSpotType

class Vehicle(ABC):
    """Vehicle parent abstract class."""

    def __init__(self, vehicle_number, vehicle_type, parking_spot_type, ticket=None):
        self.vehicle_number = vehicle_number
        self.vehicle_type = vehicle_type
        self.parking_spot_type = parking_spot_type
        self.ticket = ticket
        self.parking_time = datetime.now()
        self.ticket_status = ParkingTicketStatus.ACTIVE
        self.exit_time = None
        self.parking_cost = 0

    def assign_ticket(self, ticket):
        """Assign a parking ticket to the vehicle."""
        self.ticket = ticket

    def get_type(self):
        """Return the type of the vehicle."""
        return self.vehicle_type

    def update_parking_status(self, parking_charge):
        """Update the vehicle's parking status after exit."""
        self.exit_time = datetime.utcnow()
        self.parking_cost = parking_charge
        self.ticket_status = ParkingTicketStatus.PAID

    @abstractmethod
    def parking_charge(self):
        """Abstract method to calculate parking charge."""
        pass

class Car(Vehicle):
    def __init__(self, vehicle_number, ticket=None):
        super().__init__(vehicle_number, VehicleType.CAR, ParkingSpotType.COMPACT, ticket)

    def parking_charge(self):
        now = datetime.utcnow()
        parking_hours = math.ceil((now - self.parking_time).total_seconds() / 3600)
        if parking_hours in config.CAR_PARKING_RATE:
            return config.CAR_PARKING_RATE[parking_hours]
        return config.CAR_PARKING_RATE.get(max(config.CAR_PARKING_RATE.keys()), 0) * parking_hours

class Van(Vehicle):
    def __init__(self, vehicle_number, ticket=None):
        super().__init__(vehicle_number, VehicleType.VAN, ParkingSpotType.LARGE, ticket)

    def parking_charge(self):
        now = datetime.utcnow()
        parking_hours = math.ceil((now - self.parking_time).total_seconds() / 3600)
        if parking_hours in config.VAN_PARKING_RATE:
            return config.VAN_PARKING_RATE[parking_hours]
        return config.VAN_PARKING_RATE.get(max(config.VAN_PARKING_RATE.keys()), 0) * parking_hours

class Truck(Vehicle):
    def __init__(self, vehicle_number, ticket=None):
        super().__init__(vehicle_number, VehicleType.TRUCK, ParkingSpotType.LARGE, ticket)

    def parking_charge(self):
        now = datetime.utcnow()
        parking_hours = math.ceil((now - self.parking_time).total_seconds() / 3600)
        if parking_hours in config.TRUCK_PARKING_RATE:
            return config.TRUCK_PARKING_RATE[parking_hours]
        return config.TRUCK_PARKING_RATE.get(max(config.TRUCK_PARKING_RATE.keys()), 0) * parking_hours

class Motorcycle(Vehicle):
    def __init__(self, vehicle_number, ticket=None):
        super().__init__(vehicle_number, VehicleType.MOTORBIKE, ParkingSpotType.MOTORBIKE, ticket)

    def parking_charge(self):
        now = datetime.utcnow()
        parking_hours = math.ceil((now - self.parking_time).total_seconds() / 3600)
        if parking_hours in config.MOTORBIKE_PARKING_RATE:
            return config.MOTORBIKE_PARKING_RATE[parking_hours]
        return config.MOTORBIKE_PARKING_RATE.get(max(config.MOTORBIKE_PARKING_RATE.keys()), 0) * parking_hours
