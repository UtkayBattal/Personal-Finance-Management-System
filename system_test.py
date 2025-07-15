import unittest
import sys
import os
import random

# Add the GP-1 yedek directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
app_dir = os.path.join(current_dir, 'GP-1 yedek')
sys.path.append(app_dir)

from app import create_app, db
from app.models import User, Transaction, Budget
from datetime import datetime, timedelta
import time
import pandas as pd
import numpy as np

class FinanceAppTest(unittest.TestCase):
    def setUp(self):
        """Test öncesi ortamı hazırla"""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Test için geçici veritabanı
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Uyarıyı kapat
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()

    def tearDown(self):
        """Test sonrası temizlik"""
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def create_test_user(self):
        """Test için kullanıcı oluştur"""
        user = User(username='test_user', email='test@test.com')
        user.set_password('test123')  # Şifreyi doğru şekilde ayarla
        db.session.add(user)
        db.session.commit()
        return user

    # 1. BİRİM TESTLER
    def test_user_creation(self):
        """Kullanıcı oluşturma testi"""
        user = User(username='test_user', email='test@test.com')
        user.set_password('test123')  # Şifreyi ayarla
        db.session.add(user)
        db.session.commit()
        
        saved_user = User.query.filter_by(username='test_user').first()
        self.assertIsNotNone(saved_user)
        self.assertTrue(saved_user.check_password('test123'))

    def test_transaction_creation(self):
        """İşlem oluşturma testi"""
        user = self.create_test_user()  # Test kullanıcısını oluştur

        transaction = Transaction(
            category='Food',
            amount=100.0,
            type='expense',
            user_id=user.id
        )
        db.session.add(transaction)
        db.session.commit()

        saved_transaction = Transaction.query.filter_by(user_id=user.id).first()
        self.assertIsNotNone(saved_transaction)
        self.assertEqual(saved_transaction.amount, 100.0)

    def test_budget_creation(self):
        """Bütçe oluşturma testi"""
        user = self.create_test_user()  # Test kullanıcısını oluştur

        budget = Budget(
            category='Food',
            amount=1000.0,
            period='Monthly',
            user_id=user.id
        )
        db.session.add(budget)
        db.session.commit()

        saved_budget = Budget.query.filter_by(user_id=user.id).first()
        self.assertIsNotNone(saved_budget)
        self.assertEqual(saved_budget.amount, 1000.0)

    # 2. PERFORMANS TESTLERİ
    def test_sarima_prediction_performance(self):
        """SARIMA tahmin performans testi"""
        user = self.create_test_user()  # Test kullanıcısını oluştur

        # Test verisi oluştur - son 2 yıl için veri
        start_date = datetime.now() - timedelta(days=730)  # 2 yıl
        monthly_amounts = {
            'Food': (500, 1000),
            'Clothing': (200, 500),
            'Entertainment': (100, 300),
            'Market': (300, 800),
            'Other': (100, 400)
        }

        # Her ay için veri ekle
        current_date = start_date
        while current_date < datetime.now():
            # Her kategori için aylık işlem
            for category, (min_amount, max_amount) in monthly_amounts.items():
                # Ay içinde 2-5 işlem
                for _ in range(random.randint(2, 5)):
                    amount = random.uniform(min_amount/3, max_amount/3)
                    transaction_date = current_date + timedelta(days=random.randint(0, 27))
                    transaction = Transaction(
                        category=category,
                        amount=amount,
                        date=transaction_date,
                        type='expense',
                        user_id=user.id
                    )
                    db.session.add(transaction)
            
            # Sonraki aya geç
            if current_date.month == 12:
                current_date = datetime(current_date.year + 1, 1, 1)
            else:
                current_date = datetime(current_date.year, current_date.month + 1, 1)

        db.session.commit()

        # Tahmin süresini ölç
        start_time = time.time()
        predictions = Transaction.predict_future_expenses(user.id)
        end_time = time.time()

        # Testler
        self.assertIsNotNone(predictions, "Tahmin sonucu None olmamalı")
        self.assertIn('forecast', predictions, "Tahmin sonucunda 'forecast' anahtarı olmalı")
        self.assertIn('actual', predictions, "Tahmin sonucunda 'actual' anahtarı olmalı")
        self.assertEqual(len(predictions['forecast']), 6, "6 aylık tahmin olmalı")
        self.assertEqual(len(predictions['actual']), 6, "6 aylık gerçek veri olmalı")
        self.assertLess(end_time - start_time, 5.0, "Tahmin 5 saniyeden uzun sürmemeli")

    def test_dashboard_load_performance(self):
        """Gösterge paneli yükleme performans testi"""
        user = self.create_test_user()  # Test kullanıcısını oluştur

        # Login
        self.client.post('/auth/login', data={
            'email': 'test@test.com',
            'password': 'test123'
        })

        # Dashboard yükleme süresini ölç
        start_time = time.time()
        response = self.client.get('/dashboard')
        end_time = time.time()

        self.assertEqual(response.status_code, 200)
        self.assertLess(end_time - start_time, 2.0)  # 2 saniyeden az sürmeli

    # 3. VERİ DOĞRULAMA TESTLERİ
    def test_transaction_validation(self):
        """İşlem verisi doğrulama testi"""
        # Geçersiz miktar
        is_valid, message = Transaction.validate_transaction(-100, "Food", "expense")
        self.assertFalse(is_valid)
        self.assertEqual(message, "Amount must be positive")

        # Geçersiz kategori
        is_valid, message = Transaction.validate_transaction(100, "", "expense")
        self.assertFalse(is_valid)
        self.assertEqual(message, "Category is required")

        # Geçersiz işlem tipi
        is_valid, message = Transaction.validate_transaction(100, "Food", "invalid")
        self.assertFalse(is_valid)
        self.assertEqual(message, "Invalid transaction type")

        # Geçerli işlem
        is_valid, message = Transaction.validate_transaction(100, "Food", "expense")
        self.assertTrue(is_valid)
        self.assertEqual(message, "Valid transaction")

    def test_budget_limit_check(self):
        """Bütçe limit kontrolü testi"""
        user = self.create_test_user()

        # Bütçe oluştur
        budget = Budget(
            category='Food',
            amount=1000.0,
            period='Monthly',
            user_id=user.id
        )
        db.session.add(budget)

        # Harcama ekle
        transaction = Transaction(
            category='Food',
            amount=800.0,
            type='expense',
            user_id=user.id
        )
        db.session.add(transaction)
        db.session.commit()

        # Bütçe limitini aşacak harcama kontrolü
        would_exceed, remaining = Transaction.check_budget_limit(user.id, 'Food', 300.0)
        self.assertTrue(would_exceed)
        self.assertAlmostEqual(remaining, 200.0)

    # 4. GÜVENLİK TESTLERİ
    def test_password_security(self):
        """Şifre güvenliği testi"""
        user = User(username='security_test', email='security@test.com')
        
        # Şifre karmaşıklığı
        test_password = 'test123'
        user.set_password(test_password)
        
        # Hash kontrolü
        self.assertNotEqual(user.password, test_password)
        self.assertTrue(user.check_password(test_password))
        self.assertFalse(user.check_password('wrong_password'))

    def test_unauthorized_access(self):
        """Yetkisiz erişim testi"""
        # Giriş yapmadan dashboard'a erişim denemesi
        response = self.client.get('/dashboard', follow_redirects=True)
        self.assertIn(b'login', response.data.lower())

        # Giriş yapmadan işlem ekleme denemesi
        response = self.client.post('/add_transaction', data={
            'category': 'Food',
            'amount': 100,
            'type': 'expense'
        }, follow_redirects=True)
        self.assertIn(b'login', response.data.lower())

        # Giriş yapmadan bütçe ekleme denemesi
        response = self.client.post('/add_budget', data={
            'category': 'Food',
            'amount': 1000,
            'period': 'Monthly'
        }, follow_redirects=True)
        self.assertIn(b'login', response.data.lower())

    def test_login_functionality(self):
        """Giriş işlevselliği testi"""
        # Test kullanıcısı oluştur
        user = self.create_test_user()

        # Yanlış şifre ile giriş denemesi
        response = self.client.post('/auth/login', data={
            'email': 'test@test.com',
            'password': 'wrong_password'
        }, follow_redirects=True)
        self.assertNotEqual(response.status_code, 200)  # Başarısız giriş

        # Doğru şifre ile giriş
        response = self.client.post('/auth/login', data={
            'email': 'test@test.com',
            'password': 'test123'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)  # Başarılı giriş
        self.assertIn(b'dashboard', response.data.lower())  # Dashboard'a yönlendirme

    def test_transaction_summary(self):
        """İşlem özeti testi"""
        user = self.create_test_user()
        self.client.post('/auth/login', data={
            'email': 'test@test.com',
            'password': 'test123'
        })

        # Test işlemleri ekle
        transactions = [
            ('Food', 100, 'expense'),
            ('Food', 200, 'expense'),
            ('Salary', 5000, 'income')
        ]

        for category, amount, type in transactions:
            transaction = Transaction(
                category=category,
                amount=amount,
                type=type,
                user_id=user.id
            )
            db.session.add(transaction)
        db.session.commit()

        # İşlem özetini kontrol et
        response = self.client.get('/dashboard')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Food', response.data)
        self.assertIn(b'Salary', response.data)

    def test_category_validation(self):
        """Kategori doğrulama testi"""
        user = self.create_test_user()
        self.client.post('/auth/login', data={
            'email': 'test@test.com',
            'password': 'test123'
        })

        # Geçerli kategoriler
        valid_categories = ['Food', 'Clothing', 'Entertainment', 'Market', 'Other']
        
        for category in valid_categories:
            response = self.client.post('/add_transaction', data={
                'category': category,
                'amount': 100,
                'type': 'expense'
            }, follow_redirects=True)
            self.assertIn(b'success', response.data.lower())

    def test_date_handling(self):
        """Tarih işleme testi"""
        user = self.create_test_user()
        self.client.post('/auth/login', data={
            'email': 'test@test.com',
            'password': 'test123'
        })

        # Farklı tarihlerde işlemler ekle
        dates = [
            datetime.now(),
            datetime.now() - timedelta(days=1),
            datetime.now() - timedelta(days=7)
        ]

        for date in dates:
            transaction = Transaction(
                category='Food',
                amount=100,
                type='expense',
                user_id=user.id,
                date=date
            )
            db.session.add(transaction)
        db.session.commit()

        # Tarihlerin doğru kaydedildiğini kontrol et
        transactions = Transaction.query.filter_by(user_id=user.id).all()
        self.assertEqual(len(transactions), 3)
        for transaction in transactions:
            self.assertIsInstance(transaction.date, datetime)

    # 5. KULLANICI DENEYİMİ TESTLERİ
    def test_user_feedback(self):
        """Kullanıcı geri bildirim testi"""
        user = self.create_test_user()

        # 1. Başarılı giriş testi
        response = self.client.post('/auth/login', data={
            'email': 'test@test.com',
            'password': 'test123'
        }, follow_redirects=True)
        self.assertIn(b'success', response.data.lower())

        # 2. Başarılı bütçe ekleme testi
        response = self.client.post('/add_budget', data={
            'category': 'Food',
            'amount': 1000,
            'period': 'Monthly'
        }, follow_redirects=True)
        self.assertIn(b'success', response.data.lower())

        # 3. Başarılı işlem ekleme testi
        response = self.client.post('/add_transaction', data={
            'category': 'Food',
            'amount': 100,
            'type': 'expense'
        }, follow_redirects=True)
        self.assertIn(b'success', response.data.lower())

        # 4. Hatalı işlem testi
        response = self.client.post('/add_transaction', data={
            'category': 'Food',
            'amount': -100,  # Geçersiz miktar
            'type': 'expense'
        }, follow_redirects=True)
        self.assertIn(b'error', response.data.lower())

        # 5. İstatistik sayfası kontrolü
        response = self.client.get('/dashboard', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'statistics', response.data.lower())

    def test_error_handling(self):
        """Hata yönetimi testi"""
        user = self.create_test_user()
        self.client.post('/auth/login', data={
            'email': 'test@test.com',
            'password': 'test123'
        }, follow_redirects=True)

        # 1. Geçersiz kategori
        response = self.client.post('/add_transaction', data={
            'category': '',  # Boş kategori
            'amount': 100,
            'type': 'expense'
        }, follow_redirects=True)
        self.assertIn(b'error', response.data.lower())

        # 2. Geçersiz miktar formatı
        response = self.client.post('/add_transaction', data={
            'category': 'Food',
            'amount': 'invalid',  # Sayı olmayan değer
            'type': 'expense'
        }, follow_redirects=True)
        self.assertIn(b'error', response.data.lower())

        # 3. Eksik alan kontrolü
        response = self.client.post('/add_transaction', data={
            'category': 'Food'
            # amount ve type eksik
        }, follow_redirects=True)
        self.assertIn(b'error', response.data.lower())

if __name__ == '__main__':
    unittest.main() 