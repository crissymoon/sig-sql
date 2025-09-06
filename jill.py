# This is a custom NoSql designed by Crissy Deutsch, Still in dev and adding self testing and more fallbacks
import os; from datetime import datetime; import base64; import hashlib; import logging
import secrets; import json
try: # The lib is installed in the virtual environment
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.hazmat.primitives.asymmetric import ec
    from cryptography.hazmat.primitives.kdf.hkdf import HKDF
    from cryptography.hazmat.backends import default_backend
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False
    print("Advanced encryption requires 'cryptography' package. Install with: pip install cryptography")
    print("Falling back to basic XOR encryption for now.")

debug_dir = os.path.join(os.path.dirname(__file__), 'debug')
os.makedirs(debug_dir, exist_ok=True)
# Creates a Debug log file in the debug dir
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
                    handlers=[logging.FileHandler(os.path.join(debug_dir, 'jill_debug.log')), logging.StreamHandler() if __name__ == "__main__" else logging.NullHandler()])
logger = logging.getLogger('DataQueen')

class DataQueen:
    def __init__(self, auto_delimiter_choice=None, encryption_method=None):
        logger.info("Initializing DataQueen File Handler")
        self.data_folder = "jill_data"
        self.debug_folder = "debug"
        os.makedirs(self.data_folder, exist_ok=True)
        os.makedirs(self.debug_folder, exist_ok=True)
        
        if auto_delimiter_choice:
            self.delimiter_choice = str(auto_delimiter_choice)
            logger.info(f"Using auto-delimiter choice: {self.delimiter_choice}")
        else:
            print("File Handler Service - Choose Your Delimiter Style:")
            print("1. Pipe Delimited (|) - Classic & Clean")
            print("2. CSV Format (,) - Spreadsheet Friendly") 
            print("3. Special Control Chars - Advanced Security")
            self.delimiter_choice = input("Select your delimiter option (1-3): ").strip()
        
        if encryption_method:
            self.encryption_method = str(encryption_method)
            logger.info(f"Using auto-encryption method: {self.encryption_method}")
        else:
            print("\nEncryption Security Level - Choose Your Protection:")
            print("1. Basic XOR (Fast & Simple)")
            if CRYPTO_AVAILABLE:
                print("2. AES-256 with Salt (Strong & Secure)")
                print("3. ECC + AES Hybrid (Maximum Security)")
            else:
                print("2. AES-256 with Salt (Requires cryptography package)")
                print("3. ECC + AES Hybrid (Requires cryptography package)")
            self.encryption_method = input("Select encryption method (1-3): ").strip()
        
        self.delimiter = self._get_delimiter()
        self.current_files = {}
        self.encryption_key = self._generate_master_key()
        self.salt = self._generate_salt()
        self.sensitive_fields = {'password', 'pass', 'pwd', 'secret', 'token', 'key'}
        
        if self.encryption_method == '3' and CRYPTO_AVAILABLE:
            self.private_key, self.public_key = self._generate_ecc_keypair()
            logger.info("ECC keypair generated for maximum security")
            
    def _get_file_path(self, filename):
        return os.path.join(self.data_folder, filename)
        
    def _generate_master_key(self):
        try:
            machine_id = str(hash(os.path.expanduser('~')))
            app_seed = "DataQueen2025_JackNJill_Fixed"
            combined = f"{machine_id}{app_seed}".encode()
            key_hash = hashlib.sha256(combined).digest()
            logger.info("Master encryption key generated successfully")
            return base64.urlsafe_b64encode(key_hash[:32])
        except Exception as e:
            logger.error(f"Failed to generate encryption key: {e}")
            fallback_data = "DataQueenSecureKey2025!@#$%^&*()FIXED"
            return base64.urlsafe_b64encode(hashlib.sha256(fallback_data.encode()).digest()[:32])
    
    def _generate_salt(self):
        try:
            salt = secrets.token_bytes(32)
            logger.info("Cryptographic salt generated successfully")
            return base64.urlsafe_b64encode(salt)
        except Exception as e:
            logger.error(f"Failed to generate salt: {e}")
            fallback_salt = hashlib.sha256(b"DataQueenSalt2025_Secure").digest()
            return base64.urlsafe_b64encode(fallback_salt)
    
    def _generate_ecc_keypair(self):
        if not CRYPTO_AVAILABLE:
            logger.error("ECC encryption requires cryptography package")
            return None, None
        try:
            private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())
            public_key = private_key.public_key()
            logger.info("ECC keypair generated successfully")
            return private_key, public_key
        except Exception as e:
            logger.error(f"Failed to generate ECC keypair: {e}")
            return None, None
    
    def _derive_key_with_salt(self, password, salt):
        if not CRYPTO_AVAILABLE:
            logger.warning("Advanced key derivation requires cryptography package, using basic method")
            return self._generate_master_key()
        try:
            kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=base64.urlsafe_b64decode(salt), 
                           iterations=100000, backend=default_backend())
            key = kdf.derive(password.encode() if isinstance(password, str) else password)
            logger.debug("Key derived successfully with PBKDF2")
            return base64.urlsafe_b64encode(key)
        except Exception as e:
            logger.error(f"Key derivation failed: {e}")
            return self._generate_master_key()
    
    def _aes_encrypt(self, data, key, salt):
        if not CRYPTO_AVAILABLE:
            logger.warning("AES encryption requires cryptography package, falling back to XOR")
            return self._simple_encrypt(data, key)
        try:
            if not data: return data
            data_bytes = str(data).encode('utf-8')
            derived_key = self._derive_key_with_salt(base64.urlsafe_b64decode(key), salt)
            key_bytes = base64.urlsafe_b64decode(derived_key)
            iv = secrets.token_bytes(12)
            cipher = Cipher(algorithms.AES(key_bytes), modes.GCM(iv), backend=default_backend())
            encryptor = cipher.encryptor()
            ciphertext = encryptor.update(data_bytes) + encryptor.finalize()
            encrypted_data = iv + encryptor.tag + ciphertext
            result = base64.urlsafe_b64encode(encrypted_data).decode('utf-8')
            logger.debug(f"AES encrypted data length: {len(result)}")
            return result
        except Exception as e:
            logger.error(f"AES encryption failed: {e}")
            return self._simple_encrypt(data, key)
    
    def _aes_decrypt(self, encrypted_data, key, salt):
        if not CRYPTO_AVAILABLE:
            logger.warning("AES decryption requires cryptography package, falling back to XOR")
            return self._simple_decrypt(encrypted_data, key)
        try:
            if not encrypted_data or not str(encrypted_data).startswith('AES_'): return encrypted_data
            clean_data = str(encrypted_data)[4:]
            encrypted_bytes = base64.urlsafe_b64decode(clean_data.encode('utf-8'))
            iv, tag, ciphertext = encrypted_bytes[:12], encrypted_bytes[12:28], encrypted_bytes[28:]
            derived_key = self._derive_key_with_salt(base64.urlsafe_b64decode(key), salt)
            key_bytes = base64.urlsafe_b64decode(derived_key)
            cipher = Cipher(algorithms.AES(key_bytes), modes.GCM(iv, tag), backend=default_backend())
            decryptor = cipher.decryptor()
            decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()
            result = decrypted_data.decode('utf-8')
            logger.debug(f"AES decrypted data successfully: {len(result)} chars")
            return result
        except Exception as e:
            logger.error(f"AES decryption failed: {e}")
            return self._simple_decrypt(encrypted_data, key)
    
    def _ecc_hybrid_encrypt(self, data, public_key): # Do not concise this logic, it is very complex
        if not CRYPTO_AVAILABLE or not public_key:
            logger.warning("ECC encryption requires cryptography package and keys, falling back to AES")
            return self._aes_encrypt(data, self.encryption_key, self.salt)
        try:
            if not data: return data
            data_bytes = str(data).encode('utf-8')
            
            ephemeral_private = ec.generate_private_key(ec.SECP256R1(), default_backend())
            ephemeral_public = ephemeral_private.public_key()
            
            shared_key = ephemeral_private.exchange(ec.ECDH(), public_key)
            
            derived_key = HKDF(
                algorithm=hashes.SHA256(),
                length=32,
                salt=base64.urlsafe_b64decode(self.salt),
                info=b'DataQueen ECC Hybrid',
                backend=default_backend()
            ).derive(shared_key)
            
            iv = secrets.token_bytes(12)
        
            cipher = Cipher(algorithms.AES(derived_key), modes.GCM(iv), backend=default_backend())
            encryptor = cipher.encryptor()
            ciphertext = encryptor.update(data_bytes) + encryptor.finalize()
            
            ephemeral_public_bytes = ephemeral_public.public_bytes(
                encoding=serialization.Encoding.X962,
                format=serialization.PublicFormat.UncompressedPoint
            )
            
            encrypted_data = ephemeral_public_bytes + iv + encryptor.tag + ciphertext
            result = base64.urlsafe_b64encode(encrypted_data).decode('utf-8')
            
            logger.debug(f"ECC hybrid encrypted data length: {len(result)}")
            return result
        except Exception as e:
            logger.error(f"ECC hybrid encryption failed: {e}")
            return self._aes_encrypt(data, self.encryption_key, self.salt)
    
    def _ecc_hybrid_decrypt(self, encrypted_data, private_key):
        if not CRYPTO_AVAILABLE or not private_key:
            logger.warning("ECC decryption requires cryptography package and keys, falling back to AES")
            return self._aes_decrypt(encrypted_data, self.encryption_key, self.salt)
        try:
            if not encrypted_data or not str(encrypted_data).startswith('ECC_'):
                return encrypted_data
            
            clean_data = str(encrypted_data)[4:]
            encrypted_bytes = base64.urlsafe_b64decode(clean_data.encode('utf-8'))
            
            ephemeral_public_bytes = encrypted_bytes[:65]
            iv = encrypted_bytes[65:77]
            tag = encrypted_bytes[77:93]
            ciphertext = encrypted_bytes[93:]
            
            ephemeral_public = ec.EllipticCurvePublicKey.from_encoded_point(
                ec.SECP256R1(), ephemeral_public_bytes
            )
            
            shared_key = private_key.exchange(ec.ECDH(), ephemeral_public)
            
            derived_key = HKDF(
                algorithm=hashes.SHA256(),
                length=32,
                salt=base64.urlsafe_b64decode(self.salt),
                info=b'DataQueen ECC Hybrid',
                backend=default_backend()
            ).derive(shared_key)
            
            cipher = Cipher(algorithms.AES(derived_key), modes.GCM(iv, tag), backend=default_backend())
            decryptor = cipher.decryptor()
            decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()
            
            result = decrypted_data.decode('utf-8')
            logger.debug(f"ECC hybrid decrypted data successfully: {len(result)} chars")
            return result
        except Exception as e:
            logger.error(f"ECC hybrid decryption failed: {e}")
            return self._aes_decrypt(encrypted_data, self.encryption_key, self.salt)
    
    def _encrypt_data(self, data):
        try:
            if not data: return data
            
            if self.encryption_method == '1':
                # Basic XOR encryption
                result = self._simple_encrypt(data, self.encryption_key)
                return f"ENC_{result}"
            elif self.encryption_method == '2' and CRYPTO_AVAILABLE:
                # AES-256 with salt
                result = self._aes_encrypt(data, self.encryption_key, self.salt)
                return f"AES_{result}"
            elif self.encryption_method == '3' and CRYPTO_AVAILABLE and hasattr(self, 'public_key'):
                # ECC + AES hybrid
                result = self._ecc_hybrid_encrypt(data, self.public_key)
                return f"ECC_{result}"
            else:
                # Fallback to XOR
                logger.warning(f"Falling back to XOR encryption for method {self.encryption_method}")
                result = self._simple_encrypt(data, self.encryption_key)
                return f"ENC_{result}"
        except Exception as e:
            logger.error(f"Encryption failed: {e}")
            return data
    
    def _decrypt_data(self, encrypted_data):
        try:
            if not encrypted_data: return encrypted_data
            
            encrypted_str = str(encrypted_data)
            if encrypted_str.startswith('ENC_'):
                # XOR decryption
                return self._simple_decrypt(encrypted_data, self.encryption_key)
            elif encrypted_str.startswith('AES_'):
                # AES decryption
                return self._aes_decrypt(encrypted_data, self.encryption_key, self.salt)
            elif encrypted_str.startswith('ECC_'):
                # ECC hybrid decryption
                if hasattr(self, 'private_key') and self.private_key:
                    return self._ecc_hybrid_decrypt(encrypted_data, self.private_key)
                else:
                    logger.error("ECC private key not available for decryption")
                    return encrypted_data
            else:
                return encrypted_data
        except Exception as e:
            logger.error(f"Decryption failed: {e}")
            return encrypted_data
    
    def _simple_encrypt(self, data, key):
        try:
            if not data: return data
            data_bytes = str(data).encode('utf-8')
            key_bytes = base64.urlsafe_b64decode(key)
            encrypted = bytearray()
            for i, byte in enumerate(data_bytes):
                encrypted.append(byte ^ key_bytes[i % len(key_bytes)])
            result = base64.urlsafe_b64encode(encrypted).decode('utf-8')
            logger.debug(f"XOR encrypted data length: {len(result)}")
            return result
        except Exception as e:
            logger.error(f"XOR encryption failed: {e}")
            return data
    
    def _simple_decrypt(self, encrypted_data, key):
        try:
            if not encrypted_data or not str(encrypted_data).startswith('ENC_'):
                return encrypted_data
            clean_data = str(encrypted_data)[4:]
            encrypted_bytes = base64.urlsafe_b64decode(clean_data.encode('utf-8'))
            key_bytes = base64.urlsafe_b64decode(key)
            decrypted = bytearray()
            for i, byte in enumerate(encrypted_bytes):
                decrypted.append(byte ^ key_bytes[i % len(key_bytes)])
            result = decrypted.decode('utf-8', errors='ignore')
            logger.debug(f"XOR decrypted data successfully: {len(result)} chars")
            return result
        except Exception as e:
            logger.error(f"XOR decryption failed: {e}")
            return encrypted_data
    
    def _should_encrypt_field(self, field_name, value):
        field_lower = field_name.lower()
        return any(sensitive in field_lower for sensitive in self.sensitive_fields)
    
    def _encrypt_row(self, headers, row_data):
        try:
            encrypted_row = []
            for i, value in enumerate(row_data):
                if i < len(headers) and self._should_encrypt_field(headers[i], value):
                    encrypted_value = self._encrypt_data(value)
                    encrypted_row.append(encrypted_value)
                    logger.debug(f"Encrypted field '{headers[i]}' using method {self.encryption_method}")
                else:
                    encrypted_row.append(value)
            return encrypted_row
        except Exception as e:
            logger.error(f"Row encryption failed: {e}")
            return row_data
    
    def _decrypt_row(self, headers, row_data):
        try:
            decrypted_row = []
            for i, value in enumerate(row_data):
                if i < len(headers) and self._should_encrypt_field(headers[i], value):
                    decrypted_value = self._decrypt_data(str(value))
                    decrypted_row.append(decrypted_value)
                    logger.debug(f"Decrypted field '{headers[i]}' using appropriate method")
                else:
                    decrypted_row.append(value)
            return decrypted_row
        except Exception as e:
            logger.error(f"Row decryption failed: {e}")
            return row_data
        
    def _get_delimiter(self):
        delimiter_options = {'1': '|', '2': ',', '3': '\x1F\x1E\x1D\x1C\x1B'}
        chosen_delimiter = delimiter_options.get(self.delimiter_choice, '|')
        delimiter_names = {'|': 'Pipe', ',': 'CSV', '\x1F\x1E\x1D\x1C\x1B': 'Control Character'}
        if __name__ == "__main__":
            print(f"{delimiter_names[chosen_delimiter]} mode activated")
        logger.info(f"Delimiter mode selected: {delimiter_names[chosen_delimiter]}")
        return chosen_delimiter
    
    def write_header_magic(self, filename, header_fields):
        try:
            file_path = self._get_file_path(filename)
            logger.info(f"Writing headers to {file_path}: {header_fields}")
            with open(file_path, 'w') as f: f.write(self.delimiter.join(header_fields) + '\n')
            self.current_files[filename] = header_fields
            logger.info(f"Headers written successfully to {file_path}")
            return True, f"Header created successfully for {filename}"
        except Exception as e: 
            logger.error(f"Header creation failed for {filename}: {e}")
            return False, f"Header creation failed: {e}"
    
    def append_data_love(self, filename, data_values):
        try:
            file_path = self._get_file_path(filename)
            if not os.path.exists(file_path) and filename not in self.current_files:
                logger.warning(f"File {filename} needs headers first")
                return False, f"File {filename} needs headers first - call write_header_magic() first"
            if filename in self.current_files:
                headers = self.current_files[filename]
            else:
                with open(file_path, 'r') as f:
                    first_line = f.readline().strip()
                    headers = first_line.split(self.delimiter)
            encrypted_data = self._encrypt_row(headers, data_values)
            with open(file_path, 'a') as f: 
                f.write(self.delimiter.join(str(val) for val in encrypted_data) + '\n')
            logger.info(f"Data appended successfully to {file_path} (with encryption)")
            return True, f"Data added successfully to {filename}"
        except Exception as e: 
            logger.error(f"Data append failed for {filename}: {e}")
            return False, f"Data append failed: {e}"
    
    def read_data_sass(self, filename):
        try:
            file_path = self._get_file_path(filename)
            logger.info(f"Reading data from {file_path}")
            if not os.path.exists(file_path): 
                logger.warning(f"File {filename} doesn't exist")
                return [], f"File {filename} doesn't exist yet - create some data first!"
            with open(file_path, 'r') as f: lines_raw = f.readlines()
            if not lines_raw: 
                logger.warning(f"File {filename} is empty")
                return [], f"File {filename} is empty - time to add some content!"
            header_list = lines_raw[0].strip().split(self.delimiter)
            data_rows = [line.strip().split(self.delimiter) for line in lines_raw[1:] if line.strip()]
            decrypted_rows = []
            for row in data_rows:
                decrypted_row = self._decrypt_row(header_list, row)
                decrypted_rows.append(decrypted_row)
            logger.info(f"Successfully read and decrypted {len(decrypted_rows)} records from {file_path}")
            return {'headers': header_list, 'data': decrypted_rows}, f"Successfully read {len(decrypted_rows)} records"
        except Exception as e: 
            logger.error(f"Read operation failed for {filename}: {e}")
            return [], f"Read operation failed: {e}"
    
    def update_record_boss(self, filename, search_field, search_value, new_data):
        try:
            logger.info(f"Updating records in {filename} where {search_field}={search_value}")
            file_contents = self.read_data_sass(filename)
            if isinstance(file_contents, list): 
                logger.error(f"Failed to read file for update: {file_contents[1] if file_contents else 'Unknown error'}")
                return False, file_contents[1]
            headers, all_data = file_contents[0]['headers'], file_contents[0]['data']
            if search_field not in headers: 
                logger.error(f"Search field '{search_field}' not found in headers")
                return False, f"Search field '{search_field}' not found in headers"
            search_index, records_updated = headers.index(search_field), 0
            for row_index, row_data in enumerate(all_data):
                if row_data[search_index] == search_value:
                    for field_name, new_value in new_data.items():
                        if field_name in headers: 
                            all_data[row_index][headers.index(field_name)] = str(new_value)
                    records_updated += 1
            if records_updated == 0: 
                logger.warning(f"No records found with {search_field}='{search_value}'")
                return False, f"No records found with {search_field}='{search_value}'"
            self.write_header_magic(filename, headers)
            for row in all_data:
                self.append_data_love(filename, row)
            logger.info(f"Updated {records_updated} records successfully in {filename}")
            return True, f"Updated {records_updated} records successfully"
        except Exception as e: 
            logger.error(f"Update failed for {filename}: {e}")
            return False, f"Update failed: {e}"
    
    def delete_record_cleanup(self, filename, search_field, search_value):
        try:
            logger.info(f"Deleting records from {filename} where {search_field}={search_value}")
            file_contents = self.read_data_sass(filename)
            if isinstance(file_contents, list): 
                logger.error(f"Failed to read file for deletion: {file_contents[1] if file_contents else 'Unknown error'}")
                return False, file_contents[1]
            headers, all_data = file_contents[0]['headers'], file_contents[0]['data']
            if search_field not in headers: 
                logger.error(f"Search field '{search_field}' not found")
                return False, f"Search field '{search_field}' not found"
            search_index, original_count = headers.index(search_field), len(all_data)
            filtered_data = [row for row in all_data if row[search_index] != search_value]
            deleted_count = original_count - len(filtered_data)
            if deleted_count == 0: 
                logger.warning(f"No records found to delete with {search_field}='{search_value}'")
                return False, f"No records found to delete with {search_field}='{search_value}'"
            self.write_header_magic(filename, headers)
            for row in filtered_data:
                self.append_data_love(filename, row)
            logger.info(f"Deleted {deleted_count} records successfully from {filename}")
            return True, f"Deleted {deleted_count} records successfully"
        except Exception as e: 
            logger.error(f"Delete operation failed for {filename}: {e}")
            return False, f"Delete operation failed: {e}"

    def convert_file_format(self, source_filename, target_format, output_filename=None):
        try:
            logger.info(f"Converting {source_filename} to format {target_format}")
            source_format = self._detect_file_format(source_filename)
            if not source_format:
                logger.error(f"Could not detect source file format for {source_filename}")
                return False, "Could not detect source file format"
            logger.info(f"Detected source format: {source_format}")
            original_choice = self.delimiter_choice
            original_separator = self.delimiter
            delimiter_options = {'1': '|', '2': ',', '3': '\x1F\x1E\x1D\x1C\x1B'}
            self.delimiter_choice = source_format
            self.delimiter = delimiter_options[source_format]
            file_contents = self.read_data_sass(source_filename)
            if isinstance(file_contents, list): 
                self.delimiter_choice = original_choice
                self.delimiter = original_separator
                logger.error(f"Cannot read source file {source_filename}: {file_contents[1] if file_contents else 'Unknown error'}")
                return False, f"Cannot read source file: {file_contents[1] if file_contents else 'Unknown error'}"
            headers, all_data = file_contents[0]['headers'], file_contents[0]['data']
            self.delimiter_choice = original_choice
            self.delimiter = original_separator
            if target_format not in delimiter_options: 
                logger.error(f"Invalid target format: {target_format}")
                return False, "Invalid target format. Use '1' (Pipe), '2' (CSV), or '3' (Control Chars)"
            target_delimiter = delimiter_options[target_format]
            delimiter_names = {'|': 'Pipe', ',': 'CSV', '\x1F\x1E\x1D\x1C\x1B': 'Control Character'}
            target_name = delimiter_names[target_delimiter]
            if not output_filename:
                base_name = os.path.splitext(source_filename)[0]
                format_suffix = {'1': '_pipe', '2': '_csv', '3': '_ctrl'}
                output_filename = f"{base_name}{format_suffix[target_format]}.txt"
            temp_choice = self.delimiter_choice
            temp_separator = self.delimiter
            self.delimiter_choice = target_format
            self.delimiter = target_delimiter
            self.write_header_magic(output_filename, headers)
            for row in all_data:
                self.append_data_love(output_filename, row)
            self.delimiter_choice = temp_choice
            self.delimiter = temp_separator
            logger.info(f"File converted successfully to {target_name} format: {output_filename}")
            return True, f"File converted successfully to {target_name} format: {output_filename}"
        except Exception as e: 
            logger.error(f"Conversion failed for {source_filename}: {e}")
            return False, f"Conversion failed: {e}"

    def _detect_file_format(self, filename):
        try:
            file_path = self._get_file_path(filename)
            logger.debug(f"Detecting file format for {file_path}")
            with open(file_path, 'r') as f: first_line = f.readline()
            if '\x1F\x1E\x1D\x1C\x1B' in first_line: 
                logger.debug(f"Detected Control Characters format for {filename}"); return '3'
            elif '|' in first_line: 
                logger.debug(f"Detected Pipe format for {filename}"); return '1'
            elif ',' in first_line: 
                logger.debug(f"Detected CSV format for {filename}"); return '2'
            else: 
                logger.debug(f"Defaulting to Pipe format for {filename}"); return '1'
        except Exception as e: logger.error(f"File format detection failed for {filename}: {e}"); return None

    def show_conversion_menu(self):
        try:
            logger.info("Starting conversion menu")
            print("\nFILE FORMAT CONVERSION CENTER - DataQueen Style")
            txt_files = [f for f in os.listdir(self.data_folder) if f.endswith('.txt') and 
                        os.path.isfile(os.path.join(self.data_folder, f))]
            if not txt_files:
                logger.warning("No .txt files found in data directory")
                print("No .txt files found in data directory!")
                return
            print("\nAvailable files for conversion:")
            for i, filename in enumerate(txt_files, 1): print(f"  {i}. {filename}")
            file_choice = input(f"\nSelect file to convert (1-{len(txt_files)}) or 'q' to quit: ").strip()
            if file_choice.lower() == 'q': 
                logger.info("User quit conversion menu"); return
            file_index = int(file_choice) - 1
            if file_index < 0 or file_index >= len(txt_files):
                logger.warning(f"Invalid file selection: {file_choice}"); print("Invalid file selection!"); return
            selected_file = txt_files[file_index]; logger.info(f"User selected file: {selected_file}")
            detected_format = self._detect_file_format(selected_file)
            format_names = {'1': 'Pipe (|)', '2': 'CSV (,)', '3': 'Control Chars'}
            detected_name = format_names.get(detected_format, 'Unknown')
            print(f"\nSelected file: {selected_file}"); print(f"Detected format: {detected_name}")
            print("\nTarget formats:"); print("1. Pipe Delimited (|) - Classic & Clean")
            print("2. CSV Format (,) - Spreadsheet Friendly"); print("3. Special Control Chars - Untypeable & Unbreakable")
            format_choice = input("Select target format (1-3): ").strip()
            if format_choice not in ['1', '2', '3']: 
                logger.warning(f"Invalid format selection: {format_choice}"); print("Invalid format selection!"); return
            custom_name = input("Custom output filename (press Enter for auto-generated): ").strip()
            output_filename = custom_name if custom_name else None
            logger.info(f"Converting {selected_file} to format {format_choice} with output: {output_filename}")
            success, msg = self.convert_file_format(selected_file, format_choice, output_filename)
            print(f"\n{msg}")
            if success: print("Conversion completed successfully!"); logger.info("Conversion completed successfully")
            else: logger.error("Conversion failed")
        except ValueError: logger.error("Invalid input in conversion menu - not a number"); print("Invalid input! Please enter a number.")
        except Exception as e: logger.error(f"Conversion menu error: {e}"); print(f"Conversion menu error: {e}")
    
    def get_encryption_info(self):
        method_names = {'1': 'Basic XOR (Fast & Simple)', '2': 'AES-256 with Salt (Strong & Secure)', 
                       '3': 'ECC + AES Hybrid (Maximum Security)'}
        info = {'method': method_names.get(self.encryption_method, 'Unknown'), 'method_code': self.encryption_method,
                'crypto_available': CRYPTO_AVAILABLE, 'salt_length': len(base64.urlsafe_b64decode(self.salt)) if hasattr(self, 'salt') else 0,
                'has_ecc_keys': hasattr(self, 'private_key') and self.private_key is not None}
        print("\nCurrent Encryption Configuration:")
        print(f"   Method: {info['method']}")
        print(f"   Cryptography Library: {'Available' if info['crypto_available'] else 'Not Available'}")
        print(f"   Salt Length: {info['salt_length']} bytes")
        if info['method_code'] == '3':
            print(f"   ECC Keypair: {'Generated' if info['has_ecc_keys'] else 'Not Available'}")
        return info

