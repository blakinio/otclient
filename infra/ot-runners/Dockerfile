FROM ghcr.io/actions/actions-runner@sha256:0cfdcc701ce933c6d243c6b0b2da767366dc9f2e99961d4c3754b0b78084cdda AS base

USER root

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        bash \
        build-essential \
        ca-certificates \
        cmake \
        curl \
        git \
        gosu \
        jq \
        ninja-build \
        pkg-config \
        python3 \
        python3-pip \
    && rm -rf /var/lib/apt/lists/*

COPY --chown=runner:runner entrypoint.sh /home/runner/ot-runner-entrypoint.sh
RUN chmod 0755 /home/runner/ot-runner-entrypoint.sh \
    && mkdir -p /runner-state /home/runner/_work \
    && chown -R runner:runner /runner-state /home/runner/_work

WORKDIR /home/runner
ENTRYPOINT ["/home/runner/ot-runner-entrypoint.sh"]

FROM base AS otclient-tibia-re

USER root

# Runtime/debug dependencies already exercised by the official Linux Tibia
# analysis workflows on Ubuntu 24.04. They are baked into the dedicated
# OTClient runner so jobs remain unprivileged and need neither sudo nor a
# Docker socket at execution time.
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        file \
        gdb \
        imagemagick \
        iproute2 \
        libasound2t64 \
        libatk1.0-0t64 \
        libatspi2.0-0t64 \
        libcups2t64 \
        libdbus-1-3 \
        libdrm2 \
        libegl1 \
        libfontconfig1 \
        libfreetype6 \
        libgbm1 \
        libgl1 \
        libglx0 \
        libgtk-3-0t64 \
        libnspr4 \
        libnss3 \
        libopengl0 \
        libpulse0 \
        libvulkan1 \
        libx11-6 \
        libx11-xcb1 \
        libxcb-cursor0 \
        libxcb-glx0 \
        libxcb-icccm4 \
        libxcb-image0 \
        libxcb-keysyms1 \
        libxcb-randr0 \
        libxcb-render-util0 \
        libxcb-render0 \
        libxcb-shape0 \
        libxcb-shm0 \
        libxcb-sync1 \
        libxcb-util1 \
        libxcb-xfixes0 \
        libxcb-xinerama0 \
        libxcb-xkb1 \
        libxcomposite1 \
        libxdamage1 \
        libxi6 \
        libxkbcommon-x11-0 \
        libxrandr2 \
        libxrender1 \
        libxtst6 \
        lsof \
        mesa-utils \
        mesa-vulkan-drivers \
        netcat-openbsd \
        procps \
        proxychains4 \
        python3-pyelftools \
        python3-yaml \
        qt6-base-dev \
        socat \
        strace \
        vulkan-tools \
        x11-utils \
        xclip \
        xdotool \
        xvfb \
    && rm -rf /var/lib/apt/lists/*

USER root
