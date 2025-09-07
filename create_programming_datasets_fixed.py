#!/usr/bin/env python3

import os

def create_go_dataset():
    """Create Go programming language dataset."""
    content = """# Go Programming Language Patterns

package main

import (
    "fmt"
    "log"
    "net/http"
    "encoding/json"
    "time"
    "context"
    "sync"
)

# Variable Declarations
var globalVar string = "global"
const MaxRetries = 3

# Function Definitions
func calculateSum(a, b int) int {
    return a + b
}

func processData(data []string) (result []string, err error) {
    for _, item := range data {
        processed := strings.ToUpper(item)
        result = append(result, processed)
    }
    return result, nil
}

# Struct Definitions
type User struct {
    ID       int    `json:"id"`
    Name     string `json:"name"`
    Email    string `json:"email"`
    Created  time.Time `json:"created"`
}

type UserService struct {
    db       Database
    cache    Cache
    logger   Logger
    mutex    sync.RWMutex
}

# Interface Definitions
type Processor interface {
    Process(data []byte) ([]byte, error)
    Validate(input string) bool
}

# Method Definitions
func (u *User) FullName() string {
    return fmt.Sprintf("%s <%s>", u.Name, u.Email)
}

func (s *UserService) CreateUser(name, email string) (*User, error) {
    s.mutex.Lock()
    defer s.mutex.Unlock()
    
    user := &User{
        Name:    name,
        Email:   email,
        Created: time.Now(),
    }
    
    if err := s.db.Save(user); err != nil {
        return nil, fmt.Errorf("failed to save user: %w", err)
    }
    
    return user, nil
}

# Error Handling Patterns
func fetchData(url string) ([]byte, error) {
    resp, err := http.Get(url)
    if err != nil {
        return nil, fmt.Errorf("failed to fetch data: %w", err)
    }
    defer resp.Body.Close()
    
    if resp.StatusCode != http.StatusOK {
        return nil, fmt.Errorf("unexpected status code: %d", resp.StatusCode)
    }
    
    return io.ReadAll(resp.Body)
}

# Goroutines and Channels
func worker(jobs <-chan int, results chan<- int) {
    for job := range jobs {
        time.Sleep(time.Millisecond * 100)
        results <- job * 2
    }
}

# HTTP Server Patterns
func handleUser(w http.ResponseWriter, r *http.Request) {
    switch r.Method {
    case http.MethodGet:
        getUserHandler(w, r)
    case http.MethodPost:
        createUserHandler(w, r)
    case http.MethodPut:
        updateUserHandler(w, r)
    case http.MethodDelete:
        deleteUserHandler(w, r)
    default:
        http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
    }
}

func startServer() {
    mux := http.NewServeMux()
    mux.HandleFunc("/users", handleUser)
    mux.HandleFunc("/health", healthCheck)
    
    server := &http.Server{
        Addr:         ":8080",
        Handler:      mux,
        ReadTimeout:  15 * time.Second,
        WriteTimeout: 15 * time.Second,
    }
    
    log.Printf("Server starting on %s", server.Addr)
    log.Fatal(server.ListenAndServe())
}
"""
    return content

def create_ruby_dataset():
    """Create Ruby programming language dataset."""
    content = """# Ruby Programming Language Patterns

# Class Definitions
class User
  attr_accessor :name, :email, :created_at
  attr_reader :id
  
  def initialize(name, email)
    @name = name
    @email = email
    @created_at = Time.now
    @id = generate_id
  end
  
  def full_name
    "#{@name} <#{@email}>"
  end
  
  def age_in_days
    (Time.now - @created_at) / (24 * 60 * 60)
  end
  
  private
  
  def generate_id
    SecureRandom.uuid
  end
end

# Module Definitions
module Validatable
  def valid_email?(email)
    email.match?(/^[\\w+\\-.]+@[a-z\\d\\-]+\\.[a-z\\d\\-]+\\*\\.[a-z]+$/i)
  end
  
  def valid_password?(password)
    password.length >= 8 && password.match?(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)/)
  end
end

class UserService
  include Validatable
  
  def initialize(database)
    @database = database
    @cache = {}
  end
  
  def create_user(name, email, password)
    return { error: "Invalid email" } unless valid_email?(email)
    return { error: "Invalid password" } unless valid_password?(password)
    
    user = User.new(name, email)
    @database.save(user)
    @cache[user.id] = user
    
    { success: true, user: user }
  end
end

# Array and Hash Operations
users = [
  { name: "Alice", email: "alice@example.com", age: 25 },
  { name: "Bob", email: "bob@example.com", age: 30 },
  { name: "Charlie", email: "charlie@example.com", age: 35 }
]

# Enumerable Methods
adult_users = users.select { |user| user[:age] >= 18 }
user_names = users.map { |user| user[:name] }
total_age = users.sum { |user| user[:age] }

# Block Patterns
def process_users(&block)
  users.each do |user|
    yield(user) if block_given?
  end
end

process_users do |user|
  puts "Processing user: #{user[:name]}"
end

# Exception Handling
def divide_numbers(a, b)
  begin
    result = a / b
    puts "Result: #{result}"
  rescue ZeroDivisionError => e
    puts "Error: Cannot divide by zero"
  rescue StandardError => e
    puts "Error: #{e.message}"
  ensure
    puts "Division operation completed"
  end
end

# Rails-style Patterns
class ApplicationController
  before_action :authenticate_user
  before_action :set_current_user
  
  protected
  
  def authenticate_user
    redirect_to login_path unless session[:user_id]
  end
  
  def set_current_user
    @current_user = User.find(session[:user_id]) if session[:user_id]
  end
end

class UsersController < ApplicationController
  def index
    @users = User.all
  end
  
  def show
    @user = User.find(params[:id])
  end
  
  def create
    @user = User.new(user_params)
    
    if @user.save
      redirect_to @user, notice: 'User created successfully'
    else
      render :new
    end
  end
  
  private
  
  def user_params
    params.require(:user).permit(:name, :email, :password)
  end
end
"""
    return content

