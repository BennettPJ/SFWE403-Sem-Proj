import csv

class Pharmacy:
    def __init__(self, name, website, address, owner, phone_number, hours):
        self.name = name
        self.website = website
        self.address = address
        self.owner = owner
        self.phone_number = phone_number
        self.hours = hours

    def to_dict(self):
        return {
            "name": self.name,
            "website": self.website,
            "address": self.address,
            "owner": self.owner,
            "phone_number": self.phone_number,
            "hours": self.hours
        }

class PharmacySystem:
    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.pharmacies = []

    def add_pharmacy(self, pharmacy):
        self.pharmacies.append(pharmacy)

    def save_to_csv(self):
        with open(self.csv_file, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["name", "website", "address", "owner", "phone_number", "hours"])
            writer.writeheader()
            for pharmacy in self.pharmacies:
                writer.writerow(pharmacy.to_dict())

    def load_from_csv(self):
        self.pharmacies = []
        with open(self.csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                pharmacy = Pharmacy(
                    name=row["name"],
                    website=row["website"],
                    address=row["address"],
                    owner=row["owner"],
                    phone_number=row["phone_number"],
                    hours=row["hours"]
                )
                self.pharmacies.append(pharmacy)

# Example usage
if __name__ == "__main__":
    pharmacy_system = PharmacySystem('pharmacy_hours.csv')

#usage Example below

    # # Adding a new pharmacy
    # new_pharmacy = Pharmacy(
    #     name="Pharmacy A",
    #     website="http://pharmacya.com",
    #     address="123 Main St",
    #     owner="John Doe",
    #     phone_number="123-456-7890",
    #     hours="9 AM - 9 PM"
    # )
    # pharmacy_system.add_pharmacy(new_pharmacy)

    # # Save to CSV
    # pharmacy_system.save_to_csv()

    # # Load from CSV
    # pharmacy_system.load_from_csv()
    # for pharmacy in pharmacy_system.pharmacies:
    #     print(pharmacy.to_dict())