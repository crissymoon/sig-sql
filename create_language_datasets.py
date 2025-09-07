#!/usr/bin/env python3

import os

def create_zig_datasets():
    """Create Zig programming language datasets"""
    
    # Zig keywords and built-ins
    zig_keywords = [
        "const", "var", "fn", "struct", "enum", "union", "error", "try", "catch",
        "if", "else", "while", "for", "switch", "break", "continue", "return",
        "defer", "errdefer", "async", "await", "suspend", "resume", "nosuspend",
        "comptime", "inline", "pub", "export", "extern", "packed", "align",
        "allowzero", "volatile", "threadlocal", "linksection", "callconv",
        "test", "unreachable", "undefined", "null", "true", "false",
        "and", "or", "orelse", "catch", "anytype", "anyframe", "type"
    ]
    
    with open("zig_keywords.txt", "w") as f:
        for keyword in zig_keywords:
            f.write(f"{keyword}\n")
    
    # Zig built-in functions
    zig_builtins = [
        "@addWithOverflow", "@alignCast", "@alignOf", "@as", "@atomicLoad",
        "@atomicRmw", "@atomicStore", "@bitCast", "@bitOffsetOf", "@bitReverse",
        "@bitSizeOf", "@boolToInt", "@breakpoint", "@byteOffsetOf", "@bytesToSlice",
        "@cDefine", "@cImport", "@cInclude", "@clz", "@cmpxchgStrong", "@cmpxchgWeak",
        "@compileError", "@compileLog", "@ctz", "@cUndef", "@divExact", "@divFloor",
        "@divTrunc", "@embedFile", "@enumToInt", "@errorName", "@errorReturnTrace",
        "@errorToInt", "@export", "@fence", "@field", "@fieldParentPtr", "@floatCast",
        "@floatToInt", "@frame", "@frameAddress", "@frameSize", "@hasDecl", "@hasField",
        "@import", "@intCast", "@intToEnum", "@intToError", "@intToFloat", "@intToPtr",
        "@memcpy", "@memset", "@mod", "@mulWithOverflow", "@newStackCall", "@offsetOf",
        "@panic", "@popCount", "@ptrCast", "@ptrToInt", "@rem", "@returnAddress",
        "@setAlignStack", "@setCold", "@setEvalBranchQuota", "@setFloatMode",
        "@setGlobalLinkage", "@setGlobalSection", "@setRuntimeSafety", "@shlExact",
        "@shlWithOverflow", "@shrExact", "@shuffle", "@sizeOf", "@splat", "@sqrt",
        "@subWithOverflow", "@tagName", "@This", "@truncate", "@typeInfo", "@typeName",
        "@typeOf", "@unionInit", "@Vector", "@wasmMemoryGrow", "@wasmMemorySize"
    ]
    
    with open("zig_builtins.txt", "w") as f:
        for builtin in zig_builtins:
            f.write(f"{builtin}\n")
    
    # Zig standard library modules
    zig_std_modules = [
        "std.ArrayList", "std.HashMap", "std.BufMap", "std.StringHashMap",
        "std.allocator", "std.mem", "std.fmt", "std.io", "std.fs", "std.os",
        "std.process", "std.thread", "std.atomic", "std.crypto", "std.hash",
        "std.json", "std.log", "std.math", "std.net", "std.rand", "std.sort",
        "std.testing", "std.time", "std.unicode", "std.uri", "std.zig",
        "std.c", "std.builtin", "std.debug", "std.heap", "std.meta",
        "std.target", "std.compress", "std.ascii", "std.base64", "std.bit_set"
    ]
    
    with open("zig_std_modules.txt", "w") as f:
        for module in zig_std_modules:
            f.write(f"{module}\n")
    
    # Zig code patterns and examples
    zig_patterns = [
        "const allocator = std.heap.page_allocator;",
        "var list = std.ArrayList(i32).init(allocator);",
        "defer list.deinit();",
        "const result = try some_function();",
        "if (condition) |value| { }",
        "switch (value) { .tag => { }, else => { } }",
        "for (items) |item| { }",
        "while (condition) : (increment) { }",
        "const MyStruct = struct { field: i32 };",
        "const MyEnum = enum { variant_a, variant_b };",
        "pub fn main() !void { }",
        "test \"example test\" { }",
        "comptime var counter = 0;",
        "const array = [_]i32{1, 2, 3};",
        "const slice = array[0..2];",
        "errdefer allocator.free(memory);",
        "const optional: ?i32 = null;",
        "const error_union: !i32 = 42;"
    ]
    
    with open("zig_patterns.txt", "w") as f:
        for pattern in zig_patterns:
            f.write(f"{pattern}\n")