def create_file_handler(auto_delimiter_choice=3, encryption_method=None): 
    logger.info("Creating new DataQueen file handler instance")
    return DataQueen(auto_delimiter_choice=auto_delimiter_choice, encryption_method=encryption_method)

if __name__ == "__main__":
    print("DataQueen File Handler - Test")
    logger.info("Starting DataQueen demo application")
    print("\nOptions:"); print("1. Create demo files and test conversion"); print("2. File Format Conversion Menu (existing files)")
    choice = input("Select option (1-2): ").strip(); logger.info(f"User selected option: {choice}")
    if choice == '2':
        print("\nFile Handler Service - Choose Your Delimiter Style:")
        print("1. Pipe Delimited (|) - Classic & Clean"); print("2. CSV Format (,) - Spreadsheet Friendly")
        print("3. Special Control Chars - Advanced Security")
        format_choice = input("Select your delimiter option (1-3): ").strip()
        delimiter_options = {'1': '|', '2': ',', '3': '\x1F\x1E\x1D\x1C\x1B'}
        delimiter_names = {'|': 'Pipe', ',': 'CSV', '\x1F\x1E\x1D\x1C\x1B': 'Control Character'}
        chosen_sep = delimiter_options.get(format_choice, '|'); print(f"{delimiter_names[chosen_sep]} mode activated")
        jill = DataQueen.__new__(DataQueen); jill.delimiter_choice = format_choice; jill.delimiter = chosen_sep
        jill.current_files = {}; jill.encryption_key = jill._generate_master_key(); jill.data_folder = "jill_data"
        jill.sensitive_fields = {'password', 'pass', 'pwd', 'secret', 'token', 'key'}; logger.info("Created DataQueen instance for conversion menu")
        jill.show_conversion_menu()
    else:
        logger.info("Starting enhanced demo mode with encryption options"); print("\nEnhanced Demo - Test All Encryption Methods")
        encryption_methods = ['1', '2', '3']; method_names = {'1': 'xor_basic', '2': 'aes_256_plus_salt', '3': 'ecc_plus_aes_hybrid'}
        for method in encryption_methods:
            print(f"\n{'='*60}"); print(f"Testing {method_names[method].replace('_', ' ').title()} Encryption"); print(f"{'='*60}")
            try:
                jill = create_file_handler(auto_delimiter_choice=3, encryption_method=method); jill.get_encryption_info()
                demo_file = f"demo_{method_names[method]}.txt"
                headers = ["name", "role", "password", "salary"]
                success, msg = jill.write_header_magic(demo_file, headers); print(f"\nFile creation: {msg}")
                if success:
                    test_data = [["Alice", "Manager", "secret123", "75000"], ["Bob", "Developer", "mypassword", "65000"], 
                               ["Charlie", "Analyst", "supersecure", "55000"]]
                    for data_row in test_data: jill.append_data_love(demo_file, data_row)
                    print(f"Added {len(test_data)} records with {method_names[method].replace('_', ' ')} encryption")
                    data_result, read_msg = jill.read_data_sass(demo_file)
                    if isinstance(data_result, dict):
                        print(f"\nDecrypted Data Preview:"); print(f"Headers: {data_result['headers']}")
                        for i, row in enumerate(data_result['data'][:2]): print(f"Row {i+1}: {row}")
                        print(f"\nRaw File Content (encrypted on disk):")
                        with open(jill._get_file_path(demo_file), 'r') as f:
                            lines = f.readlines(); print(f"Header: {lines[0].strip()}")
                            if len(lines) > 1: 
                                print(f"First Record: {lines[1].strip()}")
                                if 'password' in lines[1] or 'secret' in lines[1]: print("   Notice the encrypted password field")
                    print(f"{method_names[method].replace('_', ' ')} encryption test completed successfully")
            except Exception as e: print(f"{method_names[method]} encryption test failed: {e}"); logger.error(f"Demo failed for method {method}: {e}")
        print(f"\n{'='*60}"); print("All Encryption Methods Tested")
        print("Check the jill_data folder for generated demo files"); print(f"{'='*60}")
    logger.info("DataQueen demo application completed")
