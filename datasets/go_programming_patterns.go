# Go Programming Language Patterns

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
