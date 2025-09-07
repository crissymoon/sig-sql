#!/usr/bin/env python3

import os
import json

def create_zig_advanced_datasets():
    """Create advanced Zig datasets with libraries and tools"""
    
    # Zig popular libraries and frameworks
    zig_libraries = [
        "zig-clap", "ziglyph", "zig-datetime", "zig-network", "zap",
        "raylib-zig", "mach", "zig-args", "known-folders", "zig-cache",
        "zigimg", "zig-sqlite", "zig-regex", "zig-toml", "zig-yaml",
        "zig-json", "zig-uri", "zigmod", "gyro", "zls", "zig-docgen",
        "zig-prometheus", "zig-uuid", "zig-base64", "zig-crypto"
    ]
    
    with open("zig_libraries.txt", "w") as f:
        for lib in zig_libraries:
            f.write(f"{lib}\n")
    
    # Zig compilation targets
    zig_targets = [
        "x86_64-linux-gnu", "x86_64-linux-musl", "x86_64-windows-gnu",
        "x86_64-macos", "aarch64-linux-gnu", "aarch64-macos", "arm-linux-gnueabihf",
        "i386-linux-gnu", "i386-windows-gnu", "riscv64-linux-gnu", "wasm32-freestanding",
        "wasm32-wasi", "x86_64-freebsd", "x86_64-netbsd", "x86_64-openbsd"
    ]
    
    with open("zig_targets.txt", "w") as f:
        for target in zig_targets:
            f.write(f"{target}\n")
    
    # Zig build system commands
    zig_build_commands = [
        "zig build", "zig build run", "zig build test", "zig build install",
        "zig build --help", "zig build --verbose", "zig build --summary all",
        "zig build -Doptimize=ReleaseFast", "zig build -Doptimize=ReleaseSmall",
        "zig build -Dtarget=x86_64-linux-gnu", "zig build --prefix /usr/local",
        "zig build --cache-dir build-cache", "zig build --global-cache-dir cache"
    ]
    
    with open("zig_build_commands.txt", "w") as f:
        for cmd in zig_build_commands:
            f.write(f"{cmd}\n")

def create_rust_advanced_datasets():
    """Create advanced Rust datasets with crates and tools"""
    
    # Popular Rust crates
    rust_crates = [
        "serde", "tokio", "clap", "reqwest", "diesel", "actix-web", "rocket",
        "warp", "hyper", "tower", "tonic", "prost", "sqlx", "sea-orm",
        "tracing", "log", "env_logger", "thiserror", "anyhow", "eyre",
        "rayon", "crossbeam", "parking_lot", "once_cell", "lazy_static",
        "regex", "chrono", "uuid", "rand", "serde_json", "toml", "yaml-rust",
        "config", "structopt", "clap", "indicatif", "console", "termion",
        "crossterm", "ratatui", "egui", "tauri", "bevy", "amethyst",
        "winit", "wgpu", "vulkano", "gfx-hal", "image", "imageproc"
    ]
    
    with open("rust_crates.txt", "w") as f:
        for crate in rust_crates:
            f.write(f"{crate}\n")
    
    # Rust cargo commands
    rust_cargo_commands = [
        "cargo new", "cargo init", "cargo build", "cargo run", "cargo test",
        "cargo check", "cargo clippy", "cargo fmt", "cargo doc", "cargo publish",
        "cargo install", "cargo uninstall", "cargo update", "cargo clean",
        "cargo tree", "cargo audit", "cargo outdated", "cargo expand",
        "cargo watch", "cargo tarpaulin", "cargo criterion", "cargo flamegraph",
        "cargo build --release", "cargo test --release", "cargo run --bin",
        "cargo build --target", "cargo cross", "cargo dist"
    ]
    
    with open("rust_cargo_commands.txt", "w") as f:
        for cmd in rust_cargo_commands:
            f.write(f"{cmd}\n")
    
    # Rust async patterns
    rust_async_patterns = [
        "async fn function() -> Result<T, E>",
        "await?", ".await", "async move { }",
        "tokio::spawn(async move { })",
        "tokio::time::sleep(Duration::from_secs(1)).await",
        "tokio::select! { }",
        "futures::join!(future1, future2)",
        "futures::try_join!(future1, future2)",
        "Stream::next().await",
        "async_stream::stream! { }",
        "Pin<Box<dyn Future<Output = T>>>",
        "tokio::sync::Mutex", "tokio::sync::RwLock",
        "tokio::sync::mpsc::channel", "tokio::sync::oneshot::channel"
    ]
    
    with open("rust_async_patterns.txt", "w") as f:
        for pattern in rust_async_patterns:
            f.write(f"{pattern}\n")

