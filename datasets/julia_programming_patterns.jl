# Julia Programming Language Patterns

# Type Definitions
struct User
    id::String
    name::String
    email::String
    created_at::DateTime
    
    function User(name::String, email::String)
        new(generate_id(), name, email, now())
    end
end

mutable struct UserService
    database::Any
    cache::Dict{String, User}
    
    UserService(database) = new(database, Dict{String, User}())
end

# Abstract Types and Interfaces
abstract type Processor end

struct DataProcessor <: Processor
    config::Dict{String, Any}
end

# Function Definitions
function full_name(user::User)::String
    return "$(user.name) <$(user.email)>"
end

function age_in_days(user::User)::Int
    return Dates.value(now() - user.created_at) ÷ (1000 * 60 * 60 * 24)
end

function is_valid_email(email::String)::Bool
    email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return occursin(email_regex, email)
end

function generate_id()::String
    return string("user_", time_ns(), "_", rand(1000:9999))
end

# Multiple Dispatch Examples
process(data::String) = uppercase(data)
process(data::Vector{String}) = [uppercase(s) for s in data]
process(data::Dict) = Dict(k => process(v) for (k, v) in data)

function calculate_sum(a::Number, b::Number)::Number
    return a + b
end

function calculate_sum(arrays::Vector{T}) where T <: Number
    return sum(arrays)
end

# Array and Collection Operations
users = [
    (name="Alice", email="alice@example.com", age=25),
    (name="Bob", email="bob@example.com", age=30),
    (name="Charlie", email="charlie@example.com", age=35)
]

# Functional Programming Patterns
adult_users = filter(user -> user.age >= 18, users)
user_names = map(user -> user.name, users)
total_age = reduce(+, [user.age for user in users])

# List Comprehensions
squared_ages = [user.age^2 for user in users]
adult_names = [user.name for user in users if user.age >= 18]

# Higher-order Functions
function apply_to_users(func::Function, users::Vector)
    return [func(user) for user in users]
end

function process_users(users::Vector, callback::Function)
    for user in users
        callback(user)
    end
end

process_users(users) do user
    println("Processing user: $(user.name)")
end

# Method Definitions for Custom Types
function create_user(service::UserService, name::String, email::String)
    if !is_valid_email(email)
        return (error="Invalid email format",)
    end
    
    user = User(name, email)
    service.cache[user.id] = user
    
    return (success=true, user=user)
end

# Error Handling
function divide_numbers(a::Number, b::Number)
    try
        if b == 0
            throw(DivisionError("Cannot divide by zero"))
        end
        
        result = a / b
        println("Result: $result")
        return result
        
    catch e
        if isa(e, DivisionError)
            println("Error: $(e.msg)")
        else
            println("Unexpected error: $e")
        end
        return nothing
    finally
        println("Division operation completed")
    end
end

# Parametric Types
struct Container{T}
    value::T
    timestamp::DateTime
    
    Container{T}(value::T) where T = new(value, now())
end

function get_value(container::Container{T})::T where T
    return container.value
end

# Broadcasting
numbers = [1, 2, 3, 4, 5]
squared = numbers .^ 2
added = numbers .+ 10

# Performance Annotations
function fast_calculation(data::Vector{Float64})
    @inbounds begin
        total = 0.0
        for i in 1:length(data)
            total += data[i] * 2.0
        end
        return total
    end
end

# Unit Testing Patterns
using Test

@testset "User Tests" begin
    @testset "User Creation" begin
        user = User("Alice", "alice@example.com")
        @test user.name == "Alice"
        @test user.email == "alice@example.com"
        @test length(user.id) > 0
    end
    
    @testset "Email Validation" begin
        @test is_valid_email("test@example.com") == true
        @test is_valid_email("invalid-email") == false
    end
end
