from PIL import Image, ImageDraw, ImageFont
import os

def create_product_image(product_name, category_color, filename):
    """Create a realistic product placeholder image"""
    # Create image with category-specific background
    img = Image.new('RGB', (400, 400), color=category_color)
    draw = ImageDraw.Draw(img)
    
    # Add gradient effect
    for i in range(400):
        alpha = int(255 * (1 - i/400))
        color = tuple(min(255, c + alpha//4) for c in category_color)
        draw.line([(0, i), (400, i)], fill=color)
    
    # Try to use a font, fallback to default if not available
    try:
        title_font = ImageFont.truetype("arial.ttf", 32)
        subtitle_font = ImageFont.truetype("arial.ttf", 16)
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
    
    # Add product name
    lines = product_name.split(' ')
    if len(lines) > 2:
        line1 = ' '.join(lines[:2])
        line2 = ' '.join(lines[2:])
    else:
        line1 = product_name
        line2 = ""
    
    # Calculate text position to center it
    bbox1 = draw.textbbox((0, 0), line1, font=title_font)
    text_width1 = bbox1[2] - bbox1[0]
    text_height1 = bbox1[3] - bbox1[1]
    
    x1 = (400 - text_width1) // 2
    y1 = 150 if line2 else 180
    
    # Draw main text with shadow
    draw.text((x1+2, y1+2), line1, fill=(0, 0, 0, 128), font=title_font)
    draw.text((x1, y1), line1, fill='white', font=title_font)
    
    if line2:
        bbox2 = draw.textbbox((0, 0), line2, font=title_font)
        text_width2 = bbox2[2] - bbox2[0]
        x2 = (400 - text_width2) // 2
        y2 = y1 + 40
        
        draw.text((x2+2, y2+2), line2, fill=(0, 0, 0, 128), font=title_font)
        draw.text((x2, y2), line2, fill='white', font=title_font)
    
    # Add "Product Image" subtitle
    subtitle = "Product Image"
    bbox_sub = draw.textbbox((0, 0), subtitle, font=subtitle_font)
    text_width_sub = bbox_sub[2] - bbox_sub[0]
    x_sub = (400 - text_width_sub) // 2
    y_sub = 280
    
    draw.text((x_sub+1, y_sub+1), subtitle, fill=(0, 0, 0, 100), font=subtitle_font)
    draw.text((x_sub, y_sub), subtitle, fill='white', font=subtitle_font)
    
    # Add decorative border
    draw.rectangle([(10, 10), (390, 390)], outline='white', width=3)
    
    # Save image
    img.save(filename)
    return img

# Create product images for different categories
products = {
    # Electronics - Blue theme
    'electronics': [
        ('iPhone 15 Pro', 'iphone15_pro.jpg'),
        ('Samsung Galaxy S24', 'galaxy_s24_ultra.jpg'),
        ('MacBook Pro 14', 'macbook_pro_14.jpg'),
        ('Dell XPS 15', 'dell_xps_15.jpg'),
        ('Sony Headphones', 'sony_wh1000xm5.jpg'),
        ('iPad Air 11', 'ipad_air_11.jpg'),
        ('Canon Camera', 'canon_eos_r8.jpg'),
        ('LG OLED TV', 'lg_oled_65.jpg'),
        ('Apple Watch', 'apple_watch_9.jpg'),
        ('Samsung TV', 'samsung_neo_qled.jpg')
    ],
    
    # Fashion - Purple theme
    'fashion': [
        ('Nike Air Jordan', 'air_jordan_1.jpg'),
        ('Adidas Ultraboost', 'ultraboost_23.jpg'),
        ('Levis 501 Jeans', 'levis_501.jpg'),
        ('Zara Blazer', 'zara_blazer.jpg'),
        ('H&M T-Shirt', 'hm_organic_tee.jpg'),
        ('Puma Sneakers', 'puma_rsx.jpg'),
        ('Tommy Polo', 'tommy_polo.jpg'),
        ('Calvin Klein', 'ck_jeans.jpg'),
        ('Converse Chuck', 'converse_chuck.jpg'),
        ('Mango Dress', 'mango_dress.jpg')
    ],
    
    # Home & Kitchen - Green theme
    'home': [
        ('Philips Air Fryer', 'philips_air_fryer.jpg'),
        ('Prestige Cooktop', 'prestige_induction.jpg'),
        ('IKEA Bed Frame', 'ikea_hemnes.jpg'),
        ('Godrej Fridge', 'godrej_fridge.jpg'),
        ('Bajaj Mixer', 'bajaj_mixer.jpg'),
        ('Dining Table', 'ul_dining_table.jpg'),
        ('Washing Machine', 'whirlpool_washing.jpg'),
        ('Pressure Cooker', 'hawkins_cooker.jpg'),
        ('Plastic Chairs', 'nilkamal_chairs.jpg'),
        ('Dinner Set', 'borosil_dinner_set.jpg')
    ],
    
    # Beauty - Pink theme
    'beauty': [
        ('Lakme Foundation', 'lakme_foundation.jpg'),
        ('Nykaa Lipstick', 'nykaa_lipstick.jpg'),
        ('Himalaya Face Wash', 'himalaya_facewash.jpg'),
        ('Olay Serum', 'olay_serum.jpg'),
        ('Loreal Shampoo', 'loreal_shampoo.jpg'),
        ('Maybelline Mascara', 'maybelline_mascara.jpg'),
        ('Neutrogena Sunscreen', 'neutrogena_sunscreen.jpg'),
        ('Body Shop Butter', 'tbs_body_butter.jpg'),
        ('Plum Face Mask', 'plum_face_mask.jpg'),
        ('Forest Essentials', 'fe_face_oil.jpg')
    ],
    
    # Sports - Orange theme
    'sports': [
        ('Treadmill', 'decathlon_treadmill.jpg'),
        ('Football', 'adidas_football.jpg'),
        ('Running Shorts', 'nike_running_shorts.jpg'),
        ('Badminton Racket', 'yonex_racket.jpg'),
        ('Gym Bag', 'reebok_gym_bag.jpg'),
        ('Training Gloves', 'puma_gloves.jpg'),
        ('Cricket Bat', 'cosco_bat.jpg'),
        ('Basketball', 'nivia_basketball.jpg'),
        ('Fitness Tracker', 'fitbit_charge5.jpg'),
        ('Resistance Bands', 'boldfit_bands.jpg')
    ]
}

# Color schemes for categories
colors = {
    'electronics': (52, 152, 219),  # Blue
    'fashion': (155, 89, 182),      # Purple
    'home': (46, 204, 113),         # Green
    'beauty': (231, 76, 60),        # Red/Pink
    'sports': (230, 126, 34)        # Orange
}

# Create images directory
base_path = os.path.join(os.path.dirname(__file__), 'static', 'images', 'products')
os.makedirs(base_path, exist_ok=True)

# Generate images
for category, product_list in products.items():
    category_color = colors[category]
    for product_name, filename in product_list:
        filepath = os.path.join(base_path, filename)
        if not os.path.exists(filepath):
            create_product_image(product_name, category_color, filepath)
            print(f"Created: {filename}")

# Create some grocery items with green theme
grocery_items = [
    ('Amul Milk', 'amul_milk.jpg'),
    ('Maggi Noodles', 'maggi_noodles.jpg'),
    ('Britannia Bread', 'britannia_bread.jpg'),
    ('Coca Cola', 'coca_cola.jpg'),
    ('Lays Chips', 'lays_chips.jpg'),
    ('Fresh Bananas', 'bananas.jpg'),
    ('Tata Salt', 'tata_salt.jpg')
]

for product_name, filename in grocery_items:
    filepath = os.path.join(base_path, filename)
    if not os.path.exists(filepath):
        create_product_image(product_name, (46, 204, 113), filepath)
        print(f"Created: {filename}")

print("All product images created successfully!")