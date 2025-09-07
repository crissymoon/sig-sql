#!/usr/bin/perl
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

process_users(\@users, sub {
    my $user = shift;
    say "Processing user: " . $user->{name};
});

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
};

# Module Usage Example
package Logger;

use Exporter 'import';
our @EXPORT_OK = qw(log_info log_error log_debug);

sub log_info {
    my $message = shift;
    print "INFO: $message\n";
}

sub log_error {
    my $message = shift;
    print "ERROR: $message\n";
}

1; # End of module
