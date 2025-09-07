# Ruby Programming Language Patterns

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
    email.match?(/^[\w+\-.]+@[a-z\d\-]+\.[a-z\d\-]+\*\.[a-z]+$/i)
  end
  
  def valid_password?(password)
    password.length >= 8 && password.match?(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/)
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
