#!/bin/bash
# Quick rebuild and deploy script

echo "Removing old build..."
rm -rf build/

echo "🔨 Building with pygbag..."
python -m pygbag --build --template custom.tmpl .         

echo ""
echo "📦 Deploying to Vercel..."
vercel --prod

echo ""
echo "✅ Done! Check your deployment at:"
echo "   https://suffi-30.vercel.app"