def create_go_advanced_datasets():
    """Create advanced Go datasets with modules and tools"""
    
    # Popular Go modules
    go_modules = [
        "github.com/gin-gonic/gin", "github.com/gorilla/mux", "github.com/echo-labstack/echo",
        "github.com/fiber-gopher/fiber", "github.com/go-chi/chi", "github.com/labstack/echo",
        "gorm.io/gorm", "github.com/jmoiron/sqlx", "go.mongodb.org/mongo-driver",
        "github.com/go-redis/redis", "github.com/elastic/go-elasticsearch",
        "github.com/spf13/cobra", "github.com/spf13/viper", "github.com/urfave/cli",
        "github.com/sirupsen/logrus", "go.uber.org/zap", "github.com/rs/zerolog",
        "github.com/stretchr/testify", "github.com/golang/mock", "github.com/onsi/ginkgo",
        "github.com/prometheus/client_golang", "github.com/opentracing/opentracing-go",
        "go.opentelemetry.io/otel", "github.com/jaegertracing/jaeger-client-go",
        "github.com/grpc-ecosystem/grpc-gateway", "google.golang.org/grpc",
        "google.golang.org/protobuf", "github.com/golang/protobuf"
    ]
    
    with open("go_modules.txt", "w") as f:
        for module in go_modules:
            f.write(f"{module}\n")
    
    # Go tools and commands
    go_commands = [
        "go mod init", "go mod tidy", "go mod download", "go mod verify",
        "go get", "go install", "go build", "go run", "go test", "go fmt",
        "go vet", "go doc", "go version", "go env", "go list", "go clean",
        "go generate", "go work init", "go work use", "go work sync",
        "gofmt", "goimports", "golint", "staticcheck", "gosec", "ineffassign",
        "go test -v", "go test -race", "go test -cover", "go test -bench",
        "go build -ldflags", "go build -tags", "go build -o", "go mod graph"
    ]
    
    with open("go_commands.txt", "w") as f:
        for cmd in go_commands:
            f.write(f"{cmd}\n")
    
    # Go design patterns
    go_patterns = [
        "Singleton pattern with sync.Once",
        "Factory pattern with constructors",
        "Builder pattern with method chaining",
        "Observer pattern with channels",
        "Worker pool pattern",
        "Pipeline pattern with channels",
        "Fan-in fan-out pattern",
        "Circuit breaker pattern",
        "Retry pattern with exponential backoff",
        "Context pattern for cancellation",
        "Middleware pattern for HTTP handlers",
        "Decorator pattern with function types",
        "Strategy pattern with interfaces",
        "Command pattern with function types"
    ]
    
    with open("go_patterns.txt", "w") as f:
        for pattern in go_patterns:
            f.write(f"{pattern}\n")

