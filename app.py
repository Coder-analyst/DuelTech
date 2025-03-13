from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import random
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Product categories
categories = {
    'laptops': {
        'name': 'Laptops',
        'icon': 'fas fa-laptop',
        'description': 'High-performance laptops for work and gaming'
    },
    'smartphones': {
        'name': 'Smartphones',
        'icon': 'fas fa-mobile-alt',
        'description': 'Latest smartphones with cutting-edge features'
    },
    'tablets': {
        'name': 'Tablets',
        'icon': 'fas fa-tablet-alt',
        'description': 'Versatile tablets for productivity and entertainment'
    },
    'cpus': {
        'name': 'CPUs & Processors',
        'icon': 'fas fa-microchip',
        'description': 'High-performance processors for gaming and workstations'
    },
    'gpus': {
        'name': 'Graphics Cards',
        'icon': 'fas fa-tv',
        'description': 'Powerful GPUs for gaming and content creation'
    },
    'storage': {
        'name': 'Storage Devices',
        'icon': 'fas fa-hdd',
        'description': 'SSDs, HDDs and portable storage solutions'
    },
    'monitors': {
        'name': 'Monitors & Displays',
        'icon': 'fas fa-desktop',
        'description': 'High-resolution monitors for productivity and gaming'
    },
    'peripherals': {
        'name': 'Peripherals',
        'icon': 'fas fa-keyboard',
        'description': 'Keyboards, mice, and other input devices'
    },
    'audio': {
        'name': 'Audio',
        'icon': 'fas fa-headphones',
        'description': 'Premium headphones, speakers and audio equipment'
    },
    'networking': {
        'name': 'Networking',
        'icon': 'fas fa-network-wired',
        'description': 'Routers, switches and networking equipment'
    },
    'components': {
        'name': 'PC Components',
        'icon': 'fas fa-memory',
        'description': 'Motherboards, RAM, and other PC components'
    },
    'accessories': {
        'name': 'Accessories',
        'icon': 'fas fa-plug',
        'description': 'Cables, adapters, and other tech accessories'
    }
}

# Sample products data
products = {category: [] for category in categories}

