from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.contrib.contenttypes.models import ContentType
from store.models import Product, Collection, Promotion, Review
from tags.models import Tag, TaggedItem
import random


class Command(BaseCommand):
    help = 'Seed the database with 200 realistic products in electronics, healthcare, and sports equipment'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding database...')
        
        # Clear existing data
        self.stdout.write('Clearing existing products, collections, reviews, and tags...')
        Review.objects.all().delete()
        TaggedItem.objects.all().delete()
        Tag.objects.all().delete()
        Product.objects.all().delete()
        Collection.objects.all().delete()
        Promotion.objects.all().delete()
        
        # Create promotions
        self.stdout.write('Creating promotions...')
        promotions = []
        promotion_data = [
            ('Summer Sale', 10.0),
            ('Black Friday', 25.0),
            ('Clearance', 50.0),
            ('New Year Sale', 15.0),
            ('Flash Sale', 30.0),
            ('Holiday Special', 20.0),
            ('Weekend Deal', 12.0),
        ]
        
        for desc, discount in promotion_data:
            promo = Promotion.objects.create(
                description=desc,
                discount=discount
            )
            promotions.append(promo)
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(promotions)} promotions'))
        
        # Create collections
        self.stdout.write('Creating collections...')
        collections_dict = {}
        collection_names = [
            'Smartphones', 'Laptops', 'Tablets', 'Audio & Headphones', 'Cameras',
            'Gaming Consoles', 'Smart Home', 'Wearable Technology', 'Computer Accessories',
            'Monitors & Displays', 'Networking', 'Storage Devices',
            'Vitamins & Supplements', 'First Aid', 'Personal Care', 'Medical Devices',
            'Fitness Trackers', 'Pain Relief', 'Skincare', 'Oral Care',
            'Fitness Equipment', 'Yoga & Pilates', 'Running Gear', 'Cycling',
            'Camping & Hiking', 'Water Sports', 'Team Sports', 'Golf',
            'Tennis & Racquet Sports', 'Winter Sports', 'Outdoor Recreation',
            'Men\'s Clothing', 'Women\'s Clothing', 'Shoes', 'Accessories'
        ]
        
        for name in collection_names:
            collection = Collection.objects.create(
                title=name,
                featured_product=None
            )
            collections_dict[name] = collection
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(collections_dict)} collections'))
        
        # Define realistic products
        products_data = [
            # ELECTRONICS - Smartphones (15 products)
            ('iPhone 15 Pro Max', 'Apple flagship smartphone with A17 Pro chip, titanium design, 6.7" Super Retina XDR display, and advanced camera system with 5x optical zoom', 1199.99, 'Smartphones'),
            ('Samsung Galaxy S24 Ultra', 'Premium Android phone with S Pen, 200MP camera, AI features, and stunning 6.8" Dynamic AMOLED display', 1299.99, 'Smartphones'),
            ('Google Pixel 8 Pro', 'Google\'s flagship with advanced AI photography, Magic Eraser, pure Android experience, and Tensor G3 chip', 999.99, 'Smartphones'),
            ('OnePlus 12', 'Flagship killer with Snapdragon 8 Gen 3, 100W fast charging, and Hasselblad camera system', 799.99, 'Smartphones'),
            ('Xiaomi 14 Pro', 'High-performance smartphone with Leica cameras, 120W HyperCharge, and premium build quality', 899.99, 'Smartphones'),
            ('iPhone 14', 'Reliable Apple smartphone with A15 Bionic chip, dual camera system, and all-day battery life', 799.99, 'Smartphones'),
            ('Samsung Galaxy A54', 'Mid-range phone with excellent camera, 5G connectivity, and long-lasting battery', 449.99, 'Smartphones'),
            ('Google Pixel 7a', 'Budget-friendly Pixel with great camera, clean Android, and Tensor G2 processor', 499.99, 'Smartphones'),
            ('Motorola Edge 40', 'Curved display smartphone with 144Hz refresh rate and premium design', 599.99, 'Smartphones'),
            ('Nothing Phone 2', 'Unique transparent design with Glyph Interface and flagship performance', 699.99, 'Smartphones'),
            ('ASUS ROG Phone 7', 'Gaming smartphone with 165Hz display, advanced cooling, and gaming triggers', 999.99, 'Smartphones'),
            ('Sony Xperia 1 V', 'Professional camera phone with 4K HDR OLED display and advanced photography features', 1399.99, 'Smartphones'),
            ('Oppo Find X6 Pro', 'Flagship with Hasselblad cameras, 100W charging, and stunning curved display', 1099.99, 'Smartphones'),
            ('Realme GT 3', 'Fast-charging champion with 240W charging and Snapdragon 8+ Gen 1', 649.99, 'Smartphones'),
            ('Vivo X90 Pro', 'Photography-focused flagship with Zeiss optics and advanced image processing', 899.99, 'Smartphones'),
            
            # ELECTRONICS - Laptops (15 products)
            ('MacBook Pro 16-inch M3 Max', 'Apple\'s most powerful laptop with M3 Max chip, stunning Liquid Retina XDR display, and up to 22 hours battery life', 2499.99, 'Laptops'),
            ('Dell XPS 15', 'Premium Windows laptop with stunning OLED display, Intel Core i7, and sleek aluminum design', 1799.99, 'Laptops'),
            ('Lenovo ThinkPad X1 Carbon Gen 11', 'Business ultrabook with legendary keyboard, military-grade durability, and all-day battery', 1599.99, 'Laptops'),
            ('ASUS ROG Zephyrus G14', 'Compact gaming laptop with AMD Ryzen 9, RTX 4070, and AniMe Matrix display', 1899.99, 'Laptops'),
            ('HP Spectre x360', 'Convertible laptop with 2-in-1 design, OLED touchscreen, and premium gem-cut design', 1399.99, 'Laptops'),
            ('Microsoft Surface Laptop 5', 'Sleek laptop with PixelSense touchscreen, premium Alcantara keyboard, and Windows 11', 1299.99, 'Laptops'),
            ('Acer Swift 3', 'Budget-friendly ultrabook with solid performance, lightweight design, and great value', 699.99, 'Laptops'),
            ('MacBook Air M2', 'Thin and light laptop with M2 chip, fanless design, and stunning Retina display', 1199.99, 'Laptops'),
            ('Razer Blade 15', 'Premium gaming laptop with RTX 4080, 240Hz display, and CNC aluminum chassis', 2399.99, 'Laptops'),
            ('LG Gram 17', 'Ultra-lightweight 17-inch laptop weighing just 2.98 lbs with all-day battery', 1699.99, 'Laptops'),
            ('MSI Creator Z16', 'Content creation laptop with QHD+ display, RTX graphics, and creator-focused features', 1999.99, 'Laptops'),
            ('Framework Laptop', 'Modular and repairable laptop with upgradeable components and sustainable design', 1049.99, 'Laptops'),
            ('ASUS ZenBook 14', 'Compact ultrabook with OLED display, NumberPad, and premium build quality', 899.99, 'Laptops'),
            ('Gigabyte Aero 16', 'Creative professional laptop with 4K OLED, RTX 4070, and color-accurate display', 2199.99, 'Laptops'),
            ('HP Envy x360', 'Versatile 2-in-1 laptop with AMD Ryzen processor and active pen support', 899.99, 'Laptops'),
            
            # ELECTRONICS - Audio & Headphones (12 products)
            ('Sony WH-1000XM5', 'Industry-leading noise cancelling headphones with exceptional sound quality and 30-hour battery', 399.99, 'Audio & Headphones'),
            ('Apple AirPods Pro 2', 'Premium wireless earbuds with spatial audio, adaptive transparency, and MagSafe charging', 249.99, 'Audio & Headphones'),
            ('Bose QuietComfort Ultra', 'Premium noise cancelling headphones with immersive audio and luxurious comfort', 429.99, 'Audio & Headphones'),
            ('Sennheiser Momentum 4', 'Audiophile-grade wireless headphones with 60-hour battery and exceptional sound', 379.99, 'Audio & Headphones'),
            ('JBL Flip 6', 'Portable Bluetooth speaker with powerful sound, waterproof design, and 12-hour playtime', 129.99, 'Audio & Headphones'),
            ('Beats Studio Pro', 'Stylish headphones with spatial audio, lossless audio, and premium design', 349.99, 'Audio & Headphones'),
            ('Anker Soundcore Liberty 4', 'Budget wireless earbuds with great sound, ANC, and long battery life', 99.99, 'Audio & Headphones'),
            ('Samsung Galaxy Buds 2 Pro', 'Premium earbuds with intelligent ANC, 360 audio, and seamless Samsung integration', 229.99, 'Audio & Headphones'),
            ('Jabra Elite 85t', 'Advanced ANC earbuds with adjustable sound, multipoint connectivity, and great calls', 229.99, 'Audio & Headphones'),
            ('Audio-Technica ATH-M50xBT2', 'Professional studio headphones with Bluetooth, exceptional sound quality', 199.99, 'Audio & Headphones'),
            ('Marshall Emberton II', 'Portable speaker with iconic design, 30-hour battery, and powerful sound', 169.99, 'Audio & Headphones'),
            ('Shure AONIC 50', 'Premium wireless headphones with studio-quality sound and adjustable noise cancellation', 299.99, 'Audio & Headphones'),
            
            # ELECTRONICS - Tablets & Wearables (10 products)
            ('iPad Pro 12.9-inch M2', 'Apple\'s most powerful tablet with M2 chip, Liquid Retina XDR display, and Apple Pencil support', 1099.99, 'Tablets'),
            ('Samsung Galaxy Tab S9 Ultra', 'Premium Android tablet with massive 14.6" AMOLED display, S Pen included, and desktop mode', 1199.99, 'Tablets'),
            ('iPad Air M2', 'Versatile tablet with M2 chip, 10.9" Liquid Retina display, and Apple Pencil support', 599.99, 'Tablets'),
            ('Microsoft Surface Pro 9', '2-in-1 tablet with Intel Core i7, detachable keyboard, and Windows 11', 999.99, 'Tablets'),
            ('Apple Watch Series 9', 'Advanced smartwatch with health tracking, always-on display, and ECG capability', 429.99, 'Wearable Technology'),
            ('Samsung Galaxy Watch 6', 'Feature-rich Android smartwatch with advanced health sensors and Wear OS', 349.99, 'Wearable Technology'),
            ('Garmin Fenix 7', 'Premium multisport GPS watch with advanced training features and rugged design', 699.99, 'Wearable Technology'),
            ('Fitbit Charge 6', 'Fitness tracker with heart rate monitoring, GPS, and 7-day battery life', 159.99, 'Wearable Technology'),
            ('Kindle Paperwhite', 'E-reader with adjustable warm light, waterproof design, and weeks of battery life', 139.99, 'Tablets'),
            ('Oura Ring Gen 3', 'Smart ring with sleep tracking, activity monitoring, and health insights', 299.99, 'Wearable Technology'),
            
            # ELECTRONICS - Cameras & Gaming (10 products)
            ('Sony A7 IV', 'Full-frame mirrorless camera with 33MP sensor, 4K 60p video, and advanced autofocus', 2499.99, 'Cameras'),
            ('Canon EOS R6 Mark II', 'Versatile full-frame camera with excellent autofocus, 6K video, and IBIS', 2399.99, 'Cameras'),
            ('DJI Mini 4 Pro', 'Compact drone with 4K camera, obstacle avoidance, and 34-minute flight time', 759.99, 'Cameras'),
            ('GoPro Hero 12 Black', 'Action camera with 5.3K video, HyperSmooth stabilization, and waterproof design', 399.99, 'Cameras'),
            ('Fujifilm X-T5', 'Retro-styled mirrorless camera with 40MP sensor and film simulation modes', 1699.99, 'Cameras'),
            ('PlayStation 5', 'Sony\'s latest gaming console with 4K gaming, ray tracing, and ultra-fast SSD', 499.99, 'Gaming Consoles'),
            ('Xbox Series X', 'Microsoft\'s powerful gaming console with 4K 120fps gaming and Game Pass', 499.99, 'Gaming Consoles'),
            ('Nintendo Switch OLED', 'Hybrid gaming console with vibrant OLED screen and exclusive Nintendo games', 349.99, 'Gaming Consoles'),
            ('Steam Deck', 'Portable PC gaming handheld with full Steam library access', 649.99, 'Gaming Consoles'),
            ('Meta Quest 3', 'Advanced VR headset with mixed reality, high-resolution displays, and wireless freedom', 499.99, 'Gaming Consoles'),
            
            # ELECTRONICS - Smart Home & Accessories (10 products)
            ('Amazon Echo Dot 5th Gen', 'Smart speaker with Alexa, improved sound, and smart home control', 49.99, 'Smart Home'),
            ('Google Nest Hub 2nd Gen', 'Smart display with Google Assistant, sleep tracking, and home control', 99.99, 'Smart Home'),
            ('Ring Video Doorbell Pro 2', 'Smart doorbell with HD video, 3D motion detection, and two-way talk', 249.99, 'Smart Home'),
            ('Philips Hue Starter Kit', 'Smart LED lighting system with color changing and app control', 199.99, 'Smart Home'),
            ('Logitech MX Master 3S', 'Premium wireless mouse with ergonomic design and multi-device support', 99.99, 'Computer Accessories'),
            ('Keychron K8 Pro', 'Wireless mechanical keyboard with hot-swappable switches and Mac/Windows support', 109.99, 'Computer Accessories'),
            ('Dell UltraSharp U2723DE', '27-inch QHD monitor with USB-C hub and excellent color accuracy', 599.99, 'Monitors & Displays'),
            ('LG UltraGear 27GN950', '4K 144Hz gaming monitor with Nano IPS and G-Sync support', 799.99, 'Monitors & Displays'),
            ('Samsung T7 Portable SSD 2TB', 'Fast external SSD with USB 3.2 Gen 2 and compact design', 199.99, 'Storage Devices'),
            ('TP-Link Deco X55', 'Mesh WiFi 6 system with whole-home coverage and easy setup', 229.99, 'Networking'),
            
            # HEALTHCARE - Vitamins & Supplements (15 products)
            ('Nature Made Multivitamin', 'Complete daily multivitamin with essential nutrients for overall health', 24.99, 'Vitamins & Supplements'),
            ('Optimum Nutrition Whey Protein', 'Gold standard whey protein powder for muscle recovery and growth', 59.99, 'Vitamins & Supplements'),
            ('Nordic Naturals Omega-3', 'High-quality fish oil supplement for heart and brain health', 39.99, 'Vitamins & Supplements'),
            ('Garden of Life Probiotics', 'Raw probiotics with 85 billion CFU for digestive and immune health', 44.99, 'Vitamins & Supplements'),
            ('NOW Foods Vitamin D3', 'High-potency vitamin D3 for bone health and immune support', 14.99, 'Vitamins & Supplements'),
            ('Thorne Research Multivitamin Elite', 'Premium multivitamin for active individuals with bioavailable nutrients', 49.99, 'Vitamins & Supplements'),
            ('Vital Proteins Collagen Peptides', 'Grass-fed collagen powder for skin, hair, and joint health', 43.99, 'Vitamins & Supplements'),
            ('Magnesium Glycinate 400mg', 'Highly absorbable magnesium for sleep, relaxation, and muscle function', 19.99, 'Vitamins & Supplements'),
            ('Turmeric Curcumin with BioPerine', 'Anti-inflammatory supplement with enhanced absorption', 24.99, 'Vitamins & Supplements'),
            ('Ashwagandha KSM-66', 'Adaptogenic herb for stress relief and energy support', 22.99, 'Vitamins & Supplements'),
            ('Vitamin C 1000mg', 'Immune-boosting vitamin C with rose hips', 16.99, 'Vitamins & Supplements'),
            ('B-Complex Plus', 'Complete B-vitamin complex for energy and nervous system support', 18.99, 'Vitamins & Supplements'),
            ('Zinc 50mg', 'Essential mineral for immune function and wound healing', 12.99, 'Vitamins & Supplements'),
            ('CoQ10 200mg', 'Antioxidant supplement for heart health and cellular energy', 34.99, 'Vitamins & Supplements'),
            ('Melatonin 10mg', 'Natural sleep aid for better rest and circadian rhythm support', 9.99, 'Vitamins & Supplements'),
            
            # HEALTHCARE - Personal Care & Medical (15 products)
            ('Oral-B iO Series 9', 'Premium electric toothbrush with AI tracking and pressure sensor', 299.99, 'Oral Care'),
            ('Philips Sonicare DiamondClean', 'Sonic electric toothbrush with multiple cleaning modes', 229.99, 'Oral Care'),
            ('Waterpik Aquarius', 'Water flosser for superior plaque removal and gum health', 79.99, 'Oral Care'),
            ('CeraVe Moisturizing Cream', 'Dermatologist-recommended face and body moisturizer with ceramides', 18.99, 'Skincare'),
            ('La Roche-Posay Anthelios Sunscreen', 'Broad-spectrum SPF 60 sunscreen for sensitive skin', 34.99, 'Skincare'),
            ('The Ordinary Niacinamide 10%', 'Affordable serum for blemishes and pore refinement', 12.99, 'Skincare'),
            ('Neutrogena Hydro Boost', 'Hyaluronic acid gel cream for intense hydration', 19.99, 'Skincare'),
            ('Omron Blood Pressure Monitor', 'Clinically accurate upper arm blood pressure monitor', 79.99, 'Medical Devices'),
            ('Withings Body+ Smart Scale', 'WiFi body composition scale with app sync', 99.99, 'Medical Devices'),
            ('iHealth Thermometer', 'No-touch forehead thermometer with instant readings', 39.99, 'Medical Devices'),
            ('First Aid Only Kit', 'Comprehensive 298-piece first aid kit for home and office', 29.99, 'First Aid'),
            ('Advil Pain Relief', 'Ibuprofen tablets for pain relief and fever reduction', 14.99, 'Pain Relief'),
            ('Tylenol Extra Strength', 'Acetaminophen for effective pain and fever relief', 12.99, 'Pain Relief'),
            ('Biofreeze Pain Relief Gel', 'Topical analgesic for muscle and joint pain', 16.99, 'Pain Relief'),
            ('Dove Deep Moisture Body Wash', 'Nourishing body wash with moisturizing cream', 8.99, 'Personal Care'),
            
            # SPORTS EQUIPMENT - Fitness (20 products)
            ('Bowflex SelectTech Dumbbells', 'Adjustable dumbbells from 5-52.5 lbs with easy dial system', 399.99, 'Fitness Equipment'),
            ('Peloton Bike+', 'Premium indoor cycling bike with live and on-demand classes', 2495.00, 'Fitness Equipment'),
            ('NordicTrack Treadmill', 'Commercial-grade treadmill with iFit integration and incline training', 1999.99, 'Fitness Equipment'),
            ('Concept2 Model D Rower', 'Professional rowing machine used by Olympic athletes', 1095.00, 'Fitness Equipment'),
            ('TRX Suspension Trainer', 'Bodyweight training system for full-body workouts', 179.99, 'Fitness Equipment'),
            ('Rogue Fitness Barbell', 'Olympic barbell for weightlifting and CrossFit', 325.00, 'Fitness Equipment'),
            ('Manduka PRO Yoga Mat', 'Premium yoga mat with lifetime guarantee and superior cushioning', 120.00, 'Yoga & Pilates'),
            ('Gaiam Yoga Block Set', 'Supportive foam blocks for yoga practice', 14.99, 'Yoga & Pilates'),
            ('Liforme Yoga Mat', 'Eco-friendly yoga mat with alignment markers', 139.99, 'Yoga & Pilates'),
            ('Balanced Body Reformer', 'Professional Pilates reformer for studio-quality workouts', 3995.00, 'Yoga & Pilates'),
            ('Nike Air Zoom Pegasus 40', 'Versatile running shoes with responsive cushioning', 129.99, 'Running Gear'),
            ('Garmin Forerunner 265', 'Advanced GPS running watch with AMOLED display', 449.99, 'Running Gear'),
            ('Aftershokz Aeropex', 'Bone conduction headphones for safe running', 159.99, 'Running Gear'),
            ('FlipBelt Running Belt', 'Tubular running belt for phone and essentials', 34.99, 'Running Gear'),
            ('Trek Domane SL 6', 'Endurance road bike with carbon frame and smooth ride', 3999.99, 'Cycling'),
            ('Specialized Turbo Vado', 'Electric bike for commuting and recreation', 3500.00, 'Cycling'),
            ('Giro Syntax MIPS Helmet', 'Road cycling helmet with MIPS protection', 149.99, 'Cycling'),
            ('Shimano SPD Pedals', 'Clipless pedals for road and mountain biking', 79.99, 'Cycling'),
            ('Osprey Talon 22 Backpack', 'Lightweight hiking backpack with ventilated back panel', 129.99, 'Camping & Hiking'),
            ('REI Co-op Half Dome Tent', '2-person backpacking tent with easy setup', 199.99, 'Camping & Hiking'),
            
            # SPORTS EQUIPMENT - Outdoor & Team Sports (15 products)
            ('The North Face Sleeping Bag', '20°F down sleeping bag for cold-weather camping', 299.99, 'Camping & Hiking'),
            ('MSR PocketRocket Stove', 'Ultralight backpacking stove for outdoor cooking', 49.99, 'Camping & Hiking'),
            ('Hydro Flask Water Bottle', 'Insulated stainless steel water bottle keeps drinks cold 24 hours', 44.99, 'Outdoor Recreation'),
            ('Yeti Cooler Tundra 45', 'Rotomolded cooler with superior ice retention', 325.00, 'Outdoor Recreation'),
            ('Coleman Camping Chair', 'Portable folding chair with cup holder', 29.99, 'Outdoor Recreation'),
            ('O\'Neill Wetsuit', 'Full wetsuit for surfing and water sports', 189.99, 'Water Sports'),
            ('BIC Sport Kayak', 'Recreational kayak for lakes and calm waters', 599.99, 'Water Sports'),
            ('Speedo Fastskin Swimsuit', 'Competition swimsuit for racing', 89.99, 'Water Sports'),
            ('Wilson Evolution Basketball', 'Official size indoor basketball with microfiber composite', 64.99, 'Team Sports'),
            ('Spalding NBA Basketball Hoop', 'Adjustable portable basketball system', 399.99, 'Team Sports'),
            ('Adidas Tango Soccer Ball', 'FIFA-quality soccer ball for matches', 39.99, 'Team Sports'),
            ('Rawlings Baseball Glove', 'Premium leather baseball glove for infield', 149.99, 'Team Sports'),
            ('Callaway Golf Club Set', 'Complete golf club set for beginners', 599.99, 'Golf'),
            ('TaylorMade Driver', 'High-performance driver for distance and accuracy', 499.99, 'Golf'),
            ('Wilson Tennis Racket', 'Professional tennis racket with power and control', 189.99, 'Tennis & Racquet Sports'),
            
            # FASHION - Clothing & Shoes (18 products)
            ('Levi\'s 501 Original Jeans', 'Classic straight-fit denim jeans with button fly', 69.99, 'Men\'s Clothing'),
            ('Nike Dri-FIT T-Shirt', 'Performance athletic t-shirt with moisture-wicking technology', 29.99, 'Men\'s Clothing'),
            ('Adidas Originals Hoodie', 'Classic pullover hoodie with trefoil logo', 79.99, 'Men\'s Clothing'),
            ('Patagonia Down Jacket', 'Lightweight insulated jacket with recycled materials', 279.99, 'Men\'s Clothing'),
            ('Lululemon Align Leggings', 'High-waist yoga leggings with buttery-soft Nulu fabric', 98.99, 'Women\'s Clothing'),
            ('Athleta Salutation Joggers', 'Comfortable athleisure joggers with pockets', 89.99, 'Women\'s Clothing'),
            ('Free People Boho Blouse', 'Flowy bohemian-style blouse with embroidery', 88.99, 'Women\'s Clothing'),
            ('Everlane Cashmere Sweater', 'Luxurious 100% cashmere crew neck sweater', 149.99, 'Women\'s Clothing'),
            ('Nike Air Force 1', 'Iconic basketball-inspired sneakers with classic design', 110.99, 'Shoes'),
            ('Adidas Ultraboost 22', 'Premium running shoes with Boost cushioning technology', 189.99, 'Shoes'),
            ('Converse Chuck Taylor All Star', 'Classic canvas high-top sneakers', 59.99, 'Shoes'),
            ('Dr. Martens 1460 Boots', 'Iconic leather ankle boots with air-cushioned sole', 169.99, 'Shoes'),
            ('Birkenstock Arizona Sandals', 'Comfortable two-strap sandals with cork footbed', 99.99, 'Shoes'),
            ('Allbirds Wool Runners', 'Sustainable merino wool sneakers with carbon-neutral production', 98.99, 'Shoes'),
            ('Timberland 6-Inch Boots', 'Classic waterproof work boots with premium leather', 189.99, 'Shoes'),
            ('ASICS Gel-Kayano 30', 'Stability running shoes for long distances and overpronation', 159.99, 'Shoes'),
            ('Hoka Clifton 9', 'Maximalist cushioned running shoes for comfort', 144.99, 'Shoes'),
            ('On Cloud 5', 'Swiss-engineered running shoes with CloudTec cushioning', 139.99, 'Shoes'),
        ]
        
        # Create products
        self.stdout.write('Creating products...')
        products = []
        
        for title, description, price, collection_name in products_data:
            product = Product.objects.create(
                title=title,
                slug=slugify(title),
                description=description,
                unit_price=price,
                inventory=random.randint(15, 100),
                collection=collections_dict[collection_name]
            )
            
            # Add random promotions (0-2 promotions per product)
            num_promotions = random.randint(0, 2)
            if num_promotions > 0:
                selected_promotions = random.sample(promotions, num_promotions)
                product.promotions.set(selected_promotions)
            
            products.append(product)
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(products)} products'))
        
        # Set featured products for collections
        self.stdout.write('Setting featured products for collections...')
        for collection in collections_dict.values():
            collection_products = Product.objects.filter(collection=collection)
            if collection_products.exists():
                collection.featured_product = random.choice(collection_products)
                collection.save()
        
        # Create tags
        self.stdout.write('Creating tags...')
        tag_labels = [
            'New Arrival', 'Best Seller', 'Trending', 'Limited Edition', 'Premium Quality',
            'Eco-Friendly', 'Sale', 'Featured', 'Top Rated', 'Award Winner',
            'Professional Grade', 'Budget-Friendly', 'Wireless', 'Waterproof', 'Portable',
            'Durable', 'Lightweight', 'High Performance', 'Smart', 'Innovative',
            'Comfortable', 'Stylish', 'Versatile', 'Essential', 'Popular',
            'Recommended', 'Advanced', 'Beginner Friendly', 'Compact', 'Fast Shipping'
        ]
        
        tags = []
        for label in tag_labels:
            tag = Tag.objects.create(label=label)
            tags.append(tag)
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(tags)} tags'))
        
        # Add tags to products
        self.stdout.write('Adding tags to products...')
        product_content_type = ContentType.objects.get_for_model(Product)
        product_tags_count = 0
        
        for product in products:
            num_tags = random.randint(2, 5)
            selected_tags = random.sample(tags, num_tags)
            
            for tag in selected_tags:
                TaggedItem.objects.create(
                    tag=tag,
                    content_type=product_content_type,
                    object_id=product.id
                )
                product_tags_count += 1
        
        self.stdout.write(self.style.SUCCESS(f'Added {product_tags_count} tags to products'))
        
        # Add tags to collections
        self.stdout.write('Adding tags to collections...')
        collection_content_type = ContentType.objects.get_for_model(Collection)
        collection_tags_count = 0
        
        for collection in collections_dict.values():
            num_tags = random.randint(1, 3)
            selected_tags = random.sample(tags, num_tags)
            
            for tag in selected_tags:
                TaggedItem.objects.create(
                    tag=tag,
                    content_type=collection_content_type,
                    object_id=collection.id
                )
                collection_tags_count += 1
        
        self.stdout.write(self.style.SUCCESS(f'Added {collection_tags_count} tags to collections'))
        
        # Create reviews for products
        self.stdout.write('Creating product reviews...')
        reviewer_names = [
            'Alex Thompson', 'Maria Garcia', 'James Wilson', 'Emma Davis', 'Ryan Martinez',
            'Olivia Brown', 'Liam Johnson', 'Sophia Anderson', 'Noah Taylor', 'Ava White',
            'Ethan Harris', 'Isabella Clark', 'Mason Lewis', 'Mia Robinson', 'Lucas Walker',
            'Charlotte Hall', 'Benjamin Allen', 'Amelia Young', 'Henry King', 'Harper Wright'
        ]
        
        review_templates = [
            "Absolutely love this {category}! {sentiment} Highly recommend to anyone looking for quality.",
            "Excellent {category}. {sentiment} Worth every penny and more.",
            "Very satisfied with this purchase. {sentiment} Will definitely buy again.",
            "Great {category} for the price. {sentiment} No complaints whatsoever.",
            "Impressive quality! {sentiment} Exceeded all my expectations.",
            "Solid {category}. {sentiment} Does exactly what it's supposed to do.",
            "Amazing product! {sentiment} Best purchase I've made this year.",
            "Perfect {category}! {sentiment} Couldn't be happier with this.",
            "Really good {category}. {sentiment} Would recommend to friends and family.",
            "Outstanding! {sentiment} This {category} is a game-changer.",
        ]
        
        sentiments = [
            "The quality is exceptional and build feels premium.",
            "Works flawlessly right out of the box.",
            "Exactly as described and pictured.",
            "Fast shipping and excellent packaging.",
            "Very durable and well-made construction.",
            "Easy to use with intuitive design.",
            "Great design and fantastic functionality.",
            "Perfect for my needs and lifestyle.",
            "Better than I expected in every way.",
            "Fantastic value for the money.",
            "Superior performance and reliability.",
            "Comfortable and fits perfectly.",
            "Stylish and practical at the same time.",
            "Innovative features that actually work.",
            "Long-lasting and built to last.",
        ]
        
        reviews = []
        for product in products:
            # Add 1-5 reviews per product
            num_reviews = random.randint(1, 5)
            
            # Determine category for review
            category = "product"
            if product.collection:
                category = product.collection.title.lower().rstrip('s')
            
            for _ in range(num_reviews):
                review = Review.objects.create(
                    product=product,
                    name=random.choice(reviewer_names),
                    description=random.choice(review_templates).format(
                        category=category,
                        sentiment=random.choice(sentiments)
                    )
                )
                reviews.append(review)
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(reviews)} product reviews'))
        
        # Final summary
        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS('Database seeding completed successfully!'))
        self.stdout.write(self.style.SUCCESS('='*60))
        self.stdout.write(self.style.SUCCESS(f'Summary:'))
        self.stdout.write(self.style.SUCCESS(f'  - {len(promotions)} promotions'))
        self.stdout.write(self.style.SUCCESS(f'  - {len(collections_dict)} collections'))
        self.stdout.write(self.style.SUCCESS(f'  - {len(products)} products'))
        self.stdout.write(self.style.SUCCESS(f'    • Electronics: ~100 products'))
        self.stdout.write(self.style.SUCCESS(f'    • Healthcare: ~30 products'))
        self.stdout.write(self.style.SUCCESS(f'    • Sports Equipment: ~35 products'))
        self.stdout.write(self.style.SUCCESS(f'    • Fashion: ~18 products'))
        self.stdout.write(self.style.SUCCESS(f'  - {len(tags)} tags'))
        self.stdout.write(self.style.SUCCESS(f'  - {product_tags_count} product tags'))
        self.stdout.write(self.style.SUCCESS(f'  - {collection_tags_count} collection tags'))
        self.stdout.write(self.style.SUCCESS(f'  - {len(reviews)} reviews'))
        self.stdout.write(self.style.SUCCESS('='*60 + '\n'))