def create_systems_programming_concepts():
    """Create datasets for systems programming concepts across all three languages"""
    
    # Systems programming topics
    systems_concepts = [
        "Memory allocation strategies",
        "Cache-friendly data structures",
        "SIMD instructions and vectorization",
        "Lock-free data structures",
        "Memory barriers and atomic operations",
        "Virtual memory management",
        "Process and thread scheduling",
        "Inter-process communication (IPC)",
        "System call interfaces",
        "File system operations",
        "Network socket programming",
        "Signal handling",
        "Dynamic linking and loading",
        "Profiling and performance analysis",
        "Cross-compilation techniques",
        "Embedded systems programming",
        "Real-time systems constraints",
        "Hardware abstraction layers",
        "Device driver development",
        "Kernel module programming"
    ]
    
    with open("systems_programming_concepts.txt", "w") as f:
        for concept in systems_concepts:
            f.write(f"{concept}\n")
    
    # Performance optimization techniques
    performance_techniques = [
        "Zig: comptime evaluation for zero-cost abstractions",
        "Rust: zero-cost abstractions with compile-time guarantees",
        "Go: escape analysis for stack vs heap allocation",
        "Profile-guided optimization (PGO)",
        "Link-time optimization (LTO)",
        "Dead code elimination",
        "Inlining strategies",
        "Loop unrolling and vectorization",
        "Branch prediction optimization",
        "Cache locality improvements",
        "Memory prefetching",
        "NUMA awareness",
        "CPU affinity and thread pinning",
        "Lock contention reduction",
        "False sharing avoidance"
    ]
    
    with open("performance_optimization.txt", "w") as f:
        for technique in performance_techniques:
            f.write(f"{technique}\n")

def create_language_specific_json():
    """Create JSON datasets with structured information"""
    
    # Language comparison data
    language_comparison = {
        "memory_safety": {
            "zig": "Manual with allocators and safety checks",
            "rust": "Automatic with ownership system",
            "go": "Garbage collected with runtime safety"
        },
        "performance": {
            "zig": "Zero-cost abstractions, comptime optimization",
            "rust": "Zero-cost abstractions, minimal runtime",
            "go": "Fast compilation, runtime garbage collection overhead"
        },
        "learning_curve": {
            "zig": "Moderate, explicit control",
            "rust": "Steep, complex type system",
            "go": "Gentle, simple syntax"
        },
        "use_cases": {
            "zig": ["System programming", "Embedded systems", "Game engines", "Compilers"],
            "rust": ["System programming", "Web backends", "CLI tools", "Blockchain"],
            "go": ["Web services", "Cloud infrastructure", "DevOps tools", "Microservices"]
        }
    }
    
    with open("language_comparison.json", "w") as f:
        json.dump(language_comparison, f, indent=2)
    
    # Build tools comparison
    build_tools = {
        "zig": {
            "primary": "zig build",
            "package_manager": "Built-in (zig fetch)",
            "test_runner": "zig test",
            "formatter": "zig fmt",
            "linter": "Built-in compiler warnings"
        },
        "rust": {
            "primary": "cargo build",
            "package_manager": "cargo",
            "test_runner": "cargo test",
            "formatter": "cargo fmt",
            "linter": "cargo clippy"
        },
        "go": {
            "primary": "go build",
            "package_manager": "go mod",
            "test_runner": "go test",
            "formatter": "go fmt",
            "linter": "go vet / staticcheck"
        }
    }
    
    with open("build_tools_comparison.json", "w") as f:
        json.dump(build_tools, f, indent=2)

def main():
    """Main function to create all advanced language datasets"""
    os.chdir("datasets")
    
    print("Creating advanced Zig datasets...")
    create_zig_advanced_datasets()
    
    print("Creating advanced Rust datasets...")
    create_rust_advanced_datasets()
    
    print("Creating advanced Go datasets...")
    create_go_advanced_datasets()
    
    print("Creating systems programming concepts...")
    create_systems_programming_concepts()
    
    print("Creating JSON comparison datasets...")
    create_language_specific_json()
    
    print("\nCreated advanced language datasets:")
    
    # List all new files
    new_files = [
        "zig_libraries.txt", "zig_targets.txt", "zig_build_commands.txt",
        "rust_crates.txt", "rust_cargo_commands.txt", "rust_async_patterns.txt",
        "go_modules.txt", "go_commands.txt", "go_patterns.txt",
        "systems_programming_concepts.txt", "performance_optimization.txt",
        "language_comparison.json", "build_tools_comparison.json"
    ]
    
    for file in new_files:
        print(f"  - {file}")

if __name__ == "__main__":
    main()
