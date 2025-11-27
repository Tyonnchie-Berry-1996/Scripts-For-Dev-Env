import csv


def main():
    csv_file = 'contacts.csv'
    contacts = []
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            email = row.get('E-mail 1 - Value', '')
            contacts.append({'email': email})

        for contact in contacts:
            fields = ['email']
            for field in fields:
                if contact[field]:
                    print(f"{field.capitalize()}: {contact[field]}")

            with open('email-only.csv', 'w', newline='', encoding='utf-8') as shit:
                writer = csv.DictWriter(shit, fieldnames=fields)
                writer.writeheader()
                for contact in contacts:
                    writer.writerow(contact)


if __name__ == "__main__":
    main()
