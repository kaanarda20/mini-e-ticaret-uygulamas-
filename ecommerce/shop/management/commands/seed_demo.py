from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from shop.models import Category, Product, ProductImage, ProductVariant
from django.core.files.base import ContentFile
import base64


SIMPLE_PNG_B64 = (
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR4nGNgYAAAAAMAAWgmWQ0AAAAASUVORK5CYII="
)


class Command(BaseCommand):
    help = 'Seed demo users and sample products (admin: admin/adminpass, demo: demo/demopass)'

    def handle(self, *args, **options):
        User = get_user_model()

        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'adminpass')
            self.stdout.write(self.style.SUCCESS('Created superuser: admin'))
        else:
            self.stdout.write('Superuser admin already exists')

        if not User.objects.filter(username='demo').exists():
            User.objects.create_user('demo', 'demo@example.com', 'demopass')
            self.stdout.write(self.style.SUCCESS('Created demo user: demo'))
        else:
            self.stdout.write('Demo user already exists')

        cats = []
        for name, slug in [('Kırtasiye', 'kirtasiye'), ('Aksesuar', 'aksesuar'), ('Elektronik', 'elektronik')]:
            c, _ = Category.objects.get_or_create(name=name, slug=slug)
            cats.append(c)

        products_spec = [
            ('Kurşun Kalem', 'Sert ve yumuşak seçenekleriyle kurşun kalem.', '2.50', 100, cats[0]),
            ('Çizgili Defter', '200 sayfa, çizgili defter.', '15.00', 50, cats[0]),
            ('Telefon Kabı', 'Şeffaf silikon telefon kabı.', '9.90', 30, cats[1]),
        ]

        for idx, (name, desc, price, stock, cat) in enumerate(products_spec, start=1):
            p, created = Product.objects.get_or_create(name=name, defaults={
                'description': desc,
                'price': price,
                'stock': stock,
                'category': cat,
            })
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created product: {p.name}'))
            else:
                self.stdout.write(f'Product exists: {p.name}')

            if not p.image:
                data = base64.b64decode(SIMPLE_PNG_B64)
                p.image.save(f'products/demo_{idx}.png', ContentFile(data), save=True)

            if not p.images.exists():
                data = base64.b64decode(SIMPLE_PNG_B64)
                img = ProductImage(product=p)
                img.image.save(f'products/demo_{idx}_g.png', ContentFile(data), save=True)
                img.alt = f'Demo image for {p.name}'
                img.save()

            if not p.variants.exists():
                v = ProductVariant.objects.create(product=p, name='Standart', sku=f'DEMO-{idx}', additional_price=0, stock=stock)
                self.stdout.write(self.style.SUCCESS(f'Added variant for {p.name}: {v.name}'))

        self.stdout.write(self.style.SUCCESS('Demo seeding complete.'))
