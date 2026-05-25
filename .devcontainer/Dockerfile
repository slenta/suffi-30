FROM base-devcontainer:local

USER root

# System libs pygame/SDL2 need to build/run on Linux (pygame wheel usually exists,
# but SDL2 runtime libs are required for `python play.py` inside the container).
RUN apt-get update && apt-get install -y --no-install-recommends \
    libsdl2-2.0-0 \
    libsdl2-image-2.0-0 \
    libsdl2-mixer-2.0-0 \
    libsdl2-ttf-2.0-0 \
    libfreetype6 \
    libportmidi0 \
    libjpeg62-turbo \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Vercel CLI for deploys + local `vercel dev`
RUN npm install -g vercel@latest

USER node

# Per-repo firewall script
COPY .devcontainer/init-firewall.sh /usr/local/bin/init-firewall.sh
USER root
RUN chmod +x /usr/local/bin/init-firewall.sh
USER node
