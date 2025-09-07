#!/usr/bin/env python3

import os
import time

def create_programming_language_datasets():
    """Create comprehensive datasets for Go, Perl, Ruby, PHP, and Julia programming languages."""
    
    datasets_dir = "/Users/mac/Desktop/sig-sql/datasets"
    
    # Go Programming Datasets
    go_syntax_patterns = """# Go Programming Language Syntax Patterns

# Package Declaration and Imports
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

type Repository interface {
    Create(user User) error
    GetByID(id int) (User, error)
    Update(user User) error
    Delete(id int) error
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

func processJobs(jobCount int) []int {
    jobs := make(chan int, jobCount)
    results := make(chan int, jobCount)
    
    for w := 1; w <= 3; w++ {
        go worker(jobs, results)
    }
    
    for j := 1; j <= jobCount; j++ {
        jobs <- j
    }
    close(jobs)
    
    var output []int
    for r := 1; r <= jobCount; r++ {
        result := <-results
        output = append(output, result)
    }
    
    return output
}

# Context Usage
func processWithContext(ctx context.Context, data []string) error {
    for _, item := range data {
        select {
        case <-ctx.Done():
            return ctx.Err()
        default:
            if err := processItem(item); err != nil {
                return err
            }
        }
    }
    return nil
}

# Testing Patterns
func TestCalculateSum(t *testing.T) {
    tests := []struct {
        name     string
        a, b     int
        expected int
    }{
        {"positive numbers", 2, 3, 5},
        {"negative numbers", -2, -3, -5},
        {"mixed numbers", -2, 3, 1},
    }
    
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            result := calculateSum(tt.a, tt.b)
            if result != tt.expected {
                t.Errorf("calculateSum(%d, %d) = %d; want %d", tt.a, tt.b, result, tt.expected)
            }
        })
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
    
    # Ruby Programming Datasets
    ruby_syntax_patterns = """# Ruby Programming Language Syntax Patterns

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
    email.match?(/\\A[\\w+\\-.]+@[a-z\\d\\-]+\\.[a-z\\d\\-]+\\*\\.[a-z]+\\z/i)
  end
  
  def valid_password?(password)
    password.length >= 8 && password.match?(/\\A(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)/)
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
  
  def find_user(id)
    @cache[id] || @database.find(id)
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

# String Interpolation and Methods
greeting = "Hello, #{user[:name]}!"
formatted_email = %Q(Email: "#{user[:email]}")
multiline_text = <<~TEXT
  This is a multiline string
  that preserves indentation
  and formatting.
TEXT

# Regular Expressions
def extract_domain(email)
  match = email.match(/@(.+)$/)
  match ? match[1] : nil
end

def sanitize_phone(phone)
  phone.gsub(/\D/, '')
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

# File Operations
def read_config_file(filename)
  File.open(filename, 'r') do |file|
    YAML.load(file)
  end
rescue Errno::ENOENT
  puts "Config file not found: #{filename}"
  {}
end

def write_log(message)
  File.open('application.log', 'a') do |file|
    file.puts "[#{Time.now}] #{message}"
  end
end

# Metaprogramming
class DynamicClass
  def self.define_getter(name)
    define_method(name) do
      instance_variable_get("@#{name}")
    end
  end
  
  def self.define_setter(name)
    define_method("#{name}=") do |value|
      instance_variable_set("@#{name}", value)
    end
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
  
  def current_user
    @current_user
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

# Testing with RSpec
describe User do
  let(:user) { User.new("Alice", "alice@example.com") }
  
  describe "#full_name" do
    it "returns formatted name and email" do
      expect(user.full_name).to eq("Alice <alice@example.com>")
    end
  end
  
  describe "#age_in_days" do
    it "calculates age in days" do
      expect(user.age_in_days).to be >= 0
    end
  end
end
"""
    
    # PHP Programming Datasets
    php_syntax_patterns = r"""<?php
