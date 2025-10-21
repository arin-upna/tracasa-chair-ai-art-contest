#!/usr/bin/env python3
"""
Script to convert and optimize images for the art contest website.
Converts PNG images to JPG format and resizes them to width 1024px.
"""

import os
from pathlib import Path
from PIL import Image

# Configuration
TARGET_WIDTH = 1024
JPG_QUALITY = 85  # Quality for JPG compression (0-100)
DATA_DIR = "data"

def convert_and_resize_image(input_path, output_path, target_width=TARGET_WIDTH):
    """
    Convert PNG to JPG and resize to target width while maintaining aspect ratio.
    
    Args:
        input_path: Path to input PNG file
        output_path: Path to output JPG file
        target_width: Target width in pixels
    """
    try:
        # Open the image
        img = Image.open(input_path)
        
        # Convert RGBA to RGB if necessary (PNG with transparency)
        if img.mode in ('RGBA', 'LA', 'P'):
            # Create a white background
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Calculate new dimensions maintaining aspect ratio
        original_width, original_height = img.size
        if original_width > target_width:
            aspect_ratio = original_height / original_width
            new_width = target_width
            new_height = int(target_width * aspect_ratio)
            
            # Resize with high-quality resampling
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            print(f"  Resized from {original_width}x{original_height} to {new_width}x{new_height}")
        else:
            print(f"  Image already smaller than {target_width}px, keeping original size")
        
        # Save as JPG
        img.save(output_path, 'JPEG', quality=JPG_QUALITY, optimize=True)
        
        # Get file sizes
        input_size = os.path.getsize(input_path) / 1024  # KB
        output_size = os.path.getsize(output_path) / 1024  # KB
        reduction = ((input_size - output_size) / input_size) * 100
        
        print(f"  Size: {input_size:.1f}KB → {output_size:.1f}KB (reduced by {reduction:.1f}%)")
        
    except Exception as e:
        print(f"  ERROR: {e}")

def process_directory(base_dir):
    """
    Process all PNG files in the data directory structure.
    """
    base_path = Path(base_dir)
    
    if not base_path.exists():
        print(f"Error: Directory '{base_dir}' not found!")
        return
    
    # Find all PNG files
    png_files = list(base_path.glob("*/ArteDigital/*.png"))
    
    if not png_files:
        print(f"No PNG files found in '{base_dir}'")
        return
    
    print(f"Found {len(png_files)} PNG files to convert\n")
    
    converted_count = 0
    total_input_size = 0
    total_output_size = 0
    
    for png_file in sorted(png_files):
        # Create output path with .jpg extension
        jpg_file = png_file.with_suffix('.jpg')
        
        print(f"Converting: {png_file.relative_to(base_path)}")
        
        # Track sizes
        input_size = os.path.getsize(png_file)
        total_input_size += input_size
        
        # Convert and resize
        convert_and_resize_image(png_file, jpg_file)
        
        output_size = os.path.getsize(jpg_file)
        total_output_size += output_size
        
        converted_count += 1
        print()
    
    # Summary
    print("=" * 60)
    print(f"Conversion complete!")
    print(f"Files converted: {converted_count}")
    print(f"Total size before: {total_input_size / 1024 / 1024:.2f} MB")
    print(f"Total size after: {total_output_size / 1024 / 1024:.2f} MB")
    total_reduction = ((total_input_size - total_output_size) / total_input_size) * 100
    print(f"Total size reduction: {total_reduction:.1f}%")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Review the converted JPG files")
    print("2. If satisfied, delete the original PNG files")
    print("3. Update HTML files to use .jpg instead of .png")

if __name__ == "__main__":
    print("Image Conversion Script")
    print("=" * 60)
    print(f"Target width: {TARGET_WIDTH}px")
    print(f"JPG quality: {JPG_QUALITY}")
    print(f"Processing directory: {DATA_DIR}")
    print("=" * 60)
    print()
    
    process_directory(DATA_DIR)
