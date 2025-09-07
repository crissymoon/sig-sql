<?php
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
        echo "Result: " . $result . "\n";
        return $result;
        
    } catch (DivisionByZeroError $e) {
        echo "Error: " . $e->getMessage() . "\n";
        return null;
    } finally {
        echo "Division operation completed\n";
    }
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
}
?>