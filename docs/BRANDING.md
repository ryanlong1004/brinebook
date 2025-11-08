# BrineBook Branding Guide

## Logo Variations

BrineBook has three primary logo variations, each designed for different use cases:

![BrineBook Logo Variations](branding-logos.png)

### Logo Files

All logo files are available in the following locations:

- **Full Branding Sheet**: `docs/branding-logos.png` - Contains all three logo variations
- **Main Logo**: `frontend/public/images/logo-main.png` - Primary logo (top section)
- **Variant Logo**: `frontend/public/images/logo-variant.png` - Alternative logo style (middle section)
- **Alt Logo**: `frontend/public/images/logo-alt.png` - Additional logo variation (bottom section)

### Logo Usage Guidelines

#### Main Logo (`logo-main.png`)

- **Primary use**: Navigation bar, app header
- **Best for**: Light and dark backgrounds
- **Dimensions**: 1024x512px

#### Variant Logo (`logo-variant.png`)

- **Primary use**: Marketing materials, documentation headers
- **Best for**: Presentations and promotional content
- **Dimensions**: 1024x512px

#### Alt Logo (`logo-alt.png`)

- **Primary use**: Social media, favicons, app icons
- **Best for**: Square/compact spaces
- **Dimensions**: 1024x512px

### Implementation

#### Frontend (Vue)

The main logo is used in the Navbar component:

```vue
<img
  src="/images/logo-main.png"
  alt="BrineBook Logo"
  class="h-10 w-auto object-contain"
/>
```

#### Documentation

The full branding sheet is displayed in the README:

```markdown
<div align="center">
  <img src="docs/branding-logos.png" alt="BrineBook Branding" width="400">
</div>
```

### Brand Colors

Based on the logo design:

- **Primary**: Warm tones (cooking/culinary theme)
- **Accent**: Complementary colors that represent freshness and quality
- **Background**: Dark theme (`bg-gray-900`) for the application interface

### Design Philosophy

BrineBook's branding emphasizes:

- **Professional culinary quality**: Restaurant-grade recipes and presentation
- **AI-powered intelligence**: Modern, tech-forward approach to cooking
- **Accessibility**: Clear, readable design that works across devices

## File Structure

```
brinebook/
├── docs/
│   ├── branding-logos.png          # Full branding sheet (all variations)
│   └── BRANDING.md                 # This file
├── frontend/
│   └── public/
│       └── images/
│           ├── logo-main.png       # Primary logo
│           ├── logo-variant.png    # Alternative logo
│           └── logo-alt.png        # Additional variation
└── logos.png                       # Original source file
```

## Updating Logos

To update the logos:

1. Replace `logos.png` with the new composite image (1024x1536, 3 stacked logos)
2. Run the extraction script:

```python
from PIL import Image
img = Image.open('logos.png')
width, height = img.size
logo_height = height // 3

for i in range(3):
    logo = img.crop((0, i * logo_height, width, (i + 1) * logo_height))
    logo.save(f'frontend/public/images/logo-{["main", "variant", "alt"][i]}.png')
```

3. Restart the Vite dev server to see changes

## License

All BrineBook branding materials are proprietary and should not be used without permission.
