import os
import json
import base64
import atexit
import secrets
import shutil
import glob
from datetime import datetime
from cryptography.hazmat.primitives import hashes, serialization, constant_time
from cryptography.hazmat.primitives.asymmetric import ec, rsa
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.backends import default_backend

class SecureStorage:
    def __init__(self, filename="temp_secure_data.db"):
        self.filename = filename
        self.backup_dir = "backups"
        self.backend = default_backend()
        self.data = []
        self.private_key = None
        self.public_key = None
        self._create_backup_dir()
        self._generate_or_load_keys()
        self.load_data()
        atexit.register(self.save_data)
    
    def _create_backup_dir(self):
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)
    
    def _manage_backups(self):
        backup_pattern = os.path.join(self.backup_dir, "secure_data_*.enc")
        backup_files = sorted(glob.glob(backup_pattern))
        
        while len(backup_files) >= 10:
            oldest_backup = backup_files.pop(0)
            os.remove(oldest_backup)
    
    def _create_backup(self):
        if os.path.exists(self.filename):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = os.path.join(self.backup_dir, f"secure_data_{timestamp}.enc")
            shutil.copy2(self.filename, backup_filename)
            self._manage_backups()
    
    def _ensure_keys(self):
        # Generate runtime keys - never save to disk
        if not hasattr(self, 'private_key') or self.private_key is None:
            password = os.urandom(32)  # Generate random password each session
            
            # Generate keys in memory only
            self.private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048,
                backend=default_backend()
            )
            self.public_key = self.private_key.public_key()
            self.key_password = password
    
    def _derive_key(self, shared_key, salt=None):
        if salt is None:
            salt = secrets.token_bytes(32)
        return HKDF(
            algorithm=hashes.SHA512(),
            length=32,
            salt=salt,
            info=b'chacha20poly1305-file-encryption-v2',
            backend=self.backend
        ).derive(shared_key), salt
    
    def encrypt_data(self, data_bytes):
        ephemeral_private_key = ec.generate_private_key(ec.SECP521R1(), self.backend)
        ephemeral_public_key = ephemeral_private_key.public_key()
        
        shared_key = ephemeral_private_key.exchange(ec.ECDH(), self.public_key)
        derived_key, salt = self._derive_key(shared_key)
        
        nonce = secrets.token_bytes(12)
        cipher = ChaCha20Poly1305(derived_key)
        encrypted_data = cipher.encrypt(nonce, data_bytes, None)
        
        ephemeral_public_bytes = ephemeral_public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        
        encrypted_package = {
            'ephemeral_public_key': base64.b64encode(ephemeral_public_bytes).decode('utf-8'),
            'salt': base64.b64encode(salt).decode('utf-8'),
            'nonce': base64.b64encode(nonce).decode('utf-8'),
            'encrypted_data': base64.b64encode(encrypted_data).decode('utf-8')
        }
        
        return base64.b64encode(json.dumps(encrypted_package).encode()).decode()
    
    def decrypt_data(self, encrypted_string):
        try:
            encrypted_package = json.loads(base64.b64decode(encrypted_string).decode())
            
            ephemeral_public_bytes = base64.b64decode(encrypted_package['ephemeral_public_key'])
            ephemeral_public_key = serialization.load_pem_public_key(ephemeral_public_bytes, backend=self.backend)
            
            shared_key = self.private_key.exchange(ec.ECDH(), ephemeral_public_key)
            salt = base64.b64decode(encrypted_package['salt'])
            derived_key, _ = self._derive_key(shared_key, salt)
            
            nonce = base64.b64decode(encrypted_package['nonce'])
            encrypted_data = base64.b64decode(encrypted_package['encrypted_data'])
            
            cipher = ChaCha20Poly1305(derived_key)
            data_bytes = cipher.decrypt(nonce, encrypted_data, None)
            
            return data_bytes
        except Exception as e:
            print(f"Decryption failed: {e}")
            return b''
    
    def save_data(self):
        try:
            self._create_backup()
            json_data = json.dumps(self.data, indent=2)
            data_bytes = json_data.encode('utf-8')
            encrypted_string = self.encrypt_data(data_bytes)
            
            with open(self.filename, 'w') as f:
                f.write(encrypted_string)
        except Exception as e:
            print(f"Save failed: {e}")
    
    def load_data(self):
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r') as f:
                    encrypted_string = f.read()
                
                if encrypted_string.strip():
                    decrypted_bytes = self.decrypt_data(encrypted_string)
                    if decrypted_bytes:
                        json_data = decrypted_bytes.decode('utf-8')
                        self.data = json.loads(json_data)
                    else:
                        self.data = []
                else:
                    self.data = []
            else:
                self.data = []
        except Exception as e:
            print(f"Load failed: {e}")
            self.data = []
    
    def get_data(self):
        return self.data
    
    def set_data(self, new_data):
        self.data = new_data
    
    def add_record(self, record):
        self.data.append(record)
    
    def clear_data(self):
        self.data = []
    
    def restore_from_backup(self, backup_filename):
        try:
            backup_path = os.path.join(self.backup_dir, backup_filename)
            if os.path.exists(backup_path):
                shutil.copy2(backup_path, self.filename)
                self.load_data()
                return True
            return False
        except Exception as e:
            print(f"Restore failed: {e}")
            return False
    
    def list_backups(self):
        backup_pattern = os.path.join(self.backup_dir, "secure_data_*.enc")
        backup_files = sorted(glob.glob(backup_pattern), reverse=True)
        return [os.path.basename(f) for f in backup_files]

storage = SecureStorage()