def create_php_dataset():
    """Create PHP programming language dataset."""
    content = """<?php
// PHP Programming Language Patterns

// Class Definitions
class User {
    private $id;
    private $name;
    private $email;
    private $createdAt;
    
    public function __construct($name, $email) {
        $this->name = $name;
        $this->email = $email;
        $this->createdAt = new DateTime();
        $this->id = $this->generateId();
    }
    
    public function getName() {
        return $this->name;
    }
    
    public function setName($name) {
        $this->name = $name;
    }
    
    public function getEmail() {
        return $this->email;
    }
    
    public function setEmail($email) {
        if ($this->isValidEmail($email)) {
            $this->email = $email;
        } else {
            throw new InvalidArgumentException("Invalid email format");
        }
    }
    
    public function getFullName() {
        return $this->name . ' <' . $this->email . '>';
    }
    
    private function isValidEmail($email) {
        return filter_var($email, FILTER_VALIDATE_EMAIL) !== false;
    }
    
    private function generateId() {
        return uniqid('user_', true);
    }
    
    public function toArray() {
        return [
            'id' => $this->id,
            'name' => $this->name,
            'email' => $this->email,
            'created_at' => $this->createdAt->format('Y-m-d H:i:s')
        ];
    }
}

// Interface Definitions
interface UserRepositoryInterface {
    public function save(User $user);
    public function findById($id);
    public function findByEmail($email);
    public function update(User $user);
    public function delete($id);
}

// Abstract Class
abstract class BaseController {
    protected $request;
    protected $response;
    
    public function __construct($request, $response) {
        $this->request = $request;
        $this->response = $response;
    }
    
    abstract public function index();
    abstract public function show($id);
    
    protected function jsonResponse($data, $statusCode = 200) {
        $this->response->setStatusCode($statusCode);
        $this->response->setHeader('Content-Type', 'application/json');
        return json_encode($data);
    }
}

// Array Operations
$users = [
    ['name' => 'Alice', 'email' => 'alice@example.com', 'age' => 25],
    ['name' => 'Bob', 'email' => 'bob@example.com', 'age' => 30],
    ['name' => 'Charlie', 'email' => 'charlie@example.com', 'age' => 35]
];

// Array Functions
$adultUsers = array_filter($users, function($user) {
    return $user['age'] >= 18;
});

$userNames = array_map(function($user) {
    return $user['name'];
}, $users);

// Database Operations with PDO
class DatabaseConnection {
    private $pdo;
    
    public function __construct($host, $dbname, $username, $password) {
        $dsn = "mysql:host={$host};dbname={$dbname};charset=utf8";
        $options = [
            PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
            PDO::ATTR_EMULATE_PREPARES => false
        ];
        
        $this->pdo = new PDO($dsn, $username, $password, $options);
    }
    
    public function query($sql, $params = []) {
        $stmt = $this->pdo->prepare($sql);
        $stmt->execute($params);
        return $stmt;
    }
}

// Error Handling
function divideNumbers($a, $b) {
    try {
        if ($b == 0) {
            throw new DivisionByZeroError("Cannot divide by zero");
        }
        
        $result = $a / $b;
        echo "Result: " . $result . "\\n";
        return $result;
        
    } catch (DivisionByZeroError $e) {
        echo "Error: " . $e->getMessage() . "\\n";
        return null;
    } finally {
        echo "Division operation completed\\n";
    }
}

// Namespace Example
namespace App\\Services;

use App\\Models\\User;
use App\\Repositories\\UserRepositoryInterface;

class UserService {
    private $userRepository;
    
    public function __construct(UserRepositoryInterface $userRepository) {
        $this->userRepository = $userRepository;
    }
    
    public function createUser($name, $email) {
        $user = new User($name, $email);
        return $this->userRepository->save($user);
    }
}
?>"""
    return content

