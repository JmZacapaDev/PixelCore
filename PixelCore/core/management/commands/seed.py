from django.core.management.base import BaseCommand
from django.db import transaction
from users.models import User
from content.models import MediaContent
from ratings.models import Rating
import uuid
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Seeds the database with sample data for users, media content, and ratings.'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Seeding database...'))

        fake = Faker()

        # Clear existing data (optional, but good for repeatable seeding)
        Rating.objects.all().delete()
        MediaContent.objects.all().delete()
        User.objects.filter(is_superuser=False).delete() # Keep superusers if any

        self.stdout.write(self.style.SUCCESS('Existing data cleared.'))

        # 1. Create 2 users
        users = []
        for i in range(2):
            email = fake.email()
            username = fake.user_name() + str(i) # Appending i to ensure uniqueness
            password = 'password123' # Simple password for seeded users
            user = User.objects.create_user(email=email, username=username, password=password)
            users.append(user)
            self.stdout.write(self.style.SUCCESS(f'Created user: {user.email}'))

        # 2. Create 5 media items
        media_contents = []
        categories = [choice[0] for choice in MediaContent.CATEGORY_CHOICES]
        for i in range(5):
            title = fake.sentence(nb_words=4)[:-1]
            description = fake.paragraph(nb_sentences=3)
            category = random.choice(categories)
            thumbnail_url = fake.image_url()
            content_url = fake.url()
            media_content = MediaContent.objects.create(
                title=title,
                description=description,
                category=category,
                thumbnail_url=thumbnail_url,
                content_url=content_url
            )
            media_contents.append(media_content)
            self.stdout.write(self.style.SUCCESS(f'Created media content: {media_content.title}'))

        # 3. Create 3 rating scenarios
        # Scenario 1: Same user multiple ratings
        user1 = users[0]
        for i in range(3):
            media = random.choice(media_contents)
            # Ensure user1 doesn't rate the same media twice in this scenario
            if not Rating.objects.filter(user=user1, media_content=media).exists():
                Rating.objects.create(user=user1, media_content=media, value=random.randint(1, 5))
                self.stdout.write(self.style.SUCCESS(f'User {user1.email} rated {media.title}'))

        # Scenario 2: Multiple users one content
        content1 = media_contents[0]
        for user in users:
            if not Rating.objects.filter(user=user, media_content=content1).exists():
                Rating.objects.create(user=user, media_content=content1, value=random.randint(1, 5))
                self.stdout.write(self.style.SUCCESS(f'User {user.email} rated {content1.title}'))

        # Scenario 3: User rates multiple items (already covered by scenario 1 and 2, but adding more for variety)
        user2 = users[1]
        for i in range(2):
            media = random.choice(media_contents)
            if not Rating.objects.filter(user=user2, media_content=media).exists():
                Rating.objects.create(user=user2, media_content=media, value=random.randint(1, 5))
                self.stdout.write(self.style.SUCCESS(f'User {user2.email} rated {media.title}'))

        self.stdout.write(self.style.SUCCESS('Database seeding complete!'))
