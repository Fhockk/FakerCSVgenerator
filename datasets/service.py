from faker import Faker
import random
import csv

fake = Faker()

row_headers = {
    ' full_name': 'Full name',
    ' company': 'Company',
    ' job': 'Job',
    ' email': 'Email',
    ' date': 'Date',
    ' domain_name': 'Domain name',
    ' phone_number': 'Phone number',
    ' address': 'Address',
    ' integer': 'Integer',
    ' text': 'Text'
}


def write_csv(data, rows_number, filename, delimiter, quotechar):
    headers = []
    for el in data:
        headers.append(row_headers[el[1]])
    rows = []
    get_columns = [el[2] for el in data]
    for i in range(int(rows_number)):
        types_to_fake_data = {
            ' full_name': fake.name(),
            ' company': fake.company(),
            ' job': fake.job(),
            ' email': fake.email(),
            ' date': fake.date(),
            ' domain_name': fake.domain_name(),
            ' phone_number': fake.phone_number(),
            ' address': fake.address(),
            ' integer': None,
            ' text': None
        }
        for el in data:
            if el[2] == ' integer':
                min_value = int(el[3])
                max_value = int(el[4])
                types_to_fake_data[' integer'] = fake.pyint(min_value=min_value, max_value=max_value)
            if el[2] == ' text':
                min_value = int(el[3])
                max_value = int(el[4])
                num_sentences = random.randint(min_value, max_value)
                types_to_fake_data[' text'] = ' '.join([fake.sentence() for _ in range(num_sentences)])
        row = [types_to_fake_data[column] for column in get_columns]
        rows.append(row)

    with open(f'media/csv/{filename}.csv', mode='w') as file:
        writer = csv.writer(file, delimiter=delimiter, quotechar=quotechar)
        writer.writerow(headers)
        writer.writerows(rows)
