# Stage 1: Build (musl static binary)
FROM rust:1.85-slim-bookworm AS builder
WORKDIR /build

RUN apt-get update && apt-get install -y musl-tools pkg-config libssl-dev && rm -rf /var/lib/apt/lists/*
RUN rustup target add x86_64-unknown-linux-musl

# Cache dependency compilation
COPY Cargo.toml Cargo.lock ./
RUN mkdir src && echo "fn main() {}" > src/main.rs && cargo build --release --target x86_64-unknown-linux-musl && rm -rf src

# Build actual application
COPY src/ src/
COPY migrations/ migrations/
RUN touch src/main.rs && cargo build --release --target x86_64-unknown-linux-musl

# Stage 2: Runtime (minimal Alpine image)
FROM alpine:3.21
RUN apk add --no-cache ca-certificates

WORKDIR /app
COPY --from=builder /build/target/x86_64-unknown-linux-musl/release/backend /app/backend
COPY app/templates/ /app/app/templates/
COPY app/static/ /app/app/static/

EXPOSE 5000
CMD ["/app/backend"]
