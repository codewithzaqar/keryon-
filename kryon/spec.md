# Kryon Language Specification v0.0.1

## 1. Overview
Kryon is a statically typed, compiled language. It emphasizes explicit control over memory layout while preventing common errors like null pointer dereferences and data races.

## 2. Syntax Basics
- **Indentation:** Significant whitespace (like Python) defines blocks.
- **Statements:** End with newlines. Semicolons are optional but discouraged.
- **Comments:** `//` for single-line, `/* */` for multi-line.

## 3. Data Types
- `i8`, `i16`, `i32`, `i64`: Signed integers
- `u8`, `u16`, `u32`, `u64`: Unsigned integers
- `f32`, `f64`: Floating point numbers
- `bool`: Boolean (`true`, `false`)
- `str`: Immutable UTF-8 string slice
- `T[]`: Array of type T
- `Option<T>`: Nullable type wrapper

## 4. Variables
Variables are immutable by default. Use `mut` to declare mutable variables.

```kryon
let x = 10      // Immutable
mut y = 20      // Mutable
y = 30          // Valid
x = 11          // Error: Cannot assign to immutable variable
```

## 5. Functions
Functions are defined with `fn`. Return types are specified after `->`.
```kryon
fn add(a: i32, b: i32) -> i32 {
    return a + b
}
```

## 6. Concurrency
Kryon uses `spawn` for lightweight threads and `async`/`await` for asynchronous tasks.
```kryon
async fn fetch_data(url: str) -> str {
    // ...
}

fn main() {
    let handle = spawn async {
        fetch_data("https://example.com")
    }
}
```