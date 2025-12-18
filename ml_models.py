import sqlite3
from datetime import datetime
import json

class Database:
    def __init__(self, db_path='scdas.db'):
        self.db_path = db_path
        self.create_tables()
    
    def create_tables(self):
        """Create users and diagnosis_history tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Users table with phone number as primary identifier
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                phone TEXT UNIQUE NOT NULL,
                pin TEXT NOT NULL,
                full_name TEXT NOT NULL,
                village TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Diagnosis history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS diagnosis_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                disease TEXT NOT NULL,
                confidence REAL NOT NULL,
                symptoms TEXT,
                treatment TEXT,
                prevention TEXT,
                image_path TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                location_data TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def create_user(self, phone, pin, full_name, village=None):
        """Register a new user with phone number"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO users (phone, pin, full_name, village)
                VALUES (?, ?, ?, ?)
            ''', (phone, pin, full_name, village))
            conn.commit()
            user_id = cursor.lastrowid
            conn.close()
            return user_id
        except sqlite3.IntegrityError:
            conn.close()
            return None  # Phone number already exists
    
    def verify_user(self, phone, pin):
        """Verify user login with phone and PIN"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM users WHERE phone = ? AND pin = ?', (phone, pin))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return user[0]  # Return user_id
        return None
    
    def get_user_info(self, user_id):
        """Get user information"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT id, phone, full_name, village FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return {
                'id': user[0],
                'phone': user[1],
                'full_name': user[2],
                'village': user[3]
            }
        return None
    
    def add_diagnosis(self, user_id, result):
        """Add diagnosis to user's history"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO diagnosis_history 
            (user_id, disease, confidence, symptoms, treatment, prevention, image_path, timestamp, location_data)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            user_id,
            result['disease'],
            result['confidence'],
            result['symptoms'],
            result['treatment'],
            result['prevention'],
            result['image_path'],
            result['timestamp'],
            json.dumps(result['location'])
        ))
        conn.commit()
        conn.close()
    
    def get_user_history(self, user_id):
        """Get diagnosis history for specific user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, disease, confidence, symptoms, treatment, prevention, 
                   image_path, timestamp, location_data, created_at
            FROM diagnosis_history
            WHERE user_id = ?
            ORDER BY created_at DESC
        ''', (user_id,))
        rows = cursor.fetchall()
        conn.close()
        
        history = []
        for row in rows:
            history.append({
                'id': row[0],
                'disease': row[1],
                'confidence': row[2],
                'symptoms': row[3],
                'treatment': row[4],
                'prevention': row[5],
                'image_path': row[6],
                'timestamp': row[7],
                'location': json.loads(row[8]) if row[8] else {},
                'created_at': row[9]
            })
        return history
    
    def clear_user_history(self, user_id):
        """Clear all history for user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM diagnosis_history WHERE user_id = ?', (user_id,))
        conn.commit()
        conn.close()
    
    def delete_diagnosis(self, diagnosis_id, user_id):
        """Delete specific diagnosis"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM diagnosis_history WHERE id = ? AND user_id = ?', (diagnosis_id, user_id))
        conn.commit()
        conn.close()