// PHP Programming Language Syntax Patterns

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
    
    public function getAgeInDays() {
        $now = new DateTime();
        $diff = $now->diff($this->createdAt);
        return $diff->days;
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
    
    public function __toString() {
        return json_encode($this->toArray());
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
    
    protected function validateRequired($fields, $data) {
        $missing = [];
        foreach ($fields as $field) {
            if (!isset($data[$field]) || empty($data[$field])) {
                $missing[] = $field;
            }
        }
        return $missing;
    }
}

// Concrete Implementation
class UserController extends BaseController {
    private $userRepository;
    
    public function __construct($request, $response, UserRepositoryInterface $userRepository) {
        parent::__construct($request, $response);
        $this->userRepository = $userRepository;
    }
    
    public function index() {
        try {
            $users = $this->userRepository->findAll();
            return $this->jsonResponse(['users' => $users]);
        } catch (Exception $e) {
            return $this->jsonResponse(['error' => $e->getMessage()], 500);
        }
    }
    
    public function show($id) {
        try {
            $user = $this->userRepository->findById($id);
            if (!$user) {
                return $this->jsonResponse(['error' => 'User not found'], 404);
            }
            return $this->jsonResponse(['user' => $user->toArray()]);
        } catch (Exception $e) {
            return $this->jsonResponse(['error' => $e->getMessage()], 500);
        }
    }
    
    public function create() {
        try {
            $data = json_decode($this->request->getBody(), true);
            $missing = $this->validateRequired(['name', 'email'], $data);
            
            if (!empty($missing)) {
                return $this->jsonResponse([
                    'error' => 'Missing required fields',
                    'missing' => $missing
                ], 400);
            }
            
            $user = new User($data['name'], $data['email']);
            $this->userRepository->save($user);
            
            return $this->jsonResponse([
                'message' => 'User created successfully',
                'user' => $user->toArray()
            ], 201);
            
        } catch (InvalidArgumentException $e) {
            return $this->jsonResponse(['error' => $e->getMessage()], 400);
        } catch (Exception $e) {
            return $this->jsonResponse(['error' => 'Internal server error'], 500);
        }
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

$totalAge = array_reduce($users, function($carry, $user) {
    return $carry + $user['age'];
}, 0);

// String Operations
function formatUserInfo($user) {
    $name = ucfirst(strtolower($user['name']));
    $email = strtolower($user['email']);
    return sprintf("%s <%s>", $name, $email);
}

function extractDomain($email) {
    $parts = explode('@', $email);
    return isset($parts[1]) ? $parts[1] : null;
}

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
    
    public function fetchAll($sql, $params = []) {
        return $this->query($sql, $params)->fetchAll();
    }
    
    public function fetchOne($sql, $params = []) {
        return $this->query($sql, $params)->fetch();
    }
}

// Error Handling
function divideNumbers($a, $b) {
    try {
        if ($b == 0) {
            throw new DivisionByZeroError("Cannot divide by zero");
        }
        
        $result = $a / $b;
        echo "Result: " . $result . "\n";
        return $result;
        
    } catch (DivisionByZeroError $e) {
        echo "Error: " . $e->getMessage() . "\n";
        return null;
    } catch (Exception $e) {
        echo "Unexpected error: " . $e->getMessage() . "\n";
        return null;
    } finally {
        echo "Division operation completed\n";
    }
}

// File Operations
function readConfigFile($filename) {
    if (!file_exists($filename)) {
        throw new Exception("Config file not found: {$filename}");
    }
    
    $content = file_get_contents($filename);
    $config = json_decode($content, true);
    
    if (json_last_error() !== JSON_ERROR_NONE) {
        throw new Exception("Invalid JSON in config file");
    }
    
    return $config;
}

function writeLog($message) {
    $timestamp = date('Y-m-d H:i:s');
    $logEntry = "[{$timestamp}] {$message}\n";
    file_put_contents('application.log', $logEntry, FILE_APPEND | LOCK_EX);
}

// Namespace Example
namespace App\Services;

use App\Models\User;
use App\Repositories\UserRepositoryInterface;

class UserService {
    private $userRepository;
    
    public function __construct(UserRepositoryInterface $userRepository) {
        $this->userRepository = $userRepository;
    }
    
    public function createUser($name, $email) {
        $user = new User($name, $email);
        return $this->userRepository->save($user);
    }
    
    public function getUserById($id) {
        return $this->userRepository->findById($id);
    }
}
?>"""
    
    # Perl Programming Datasets
    perl_syntax_patterns = """#!/usr/bin/perl
# Perl Programming Language Syntax Patterns

use strict;
use warnings;
use feature 'say';
use Data::Dumper;
use JSON;
use DBI;
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

sub set_email {
    my ($self, $email) = @_;
    if (is_valid_email($email)) {
        $self->{email} = $email;
    } else {
        die "Invalid email format: $email";
    }
}

sub full_name {
    my $self = shift;
    return $self->{name} . ' <' . $self->{email} . '>';
}

sub age_in_days {
    my $self = shift;
    my $now = DateTime->now();
    my $duration = $now - $self->{created_at};
    return $duration->days;
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
    return $email =~ /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
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

sub find_user {
    my ($self, $id) = @_;
    return $self->{cache}->{$id} || $self->{database}->find($id);
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

my $total_age = 0;
$total_age += $_->{age} for @users;

# Subroutines
sub process_users {
    my ($users_ref, $callback) = @_;
    for my $user (@$users_ref) {
        $callback->($user) if $callback;
    }
}

process_users(\@users, sub {
    my $user = shift;
    say "Processing user: " . $user->{name};
});

# String Operations
sub format_user_info {
    my $user = shift;
    my $name = ucfirst(lc($user->{name}));
    my $email = lc($user->{email});
    return "$name <$email>";
}

sub extract_domain {
    my $email = shift;
    if ($email =~ /@(.+)$/) {
        return $1;
    }
    return undef;
}

# Regular Expressions
sub sanitize_phone {
    my $phone = shift;
    $phone =~ s/\D//g;
    return $phone;
}

sub validate_password {
    my $password = shift;
    return length($password) >= 8 && 
           $password =~ /[a-z]/ && 
           $password =~ /[A-Z]/ && 
           $password =~ /\d/;
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

sub write_log {
    my $message = shift;
    my $timestamp = localtime();
    
    open my $fh, '>>', 'application.log' or die "Cannot open log file: $!";
    say $fh "[$timestamp] $message";
    close $fh;
}

# Database Operations
sub connect_database {
    my ($host, $database, $username, $password) = @_;
    
    my $dsn = "DBI:mysql:database=$database;host=$host";
    my $dbh = DBI->connect($dsn, $username, $password, {
        RaiseError => 1,
        PrintError => 0,
        AutoCommit => 1,
    }) or die "Database connection failed: " . DBI->errstr;
    
    return $dbh;
}

sub fetch_users {
    my $dbh = shift;
    my $sql = "SELECT id, name, email, created_at FROM users WHERE active = ?";
    my $sth = $dbh->prepare($sql);
    $sth->execute(1);
    
    my @users;
    while (my $row = $sth->fetchrow_hashref) {
        push @users, $row;
    }
    
    return \@users;
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
    users => \@users,
    count => scalar @users,
    stats => {
        total_age => $total_age,
        average_age => $total_age / scalar @users,
    }
};

# Dereferencing
for my $user (@{$user_data->{users}}) {
    say "User: " . $user->{name};
}

# Anonymous Subroutines
my $processor = sub {
    my $data = shift;
    return uc($data);
};

my $result = $processor->("hello world");

# Context-sensitive Operations
my @names_array = get_names();  # List context
my $names_count = get_names();  # Scalar context

sub get_names {
    my @names = ("Alice", "Bob", "Charlie");
    return wantarray ? @names : scalar @names;
}

# Module Usage Example
package Logger;

use Exporter 'import';
our @EXPORT_OK = qw(log_info log_error log_debug);

sub log_info {
    my $message = shift;
    write_log("INFO: $message");
}

sub log_error {
    my $message = shift;
    write_log("ERROR: $message");
}

sub log_debug {
    my $message = shift;
    write_log("DEBUG: $message");
}

1; # End of module
"""
    
    # Julia Programming Datasets
    julia_syntax_patterns = """# Julia Programming Language Syntax Patterns

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

struct FileProcessor <: Processor
    file_path::String
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
    save_user(service.database, user)
    service.cache[user.id] = user
    
    return (success=true, user=user)
end

function find_user(service::UserService, id::String)
    return get(service.cache, id, nothing) ?? find_in_database(service.database, id)
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

# File Operations
function read_config_file(filename::String)
    if !isfile(filename)
        throw(ArgumentError("Config file not found: $filename"))
    end
    
    content = read(filename, String)
    return JSON.parse(content)
end

function write_log(message::String)
    timestamp = Dates.format(now(), "yyyy-mm-dd HH:MM:SS")
    log_entry = "[$timestamp] $message\n"
    open("application.log", "a") do file
        write(file, log_entry)
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

# Metaprogramming
macro log_function_call(func_call)
    quote
        println("Calling function: $($(string(func_call.args[1])))")
        result = $(esc(func_call))
        println("Function completed")
        result
    end
end

# Usage: @log_function_call calculate_sum(5, 3)

# Package and Module System
module UserManagement

export User, UserService, create_user, find_user

using Dates, JSON

# Include the definitions above

end # module

# Using modules
using .UserManagement

# Database Operations (conceptual)
function connect_database(host::String, database::String, username::String, password::String)
    # Simulated database connection
    return Dict("host" => host, "database" => database, "connected" => true)
end

function execute_query(db::Dict, query::String, params::Vector=[])
    # Simulated query execution
    println("Executing: $query with params: $params")
    return [Dict("id" => i, "name" => "User $i") for i in 1:3]
end

# Async Programming
function fetch_data_async(url::String)
    @async begin
        # Simulated async operation
        sleep(1)
        return "Data from $url"
    end
end

function process_multiple_urls(urls::Vector{String})
    tasks = [fetch_data_async(url) for url in urls]
    results = [fetch(task) for task in tasks]
    return results
end

# Broadcasting
numbers = [1, 2, 3, 4, 5]
squared = numbers .^ 2
added = numbers .+ 10

# Pattern Matching (using external package concept)
function handle_result(result)
    if haskey(result, :success) && result.success
        println("Operation successful: $(result.user.name)")
    elseif haskey(result, :error)
        println("Error occurred: $(result.error)")
    else
        println("Unknown result format")
    end
end

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
    
    @testset "Full Name Formatting" begin
        user = User("Bob", "bob@test.com")
        @test full_name(user) == "Bob <bob@test.com>"
    end
end
"""
    
    # Write all datasets
    datasets = {
        "go_programming_patterns.go": go_syntax_patterns,
        "ruby_programming_patterns.rb": ruby_syntax_patterns,
        "php_programming_patterns.php": php_syntax_patterns,
        "perl_programming_patterns.pl": perl_syntax_patterns,
        "julia_programming_patterns.jl": julia_syntax_patterns,
    }
    
    for filename, content in datasets.items():
        filepath = os.path.join(datasets_dir, filename)
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Created: {filename}")
    
    print(f"\nCreated {len(datasets)} comprehensive programming language datasets")
    print("Enhanced coverage for Go, Ruby, PHP, Perl, and Julia programming languages")

if __name__ == "__main__":
    create_programming_language_datasets()
