#!/bin/bash
set -e

echo "🎮 Deploying suffi-30 to Vercel..."

# Step 1: Build the web version with pygbag
echo "📦 Building web version with pygbag..."
python -m pygbag --PYBUILD 3.12 --build .

# Step 2: Copy build files to public directory
echo "📁 Copying build files to public directory..."
rm -rf public
mkdir -p public
cp -r build/web/* public/

# Step 3: Deploy to Vercel
echo "☁️  Deploying to Vercel..."
vercel --prod

echo "✅ Deployment complete!"
