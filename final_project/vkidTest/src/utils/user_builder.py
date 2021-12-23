from faker import Faker


fake_rus = Faker('ru-RU')
fake = Faker()

russian_name = fake_rus.first_name() + fake_rus.last_name()
username = fake.profile()["username"]
email = fake.profile()["mail"]
password = fake.password()