def create_rust_datasets():
    """Create Rust programming language datasets"""
    
    # Rust keywords
    rust_keywords = [
        "as", "async", "await", "break", "const", "continue", "crate", "dyn",
        "else", "enum", "extern", "false", "fn", "for", "if", "impl", "in",
        "let", "loop", "match", "mod", "move", "mut", "pub", "ref", "return",
        "self", "Self", "static", "struct", "super", "trait", "true", "type",
        "union", "unsafe", "use", "where", "while", "abstract", "become",
        "box", "do", "final", "macro", "override", "priv", "typeof", "unsized",
        "virtual", "yield", "try", "macro_rules", "raw"
    ]
    
    with open("rust_keywords.txt", "w") as f:
        for keyword in rust_keywords:
            f.write(f"{keyword}\n")
    
    # Rust standard library types and traits
    rust_std_types = [
        "Vec", "HashMap", "HashSet", "BTreeMap", "BTreeSet", "LinkedList",
        "VecDeque", "String", "str", "Option", "Result", "Box", "Rc", "Arc",
        "RefCell", "Cell", "Mutex", "RwLock", "Channel", "Receiver", "Sender",
        "Iterator", "IntoIterator", "Collect", "Clone", "Copy", "Debug", "Display",
        "PartialEq", "Eq", "PartialOrd", "Ord", "Hash", "Default", "Drop",
        "From", "Into", "TryFrom", "TryInto", "AsRef", "AsMut", "Deref", "DerefMut",
        "Index", "IndexMut", "Add", "Sub", "Mul", "Div", "Rem", "Not", "BitAnd",
        "BitOr", "BitXor", "Shl", "Shr", "Send", "Sync", "Sized", "Unpin",
        "Future", "Stream", "Read", "Write", "Seek", "BufRead", "BufWrite"
    ]
    
    with open("rust_std_types.txt", "w") as f:
        for rust_type in rust_std_types:
            f.write(f"{rust_type}\n")
    
    # Rust macros
    rust_macros = [
        "println!", "print!", "eprintln!", "eprint!", "format!", "panic!",
        "assert!", "assert_eq!", "assert_ne!", "debug_assert!", "unreachable!",
        "unimplemented!", "todo!", "vec!", "include!", "include_str!", "include_bytes!",
        "env!", "option_env!", "concat!", "stringify!", "file!", "line!", "column!",
        "module_path!", "cfg!", "compile_error!", "thread_local!", "lazy_static!",
        "matches!", "write!", "writeln!", "dbg!", "is_x86_feature_detected!"
    ]
    
    with open("rust_macros.txt", "w") as f:
        for macro in rust_macros:
            f.write(f"{macro}\n")
    
    # Rust code patterns
    rust_patterns = [
        "fn main() { }",
        "let mut variable = value;",
        "let variable: Type = value;",
        "match expression { pattern => result, _ => default }",
        "if let Some(value) = option { }",
        "while let Some(item) = iterator.next() { }",
        "for item in collection { }",
        "impl Trait for Type { }",
        "struct Name { field: Type }",
        "enum Name { Variant(Type) }",
        "fn function(param: Type) -> ReturnType { }",
        "use std::collections::HashMap;",
        "mod module_name;",
        "pub struct PublicStruct;",
        "#[derive(Debug, Clone)]",
        "Result<T, E>",
        "Option<T>",
        "Box<dyn Trait>",
        "Arc<Mutex<T>>",
        "async fn async_function() -> Result<(), Error> { }",
        "let result = function().await?;",
        "|| { /* closure */ }",
        "|param| param + 1",
        "vec![1, 2, 3]",
        "HashMap::new()",
        "&str vs String",
        "unsafe { /* unsafe code */ }"
    ]
    
    with open("rust_patterns.txt", "w") as f:
        for pattern in rust_patterns:
            f.write(f"{pattern}\n")