def generate_more_products():
    # Product characteristics by category
    product_names = {
        'laptops': ['XPS', 'ThinkPad', 'MacBook Pro', 'ROG Zephyrus', 'Predator', 'Surface Laptop', 'Gram', 'Envy', 'Pavilion', 'Swift'],
        'smartphones': ['iPhone Pro', 'Galaxy S Ultra', 'Pixel Pro', 'OnePlus', 'Mi', 'ROG Phone', 'Find X', 'Edge', 'Xperia', 'Nothing'],
        'tablets': ['iPad Pro', 'Galaxy Tab S', 'Surface Pro', 'MatePad Pro', 'Mi Pad', 'ROG Flow Z', 'Yoga Tab', 'Nova', 'Nexus', 'Shield'],
        'cpus': ['Ryzen 9', 'Core i9', 'Threadripper', 'Core i7', 'Ryzen 7', 'Core i5', 'Ryzen 5', 'Xeon', 'EPYC', 'M2 Pro'],
        'gpus': ['RTX 4090', 'RTX 4080', 'RX 7900 XTX', 'RTX 4070', 'RX 7800 XT', 'RTX 4060', 'RX 7600', 'Arc A770', 'Quadro RTX'],
        'storage': ['980 Pro', 'FireCuda', 'WD Black', 'MP600', 'SN850', 'Barracuda', 'Crucial P5', 'XPG', 'Rocket 4', 'IronWolf'],
        'monitors': ['Odyssey', 'Predator', 'UltraGear', 'ProArt', 'Nitro', 'Alienware', 'Swift', 'ROG Swift', 'ViewSonic', 'BenQ'],
        'peripherals': ['MX Master', 'G Pro', 'BlackWidow', 'Huntsman', 'SteelSeries Apex', 'Corsair K', 'HyperX Alloy', 'Viper'],
        'audio': ['AirPods Pro', 'Galaxy Buds', 'WH-1000XM', 'QuietComfort', 'HD 660', 'Momentum', 'Liberty', 'FreeBuds'],
        'networking': ['Nighthawk', 'ROG Rapture', 'Deco', 'Orbi', 'UniFi', 'Archer', 'Velop', 'Nova'],
        'components': ['ROG Strix', 'MPG', 'TUF Gaming', 'Aorus', 'Vengeance', 'Trident Z', 'Ripjaws', 'Fury'],
        'accessories': ['MagSafe', 'Galaxy Charger', 'ThunderBolt', 'USB-C Hub', 'PowerCore', 'HDMI Adapter', 'Laptop Stand', 'Cooling Pad']
    }

    brands = {
        'laptops': ['Apple', 'Dell', 'Lenovo', 'ASUS', 'Acer', 'HP', 'LG', 'Microsoft', 'MSI', 'Razer'],
        'smartphones': ['Apple', 'Samsung', 'Google', 'OnePlus', 'Xiaomi', 'ASUS', 'OPPO', 'Motorola', 'Sony', 'Nothing'],
        'tablets': ['Apple', 'Samsung', 'Microsoft', 'Huawei', 'Xiaomi', 'ASUS', 'Lenovo', 'Amazon', 'Google', 'NVIDIA'],
        'cpus': ['AMD', 'Intel', 'Apple'],
        'gpus': ['NVIDIA', 'AMD', 'Intel', 'ASUS', 'MSI', 'Gigabyte', 'EVGA', 'Sapphire', 'PowerColor', 'XFX'],
        'storage': ['Samsung', 'Seagate', 'Western Digital', 'Corsair', 'SanDisk', 'Crucial', 'Kingston', 'ADATA', 'Sabrent', 'Toshiba'],
        'monitors': ['Samsung', 'LG', 'ASUS', 'Acer', 'Dell', 'Alienware', 'BenQ', 'MSI', 'ViewSonic', 'AOC'],
        'peripherals': ['Logitech', 'Razer', 'Corsair', 'SteelSeries', 'HyperX', 'Glorious', 'Ducky', 'Keychron'],
        'audio': ['Apple', 'Samsung', 'Sony', 'Bose', 'Sennheiser', 'JBL', 'Audio-Technica', 'Anker'],
        'networking': ['NETGEAR', 'ASUS', 'TP-Link', 'Ubiquiti', 'Linksys', 'D-Link', 'Cisco', 'Google'],
        'components': ['ASUS', 'MSI', 'Gigabyte', 'Corsair', 'G.SKILL', 'Kingston', 'NZXT', 'be quiet!'],
        'accessories': ['Apple', 'Samsung', 'Anker', 'Belkin', 'Logitech', 'Microsoft', 'UGREEN', 'Satechi']
    }
    
    # Generate products for each category
    for category in categories:
        for i in range(20):  # 20 products per category = 240+ products total
            model = random.choice(product_names[category])
            brand = random.choice(brands.get(category, brands['laptops']))  # Default to laptop brands if not specified
            
            # Price ranges for different categories
            if category in ['laptops', 'gpus']:
                price = random.randint(50000, 300000)
            elif category in ['smartphones', 'tablets', 'monitors']:
                price = random.randint(20000, 150000)
            elif category in ['cpus', 'components', 'audio']:
                price = random.randint(15000, 100000)
            else:
                price = random.randint(2000, 25000)
                
            rating = round(random.uniform(3.5, 5.0), 1)
            
            product = {
                'id': f'{category}{i+1}',
                'name': f'{brand} {model} {random.choice(["Pro", "Ultra", "X", "Max", "Elite", "Plus", str(random.randint(1, 15))])}',
                'price': f'₹{price:,}',
                'rating': rating,
                'brand': brand,
                'specs': generate_specs(category)
            }
            products[category].append(product)

