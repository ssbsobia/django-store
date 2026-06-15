import os
import random

from django.core.files import File
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from config import settings
from products.models import Brand, Category, Product


class Command(BaseCommand):
    help = 'Create 250+ dummy products using images from media/products/product_img/2026/06/03/'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=260,
            help='Number of dummy products to create',
        )

    def handle(self, *args, **options):
        count = options['count']
        media_dir = os.path.join(settings.MEDIA_ROOT, 'phonImg' )

        if not os.path.isdir(media_dir):
            self.stderr.write(self.style.ERROR(f'Media image directory not found: {media_dir}'))
            return

        image_files = [f for f in os.listdir(media_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]
        if not image_files:
            self.stderr.write(self.style.ERROR(f'No image files found in {media_dir}'))
            return

        brands = ['Samsung', 'Nokia', 'Infinix', 'Tecno', 'Apple', 'Xiaomi', 'Realme', 'Oppo', 'Vivo', 'Motorola']
        categories = ['Smartphones', 'Tablets', 'Laptops', 'Accessories', 'Wearables', 'Gaming', 'Home Electronics']
        colors = ['Black', 'White', 'Blue', 'Red', 'Green', 'Silver', 'Pink']
        ram_options = ['4GB', '6GB', '8GB', '12GB', '16GB']
        storage_options = ['64GB', '128GB', '256GB', '512GB']
        purchased_price_options = [random.randrange(5000, 50000) for _ in range(100)]
        featured_options = [True, False]

        created_brands = []
        for brand_name in brands:
            brand, _ = Brand.objects.get_or_create(
                name=brand_name,
                defaults={'slug': slugify(brand_name)}
            )
            created_brands.append(brand)

        created_categories = []
        for category_name in categories:
            category, _ = Category.objects.get_or_create(
                name=category_name,
                defaults={'slug': slugify(category_name)}
            )
            created_categories.append(category)

        existing_count = Product.objects.count()
        start_index = existing_count + 1
        created_count = 0

        for i in range(start_index, start_index + count):
            name = f'Dummy Product {i}'
            brand = random.choice(created_brands)
            category = random.choice(created_categories)
            price = random.randrange(9999, 99999) / 100
            discount_price = round(price * random.uniform(0.70, 0.95), 2)
            stock = random.randrange(10, 201)
            color = random.choice(colors)
            ram = random.choice(ram_options)
            storage = random.choice(storage_options)
            featured = random.choice(featured_options)

            purchased_price = random.choice(purchased_price_options)
            description = (
                f'This is a bulk generated dummy product. '
                f'Brand: {brand.name}, Category: {category.name}, Color: {color}, RAM: {ram}, Storage: {storage}. '
                'Use this product for testing and development.'
            )

            product = Product(
                name=name,
                brand=brand,
                category=category,
                price=price,
                discount_price=discount_price,
                description=description,
                stock=stock,
                ram=ram,
                storage=storage,
                color=color,
                purchased_price=purchased_price,
                is_available=True,
                featured=featured,
            )

            image_name = random.choice(image_files)
            image_path = os.path.join(media_dir, image_name)
            with open(image_path, 'rb') as image_file:
                product.image.save(image_name, File(image_file), save=False)

            product.save()
            created_count += 1

            if created_count % 50 == 0:
                self.stdout.write(self.style.SUCCESS(f'Created {created_count} products...'))

        self.stdout.write(self.style.SUCCESS(f'Successfully created {created_count} dummy products.'))
