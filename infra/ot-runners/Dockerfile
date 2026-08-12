FROM ghcr.io/actions/actions-runner@sha256:0cfdcc701ce933c6d243c6b0b2da767366dc9f2e99961d4c3754b0b78084cdda

USER root

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        bash \
        build-essential \
        ca-certificates \
        cmake \
        curl \
        git \
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

USER runner
WORKDIR /home/runner
ENTRYPOINT ["/home/runner/ot-runner-entrypoint.sh"]
