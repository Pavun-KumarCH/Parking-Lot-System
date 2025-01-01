import time
import json
import config
from enums import VehicleType

class ParkingLot:
    """Parking Lot System."""

    def __init__(self, name):
        self.name = name
        self.compact_spot_count = 0
        self.large_spot_count = 0
        self.motorbike_spot_count = 0
        self.max_compact_count = config.COMPACT_COUNT
        self.max_large_count = config.LARGE_COUNT
        self.max_motorbike_count = config.MOTORBIKE_COUNT

        # all active parking tickets, identified by their ticket_number
        self.active_tickets = {}
        self.parking_history = {}

    def get_new_parking_ticket(self, vehicle):
        """Park vehicle in parking lot if spot is available.
        Args: vehicle object

        Returns: ticket number or message
        """
        if self.is_full(vehicle.get_type()):
            return "Parking Full!"

        ticket = int(time.time() * 100)  # Generate unique ticket number
        vehicle.assign_ticket(ticket)
        self._increment_spot_count(vehicle.get_type())
        self.active_tickets[ticket] = vehicle
        return ticket

    def is_full(self, vehicle_type):
        """Check Parking lot status

        Args: vehicle_type (VehicleType)

        Returns: True if parking lot is full, False otherwise
        """
        if vehicle_type in {VehicleType.TRUCK, VehicleType.VAN}:
            return self.large_spot_count >= self.max_large_count

        if vehicle_type == VehicleType.MOTORBIKE:
            return self.motorbike_spot_count >= self.max_motorbike_count

        if vehicle_type == VehicleType.CAR:
            return (self.compact_spot_count + self.large_spot_count) >= (
                self.max_compact_count + self.max_large_count)

    def _increment_spot_count(self, vehicle_type):
        """Update parking spot count.

        Args: vehicle_type (VehicleType)

        Returns: None
        """
        if vehicle_type in {VehicleType.TRUCK, VehicleType.VAN}:
            self.large_spot_count += 1
        elif vehicle_type == VehicleType.MOTORBIKE:
            self.motorbike_spot_count += 1
        elif vehicle_type == VehicleType.CAR:
            if self.compact_spot_count < self.max_compact_count:
                self.compact_spot_count += 1
            else:
                self.large_spot_count += 1

    def _decrement_spot_count(self, vehicle_type):
        """Update parking spot count.

        Args: vehicle_type (VehicleType)

        Returns: None
        """
        if vehicle_type in {VehicleType.TRUCK, VehicleType.VAN}:
            self.large_spot_count -= 1
        elif vehicle_type == VehicleType.MOTORBIKE:
            self.motorbike_spot_count -= 1
        elif vehicle_type == VehicleType.CAR:
            if self.compact_spot_count > 0:
                self.compact_spot_count -= 1
            else:
                self.large_spot_count -= 1

    def leave_parking(self, ticket_number):
        """Exit vehicle from parking. Remove vehicle from active_tickets and calculate parking charges.

        Args:
            ticket_number: int ticket_number

        Returns: vehicle_number and parking_charge
        """
        if ticket_number in self.active_tickets:
            vehicle = self.active_tickets.pop(ticket_number)
            self._decrement_spot_count(vehicle.get_type())
            parking_charge = vehicle.parking_charge()
            vehicle.update_parking_status(parking_charge)
            self.parking_history[ticket_number] = vehicle
            return vehicle.vehicle_number, parking_charge
        return "Invalid ticket number.", None

    def vehicle_status(self, ticket_number):
        """Check the vehicle status

        Args:
            ticket_number: int ticket_number

        Returns: dict with vehicle details or error message
        """
        if ticket_number in self.parking_history:
            vehicle = self.parking_history[ticket_number]
            vehicle_details = {
                "Vehicle Number": vehicle.vehicle_number,
                "Vehicle Type": vehicle.vehicle_type.name,
                "Parking Spot Type": vehicle.parking_spot_type.name,
                "Parking Time": vehicle.parking_time.strftime("%d-%m-%Y, %H:%M:%S"),
                "Parking Charge": vehicle.parking_cost,
                "Ticket Status": vehicle.ticket_status.name
            }
            return vehicle_details
        return "Invalid ticket number.", None

    def get_empty_spot_number(self):
        """Return available parking spots.

        Returns: available parking space as a string.
        """
        message = []
        if self.max_compact_count - self.compact_spot_count > 0:
            message.append(f"Free Compact: {self.max_compact_count - self.compact_spot_count}")
        else:
            message.append("Compact is Full.")

        if self.max_large_count - self.large_spot_count > 0:
            message.append(f"Free Large: {self.max_large_count - self.large_spot_count}")
        else:
            message.append("Large is Full.")

        if self.max_motorbike_count - self.motorbike_spot_count > 0:
            message.append(f"Free Motorbike: {self.max_motorbike_count - self.motorbike_spot_count}")
        else:
            message.append("Motorbike is Full.")

        return "\n".join(message)