def create_go_datasets():
    """Create Go programming language datasets"""
    
    # Go keywords
    go_keywords = [
        "break", "case", "chan", "const", "continue", "default", "defer", "else",
        "fallthrough", "for", "func", "go", "goto", "if", "import", "interface",
        "map", "package", "range", "return", "select", "struct", "switch", "type",
        "var", "nil", "true", "false", "iota", "make", "new", "len", "cap",
        "append", "copy", "delete", "close", "panic", "recover", "print", "println"
    ]
    
    with open("go_keywords.txt", "w") as f:
        for keyword in go_keywords:
            f.write(f"{keyword}\n")
    
    # Go standard library packages
    go_std_packages = [
        "fmt", "os", "io", "bufio", "strings", "strconv", "time", "math", "rand",
        "sort", "net", "net/http", "net/url", "encoding/json", "encoding/xml",
        "encoding/csv", "database/sql", "context", "sync", "crypto", "crypto/tls",
        "crypto/rand", "log", "flag", "path", "path/filepath", "regexp", "bytes",
        "reflect", "runtime", "testing", "errors", "archive/zip", "archive/tar",
        "compress/gzip", "image", "image/png", "image/jpeg", "html", "html/template",
        "text/template", "go/ast", "go/parser", "go/token", "unicode", "unicode/utf8"
    ]
    
    with open("go_std_packages.txt", "w") as f:
        for package in go_std_packages:
            f.write(f"{package}\n")
    
    # Go built-in types and functions
    go_builtins = [
        "bool", "byte", "complex64", "complex128", "error", "float32", "float64",
        "int", "int8", "int16", "int32", "int64", "rune", "string", "uint",
        "uint8", "uint16", "uint32", "uint64", "uintptr", "append", "cap", "close",
        "complex", "copy", "delete", "imag", "len", "make", "new", "panic",
        "print", "println", "real", "recover"
    ]
    
    with open("go_builtins.txt", "w") as f:
        for builtin in go_builtins:
            f.write(f"{builtin}\n")
    
    # Go code patterns
    go_patterns = [
        "package main",
        "import \"fmt\"",
        "func main() { }",
        "func function(param type) returnType { }",
        "var variable type = value",
        "variable := value",
        "if condition { }",
        "for i := 0; i < len(slice); i++ { }",
        "for index, value := range slice { }",
        "for key, value := range map { }",
        "switch value { case x: }",
        "select { case <-channel: }",
        "go function()",
        "defer function()",
        "make(chan type)",
        "make([]type, length)",
        "make(map[keyType]valueType)",
        "type StructName struct { field type }",
        "type InterfaceName interface { method() }",
        "if err != nil { return err }",
        "result, err := function()",
        "func (receiver Type) method() { }",
        "json.Marshal(data)",
        "json.Unmarshal(data, &result)",
        "http.HandleFunc(\"/path\", handler)",
        "fmt.Printf(\"format %s\\n\", value)",
        "errors.New(\"error message\")",
        "context.Background()",
        "sync.WaitGroup",
        "sync.Mutex"
    ]
    
    with open("go_patterns.txt", "w") as f:
        for pattern in go_patterns:
            f.write(f"{pattern}\n")

def create_language_comparison():
    """Create comparison datasets between languages"""
    
    # Memory management concepts
    memory_management = [
        "Zig: Manual memory management with allocators",
        "Rust: Ownership system with automatic memory management",
        "Go: Garbage collector handles memory automatically",
        "Zig: defer for cleanup, errdefer for error cleanup",
        "Rust: RAII (Resource Acquisition Is Initialization)",
        "Go: Finalizers and runtime garbage collection",
        "Zig: Comptime memory allocation",
        "Rust: Stack vs heap allocation control",
        "Go: Escape analysis determines allocation location"
    ]
    
    with open("memory_management_comparison.txt", "w") as f:
        for concept in memory_management:
            f.write(f"{concept}\n")
    
    # Error handling approaches
    error_handling = [
        "Zig: Error unions (!Type) and try/catch",
        "Rust: Result<T, E> type and ? operator",
        "Go: Multiple return values with error type",
        "Zig: Explicit error handling required",
        "Rust: Compile-time error handling guarantees",
        "Go: Runtime error checking conventions",
        "Zig: Error sets for specific error types",
        "Rust: panic! for unrecoverable errors",
        "Go: panic and recover for exceptional cases"
    ]
    
    with open("error_handling_comparison.txt", "w") as f:
        for approach in error_handling:
            f.write(f"{approach}\n")
    
    # Concurrency models
    concurrency_models = [
        "Zig: Async/await with event loops",
        "Rust: async/await with futures and tokio",
        "Go: Goroutines and channels",
        "Zig: Suspending and resuming functions",
        "Rust: Send/Sync traits for thread safety",
        "Go: Share memory by communicating",
        "Zig: Comptime async frame allocation",
        "Rust: Zero-cost abstractions for async",
        "Go: M:N threading model with scheduler"
    ]
    
    with open("concurrency_comparison.txt", "w") as f:
        for model in concurrency_models:
            f.write(f"{model}\n")

def main():
    """Main function to create all language datasets"""
    os.chdir("datasets")
    
    print("Creating Zig datasets...")
    create_zig_datasets()
    
    print("Creating Rust datasets...")
    create_rust_datasets()
    
    print("Creating Go datasets...")
    create_go_datasets()
    
    print("Creating language comparison datasets...")
    create_language_comparison()
    
    print("\nCreated language-specific datasets:")
    
    zig_files = ["zig_keywords.txt", "zig_builtins.txt", "zig_std_modules.txt", "zig_patterns.txt"]
    rust_files = ["rust_keywords.txt", "rust_std_types.txt", "rust_macros.txt", "rust_patterns.txt"]
    go_files = ["go_keywords.txt", "go_std_packages.txt", "go_builtins.txt", "go_patterns.txt"]
    comparison_files = ["memory_management_comparison.txt", "error_handling_comparison.txt", "concurrency_comparison.txt"]
    
    print("\nZig datasets:")
    for file in zig_files:
        print(f"  - {file}")
    
    print("\nRust datasets:")
    for file in rust_files:
        print(f"  - {file}")
    
    print("\nGo datasets:")
    for file in go_files:
        print(f"  - {file}")
    
    print("\nComparison datasets:")
    for file in comparison_files:
        print(f"  - {file}")

if __name__ == "__main__":
    main()
