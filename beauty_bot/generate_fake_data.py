from faker import Faker
from bot.models import Salon, Specialist


fake = Faker('ru_RU')


for _ in range(5):
    Salon.objects.create(
        name=fake.company(),
        address=fake.address(),
        phone=fake.phone_number(),
        email=fake.email(),
        opening_time="09:00:00",
        closing_time="20:00:00"
    )

for _ in range(10):
    Specialist.objects.create(name=fake.name())

print("Случайные данные сгенерированы.")