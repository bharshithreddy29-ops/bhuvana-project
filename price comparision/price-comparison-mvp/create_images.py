from PIL import Image, ImageDraw, ImageFont
import os

def create_placeholder_image(text, size=(300, 300), filename=None):
    """Create a simple placeholder image with text"""
    # Create image with light gray background
    img = Image.new('RGB', size, color='#f8f9fa')
    draw = ImageDraw.Draw(img)
    
    # Try to use a font, fallback to default if not available
    try:
        font = ImageFont.truetype("arial.ttf", 24)
    except:
        font = ImageFont.load_default()
    
    # Calculate text position to center it
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (size[0] - text_width) // 2
    y = (size[1] - text_height) // 2
    
    # Draw text
    draw.text((x, y), text, fill='#6c757d', font=font)
    
    # Save image
    if filename:
        img.save(filename)
    
    return img

# Create placeholder images for common products
products = [
    'amul_milk', 'maggi_noodles', 'britannia_bread', 'coca_cola', 
    'lays_chips', 'nike_shoes', 'adidas_tshirt', 'levis_jeans',
    'zara_dress', 'puma_sneakers', 'bananas', 'tata_salt'
]

base_path = os.path.join(os.path.dirname(__file__), 'static', 'images', 'products')
os.makedirs(base_path, exist_ok=True)

for product in products:
    filename = os.path.join(base_path, f'{product}.jpg')
    if not os.path.exists(filename):
        create_placeholder_image(product.replace('_', ' ').title(), filename=filename)

# Create a general placeholder
create_placeholder_image('Product Image', filename=os.path.join(base_path, 'placeholder.jpg'))

print("Placeholder images created successfully!")