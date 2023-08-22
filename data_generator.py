#!/usr/bin/python3

from faker import Faker

class RandomDataGenerator:
    def __init__(self):
        """
        Initial paramethers of the data random generator class
        """
        self.fake = Faker(["es_ES", "es_MX", "es_AR", "fr_FR", "it_IT", "pt_PT", "en_GB", "en_US"])
        self.generated_data = []


    def __iter__(self):
        """
        Sets up the class as an iterator class, returning itself
        :return:
        """
        pass

    def __next__(self):
        """
        Defines the logic to create new random data of corresponding type
        :return:
        """
        pass

    def _gen_random(self):
        """
        Generates a line of fake data, using this model
        - personal_data: name, last_name, sex, telfnumber, passport, email
        - location: fullname, city, address
        - profesional_data: fullname,company, company address, company telfnumber, job, company email
        - bank_data :passport, IBAN, Salary
        - net data: address, IPv4
        """
        fullname = self.fake.name()
        name = fullname.split()[0]
        lastname = fullname.split()[1]
        sex = self.fake.random_choices(elements=("M", "F", "ND"))
        telfnumber = self.fake.phone_number()
        passport = self.fake.passport_number()
        email = self.fake.ascii_free_email()
        city = self.fake.city()
        address = self.fake.street_address()
        company = self.fake.company()
        company_address = self.fake.street_address()
        company_telfnumber = self.fake.phone_number()
        job = self.fake.job()
        company_email = self.fake.ascii_company_email()
        IBAN = self.fake.iban()
        salary = str(self.fake.pyint(min_value=30000, max_value=200000)) + str(self.fake.currency_symbol())
        IPv4 = self.fake.ipv4()

        personal_data = {
            "name": name,
            "last_name": lastname,
            "sex": sex,
            "telfnumber": telfnumber,
            "passport": passport,
            "email": email,
        }

        location = {
            "fullname": fullname,
            "city": city,
            "address": address
        }

        professional_data = {
            "fullname": fullname,
            "company": company,
            "company address": company_address,
            "company_telfnumber": company_telfnumber,
            "company_email": company_email,
            "job": job
        }

        bank_data = {
            "passport": passport,
            "IBAN": IBAN,
            "salary": salary
        }

        net_data = {
            "address": address,
            "IPv4": IPv4
        }

        self.generated_data.append(personal_data)
        self.generated_data.append(location)
        self.generated_data.append(professional_data)
        self.generated_data.append(bank_data)
        self.generated_data.append(net_data)