def generate_specs(category):
    specs = {}
    
    if category == 'laptops':
        specs = {
            'processor': random.choice(['Intel i7', 'Intel i9', 'AMD Ryzen 7', 'AMD Ryzen 9', 'Apple M1', 'Apple M2']),
            'ram': f'{random.choice([8, 16, 32, 64])}GB',
            'storage': f'{random.choice([256, 512, 1024, 2048])}GB SSD',
            'display': f'{random.choice([13.3, 14, 15.6, 16])}inch {random.choice(["FHD", "4K", "QHD"])}',
            'battery': f'Up to {random.randint(8, 24)} hours'
        }
    elif category == 'smartphones':
        specs = {
            'processor': random.choice(['A16 Bionic', 'Snapdragon 8 Gen 2', 'Tensor G2', 'Dimensity 9000', 'Exynos 2200']),
            'ram': f'{random.choice([6, 8, 12, 16])}GB',
            'storage': f'{random.choice([128, 256, 512, 1024])}GB',
            'display': f'{random.choice([6.1, 6.4, 6.7, 6.9])}inch {random.choice(["OLED", "AMOLED", "IPS"])}',
            'battery': f'{random.randint(3500, 5500)}mAh'
        }
    elif category == 'tablets':
        specs = {
            'processor': random.choice(['A14 Bionic', 'Snapdragon 870', 'Tensor G1', 'Dimensity 1300', 'Snapdragon 8cx']),
            'ram': f'{random.choice([4, 6, 8, 12])}GB',
            'storage': f'{random.choice([64, 128, 256, 512])}GB',
            'display': f'{random.choice([8.3, 10.9, 11, 12.9])}inch {random.choice(["IPS", "OLED", "Mini-LED"])}',
            'battery': f'Up to {random.randint(8, 15)} hours'
        }
    elif category == 'cpus':
        specs = {
            'cores': f'{random.choice([4, 6, 8, 12, 16, 24, 32])} cores',
            'threads': f'{random.choice([8, 12, 16, 24, 32, 48, 64])} threads',
            'base_clock': f'{round(random.uniform(2.5, 4.0), 1)}GHz',
            'boost_clock': f'{round(random.uniform(4.0, 5.5), 1)}GHz',
            'tdp': f'{random.choice([65, 95, 105, 125, 150, 170])}W'
        }
    elif category == 'gpus':
        specs = {
            'memory': f'{random.choice([8, 10, 12, 16, 24])}GB {random.choice(["GDDR6", "GDDR6X", "HBM2e"])}',
            'cuda_cores': f'{random.randint(3000, 16000)}',
            'boost_clock': f'{round(random.uniform(1.5, 3.0), 2)}GHz',
            'tdp': f'{random.choice([150, 200, 250, 300, 350, 400])}W',
            'psu_recommendation': f'{random.choice([550, 650, 750, 850, 1000])}W'
        }
    elif category == 'storage':
        specs = {
            'capacity': f'{random.choice([250, 500, 1000, 2000, 4000, 8000])}GB',
            'interface': random.choice(['PCIe 4.0', 'PCIe 3.0', 'SATA III', 'USB 3.2', 'Thunderbolt 3']),
            'read_speed': f'{random.randint(500, 7000)}MB/s',
            'write_speed': f'{random.randint(500, 6000)}MB/s',
            'durability': f'{random.randint(300, 1800)}TBW'
        }
    else:
        # Default specs for other categories
        specs = {
            'feature1': random.choice(['Premium', 'Standard', 'Ultra', 'Pro', 'Elite']),
            'feature2': random.choice(['Wireless', 'Wired', 'Bluetooth 5.2', 'RGB', 'Compact']),
            'feature3': random.choice(['2023 Model', '2022 Model', 'Latest Gen', '2nd Gen', '3rd Gen']),
            'warranty': f'{random.choice([1, 2, 3, 5])} years'
        }
    
    return specs

# Generate the additional products
generate_more_products()

@app.route('/')
def index():
    return render_template('index.html', categories=categories, products=products)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        
        if name and email and message:
            flash('Thank you for your message! We will get back to you soon.', 'success')
            return redirect(url_for('contact'))
        
        flash('Please fill out all fields.', 'warning')
    
    return render_template('contact.html')

@app.route('/products')
def products_page():
    return render_template('products.html', categories=categories, all_products=products)

@app.route('/category/<category_id>')
def category(category_id):
    if category_id in categories:
        return render_template('category.html', 
                             category=categories[category_id],
                             products=products[category_id][:20])
    return redirect(url_for('index'))

@app.route('/product/<product_id>')
def product_detail(product_id):
    for category in products:
        for product in products[category]:
            if product['id'] == product_id:
                return render_template('product.html', product=product)
    return redirect(url_for('index'))

@app.route('/compare')
def compare():
    # Get selected product IDs from query parameters
    product_ids = request.args.getlist('product_id')
    selected_category = request.args.get('category', 'laptops')
    
    if selected_category not in categories:
        selected_category = 'laptops'
    
    # Get products for comparison
    comparison_products = []
    
    # If product IDs are provided, find those specific products
    if product_ids:
        for product_id in product_ids:
            # Extract category from product ID (e.g., 'laptops1' -> 'laptops')
            category_name = ''.join([c for c in product_id if not c.isdigit()])
            
            if category_name in products:
                # Find the product in the category
                for product in products[category_name]:
                    if product['id'] == product_id:
                        comparison_products.append(product)
                        break
    
    # If no products were found or no IDs provided, use default products from selected category
    if not comparison_products:
        comparison_products = products[selected_category][:3]
    
    # Get all specs keys from all products for complete comparison
    all_specs_keys = set()
    for product in comparison_products:
        all_specs_keys.update(product['specs'].keys())
    
    # Sort the keys for consistent display
    all_specs_keys = sorted(list(all_specs_keys))
    
    return render_template('compare.html', 
                         products=comparison_products,
                         categories=categories,
                         all_specs_keys=all_specs_keys,
                         selected_category=selected_category)

if __name__ == '__main__':
    app.run(debug=True)
