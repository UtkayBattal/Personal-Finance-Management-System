# app/models.py
from . import db
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Enum
from flask_login import UserMixin
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np

# Kullanıcı Modeli
class User(UserMixin, db.Model):
    __tablename__ = 'User'  # Tablo adını açıkça belirtiyoruz
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    transactions = db.relationship('Transaction', backref='user', lazy=True)
    budgets = db.relationship('Budget', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

    def get_id(self):
        return str(self.id)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def set_password(self, password):
        self.password = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        return check_password_hash(self.password, password)



# Gelir-Gider Modeli
class Transaction(db.Model):
    __tablename__ = 'Transaction'
    
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    type = db.Column(db.Enum('income', 'expense', name='transaction_type'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)

    @classmethod
    def get_monthly_time_series(cls, user_id, start_date=None, end_date=None):
        """Gets monthly total expenses for all categories combined"""
        query = cls.query.filter_by(
            user_id=user_id,
            type='expense'
        )
        
        if start_date:
            query = query.filter(cls.date >= start_date)
        if end_date:
            query = query.filter(cls.date < end_date)
        
        transactions = query.order_by(cls.date).all()
        
        # Calculate monthly totals
        df = pd.DataFrame([(t.date.replace(day=1), t.amount) for t in transactions], 
                         columns=['date', 'amount'])
        
        if df.empty:
            return df
            
        df = df.groupby('date')['amount'].sum().reset_index()
        df.set_index('date', inplace=True)
        
        return df

    @classmethod
    def get_first_transaction_date(cls, user_id):
        """Gets the date of the first transaction for the user"""
        first_transaction = cls.query.filter_by(
            user_id=user_id
        ).order_by(cls.date.asc()).first()
        
        return first_transaction.date if first_transaction else None

    @classmethod
    def predict_future_expenses(cls, user_id, start_date=None, end_date=None):
        """Predicts total monthly expenses for the next 6 months using SARIMA model"""
        try:
            # Get the first transaction date
            first_transaction_date = cls.get_first_transaction_date(user_id)
            if not first_transaction_date:
                print("No transaction history found")
                return None
            
            print(f"First transaction date: {first_transaction_date}")
            
            # If end_date is None, use current date
            if end_date is None:
                end_date = datetime.now()
            
            # Get all historical data up to end_date
            df = cls.get_monthly_time_series(user_id, first_transaction_date, end_date)
            
            if df.empty:
                print("No historical data available")
                return None
            
            # We need at least 6 months of data for meaningful predictions
            if len(df) < 6:
                print("Insufficient data for prediction (need at least 6 months)")
                return None
            
            # Prepare data for SARIMA
            values = df['amount'].values
            
            # Calculate basic statistics for bounds
            recent_mean = values[-6:].mean()  # Last 6 months average
            overall_mean = values.mean()      # Overall average
            recent_std = values[-6:].std()    # Last 6 months standard deviation
            
            print(f"Recent 6-month average: {recent_mean:.2f}")
            print(f"Overall average: {overall_mean:.2f}")
            print(f"Recent std: {recent_std:.2f}")
            
            # Fit SARIMA model
            model = SARIMAX(
                values,
                order=(1, 1, 1),
                seasonal_order=(1, 1, 1, 12),
                enforce_stationarity=False,
                enforce_invertibility=False
            )
            
            results = model.fit(disp=False)
            
            # Generate forecasts
            forecast = results.forecast(steps=6)
            
            # Apply bounds and adjustments
            forecasts = []
            for pred in forecast:
                # Ensure prediction is not too far from recent patterns
                min_bound = max(recent_mean * 0.7, overall_mean * 0.7)
                max_bound = min(recent_mean * 1.3, overall_mean * 1.3) + recent_std
                
                # Clip prediction to bounds
                adjusted_pred = np.clip(pred, min_bound, max_bound)
                forecasts.append(float(adjusted_pred))
            
            print(f"SARIMA forecasts: {forecasts}")
            
            # Get actual expenses for the forecast period
            actual_expenses = []
            current_date = end_date
            
            for _ in range(6):
                if current_date.month == 12:
                    next_month = datetime(current_date.year + 1, 1, 1)
                else:
                    next_month = datetime(current_date.year, current_date.month + 1, 1)
                
                actual = cls.query.filter(
                    cls.user_id == user_id,
                    cls.type == 'expense',
                    cls.date >= current_date,
                    cls.date < next_month
                ).with_entities(db.func.sum(cls.amount)).scalar()
                
                actual_expenses.append(float(actual) if actual else 0)
                current_date = next_month
            
            print(f"Actual expenses: {actual_expenses}")
            
            return {
                'forecast': forecasts,
                'actual': actual_expenses
            }
            
        except Exception as e:
            print(f"Prediction error: {e}")
            return None

    @classmethod
    def validate_transaction(cls, amount, category, type):
        """Validates transaction data"""
        if amount <= 0:
            return False, "Amount must be positive"
        if not category:
            return False, "Category is required"
        if type not in ['income', 'expense']:
            return False, "Invalid transaction type"
        return True, "Valid transaction"

    @classmethod
    def check_budget_limit(cls, user_id, category, amount):
        """Checks if a transaction would exceed the budget limit"""
        current_month_start = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        next_month_start = (current_month_start + timedelta(days=32)).replace(day=1)
        
        # Get current month's spending
        current_spending = cls.query.filter(
            cls.user_id == user_id,
            cls.category == category,
            cls.type == 'expense',
            cls.date >= current_month_start,
            cls.date < next_month_start
        ).with_entities(db.func.sum(cls.amount)).scalar() or 0

        # Get budget limit
        budget = Budget.query.filter_by(
            user_id=user_id,
            category=category,
            period='Monthly'
        ).order_by(Budget.date.desc()).first()

        if budget:
            remaining = budget.amount - current_spending
            would_exceed = (current_spending + amount) > budget.amount
            return would_exceed, remaining
        
        return False, None



# Model for budgeting specific categories
class Budget(db.Model):
    __tablename__ = 'Budget'
    
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    period = db.Column(db.String(20), nullable=False)  # Monthly veya Yearly
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)

    