def create_perl_dataset():
    """Create Perl programming language dataset."""
    content = """#!/usr/bin/perl
# Perl Programming Language Patterns

use strict;
use warnings;
use feature 'say';
use Data::Dumper;
use JSON;
use DateTime;

# Package and Class Definitions
package User;

sub new {
    my ($class, $name, $email) = @_;
    my $self = {
        id         => generate_id(),
        name       => $name,
        email      => $email,
        created_at => DateTime->now(),
    };
    bless $self, $class;
    return $self;
}

sub get_name {
    my $self = shift;
    return $self->{name};
}

sub set_name {
    my ($self, $name) = @_;
    $self->{name} = $name;
}

sub get_email {
    my $self = shift;
    return $self->{email};
}

sub full_name {
    my $self = shift;
    return $self->{name} . ' <' . $self->{email} . '>';
}

sub to_hash {
    my $self = shift;
    return {
        id         => $self->{id},
        name       => $self->{name},
        email      => $self->{email},
        created_at => $self->{created_at}->iso8601(),
    };
}

# Utility Functions
sub generate_id {
    return sprintf("user_%d_%d", time(), int(rand(10000)));
}

sub is_valid_email {
    my $email = shift;
    return $email =~ /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$/;
}

package UserService;

sub new {
    my ($class, $database) = @_;
    my $self = {
        database => $database,
        cache    => {},
    };
    bless $self, $class;
    return $self;
}

sub create_user {
    my ($self, $name, $email) = @_;
    
    unless (User::is_valid_email($email)) {
        return { error => "Invalid email format" };
    }
    
    my $user = User->new($name, $email);
    $self->{database}->save($user);
    $self->{cache}->{$user->{id}} = $user;
    
    return { success => 1, user => $user };
}

package main;

# Array and Hash Operations
my @users = (
    { name => "Alice",   email => "alice@example.com",   age => 25 },
    { name => "Bob",     email => "bob@example.com",     age => 30 },
    { name => "Charlie", email => "charlie@example.com", age => 35 },
);

# Array Processing
my @adult_users = grep { $_->{age} >= 18 } @users;
my @user_names = map { $_->{name} } @users;

# Subroutines
sub process_users {
    my ($users_ref, $callback) = @_;
    for my $user (@$users_ref) {
        $callback->($user) if $callback;
    }
}

process_users(\\@users, sub {
    my $user = shift;
    say "Processing user: " . $user->{name};
});

# Regular Expressions
sub sanitize_phone {
    my $phone = shift;
    $phone =~ s/\\D//g;
    return $phone;
}

sub validate_password {
    my $password = shift;
    return length($password) >= 8 && 
           $password =~ /[a-z]/ && 
           $password =~ /[A-Z]/ && 
           $password =~ /\\d/;
}

# File Operations
sub read_config_file {
    my $filename = shift;
    
    open my $fh, '<', $filename or die "Cannot open file '$filename': $!";
    local $/;
    my $content = <$fh>;
    close $fh;
    
    my $config = decode_json($content);
    return $config;
}

# Error Handling
sub divide_numbers {
    my ($a, $b) = @_;
    
    eval {
        die "Cannot divide by zero" if $b == 0;
        my $result = $a / $b;
        say "Result: $result";
        return $result;
    };
    
    if ($@) {
        warn "Error: $@";
        return undef;
    }
}

# Reference Operations
my $user_data = {
    users => \\@users,
    count => scalar @users,
};

# Module Usage Example
package Logger;

use Exporter 'import';
our @EXPORT_OK = qw(log_info log_error log_debug);

sub log_info {
    my $message = shift;
    print "INFO: $message\\n";
}

sub log_error {
    my $message = shift;
    print "ERROR: $message\\n";
}

1; # End of module
"""
    return content

def create_julia_dataset():
    """Create Julia programming language dataset."""
    content = """# Julia Programming Language Patterns

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
    email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
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
"""
    return content

def main():
    """Create all programming language datasets."""
    datasets_dir = "/Users/mac/Desktop/sig-sql/datasets"
    
    datasets = {
        "go_programming_patterns.go": create_go_dataset(),
        "ruby_programming_patterns.rb": create_ruby_dataset(),
        "php_programming_patterns.php": create_php_dataset(),
        "perl_programming_patterns.pl": create_perl_dataset(),
        "julia_programming_patterns.jl": create_julia_dataset(),
    }
    
    created_count = 0
    for filename, content in datasets.items():
        filepath = os.path.join(datasets_dir, filename)
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Created: {filename}")
            created_count += 1
        except Exception as e:
            print(f"Error creating {filename}: {e}")
    
    print(f"\\nSuccessfully created {created_count} programming language datasets")
    print("Enhanced coverage for Go, Ruby, PHP, Perl, and Julia programming languages")

if __name__ == "__main__":
    main()
