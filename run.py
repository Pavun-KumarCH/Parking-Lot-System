from parking_lot import ParkingLot
from vehicle import Car, Truck, Motorcycle, Van

def main():
    name = input("Enter parking lot operator name: ")
    parking_lot = ParkingLot(name)

    while True:
        print("\nMenu:")
        print("1. Parking Entry Gate")
        print("2. Parking Exit Gate")
        print("3. Check Parking Status")
        print("4. Check Vehicle Status")
        print("5. Exit Program")

        choice = input("\n Enter your choice:")
        try:
            choice = int(choice)
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if choice == 1:
            handle_parking_entry(parking_lot)
        elif choice == 2:
            handle_parking_exit(parking_lot)
        elif choice == 3:
            print(parking_lot.get_empty_spot_number())
        elif choice == 4:
            handle_vehicle_status(parking_lot)
        elif choice == 5:
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option.")

def handle_parking_entry(parking_lot):
    vehicle_type = input("\nEnter vehicle type:\n1. Car\n2. Motorcycle\n3. Truck\n4. Van\n")
    try:
        vehicle_type = int(vehicle_type)
    except ValueError:
        print("Invalid input. Please enter a number.")
        return

    if vehicle_type < 1 or vehicle_type > 4:
        print("Invalid vehicle type.")
        return

    vehicle_number = input("\n Enter vehicle number:")
    if vehicle_type == 1:
        vehicle = Car(vehicle_number)
    elif vehicle_type == 2:
        vehicle = Motorcycle(vehicle_number)
    elif vehicle_type == 3:
        vehicle = Truck(vehicle_number)
    else:
        vehicle = Van(vehicle_number)

    ticket_number = parking_lot.get_new_parking_ticket(vehicle)
    if isinstance(ticket_number, str):  # Check if it's an error message
        print(ticket_number)
    else:
        print(f"Ticket issued. Ticket number: {ticket_number}")

def handle_parking_exit(parking_lot):
    ticket_number = input("\n Enter ticket number: ")
    try:
        ticket_number = int(ticket_number)
    except ValueError:
        print("Invalid input. Please enter a number.")
        return

    vehicle_number, parking_cost = parking_lot.leave_parking(ticket_number)
    if parking_cost is None:
        print(vehicle_number)  # Error message
    else:
        print(f"Vehicle Number: {vehicle_number}. Parking cost: {parking_cost}.")
def handle_vehicle_status(parking_lot):
    ticket_number = input("\n Enter ticket number: ")
    try:
        ticket_number = int(ticket_number)
    except ValueError:
        print("Invalid input. Please enter a number.")
        return

    vehicle_status = parking_lot.vehicle_status(ticket_number)
    if isinstance(vehicle_status, tuple):  # Check if it's an error message
        print(vehicle_status[0])  # Print the error message
    else:
        for key, value in vehicle_status.items():
            print(f"{key}: {value}")


if __name__ == "__main__":
    main()
