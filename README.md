# 💰 Personal Finance Management System

A modern and user-friendly personal finance management system. A comprehensive financial tracking application developed using Flask web framework, supported by SQLite database, and offering future expense predictions through machine learning algorithms.

## 🚀 Features

### 📊 Core Functions
- **Income-Expense Tracking**: Detailed category-based income and expense records
- **Budget Management**: Monthly and yearly budget planning and tracking
- **Statistical Analysis**: Category-based expense analysis and visualization
- **Advanced Search**: Multi-criteria transaction search and filtering

### 🤖 Machine Learning Features
- **SARIMA Prediction Model**: 6-month expense predictions based on historical data
- **Smart Budget Alerts**: Automatic alerts when approaching budget limits
- **Trend Analysis**: Analysis of monthly and daily expense trends

### 🎨 User Experience
- **Modern UI/UX**: Modern interface with glassmorphism design
- **Responsive Design**: Mobile and desktop compatible design
- **Real-time Charts**: Interactive data visualization with Chart.js
- **Automatic Notifications**: User feedback with success/error messages

## 🛠️ Technology Stack

### Backend
- **Flask**: Python web framework
- **SQLAlchemy**: ORM (Object-Relational Mapping)
- **Flask-Migrate**: Database migration management
- **Flask-Login**: User session management
- **Werkzeug**: Secure password hashing

### Frontend
- **HTML5/CSS3**: Modern web standards
- **JavaScript (ES6+)**: Dynamic interface functionality
- **Chart.js**: Interactive charts and graphs
- **Font Awesome**: Icon library
- **Google Fonts (Poppins)**: Modern typography

### Data Analysis and ML
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computations
- **Statsmodels**: SARIMA time series analysis
- **Scikit-learn**: Machine learning tools

### Database
- **SQLite**: Lightweight and portable database
- **Alembic**: Database migration system

## 📁 Project Structure

```
Personal-Finance-Management-System/
├── app/                          # Main application package
│   ├── __init__.py              # Flask app factory and configuration
│   ├── models.py                # Database models (User, Transaction, Budget)
│   ├── routes.py                # URL routing and view functions
│   └── forms.py                 # WTForms form definitions
├── templates/                   # Jinja2 HTML templates
│   ├── index.html              # Home page
│   ├── auth.html               # Login/register page
│   ├── dashboard.html          # Main control panel
│   ├── add_transaction.html    # Transaction addition page
│   └── add_budget.html         # Budget addition page
├── static/                     # Static files (CSS, JS, images)
│   ├── dashboard.css           # Dashboard style file
│   ├── index.css              # Home page style file
│   ├── auth.css               # Authentication page styles
│   ├── add_transaction.css    # Transaction addition page styles
│   └── add_budget.css         # Budget addition page styles
├── migrations/                 # Database migration files
│   ├── env.py                 # Alembic configuration
│   ├── alembic.ini            # Alembic settings
│   └── script.py.mako         # Migration template
├── instance/                   # Application instance files
│   └── finance.db             # SQLite database file
├── run.py                      # Application startup file
├── system_test.py             # Comprehensive test suite
└── app_debug.log              # Application log file
```

## 🔧 Installation and Setup

### Requirements
- Python 3.8+
- pip (Python package manager)

### Step 1: Clone the Project
```bash
git clone https://github.com/UtkayBattal/Personal-Finance-Management-System.git
cd Personal-Finance-Management-System
```

### Step 2: Create Virtual Environment (Recommended)
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### Step 3: Install Required Packages
```bash
pip install flask
pip install flask-sqlalchemy
pip install flask-migrate
pip install flask-login
pip install flask-wtf
pip install wtforms
pip install pandas
pip install numpy
pip install statsmodels
pip install scikit-learn
pip install werkzeug
```

### Step 4: Initialize Database
```bash
# Initialize migration folder
flask db init

# Create initial migration
flask db migrate -m "Initial migration"

# Apply migration
flask db upgrade
```

### Step 5: Run the Application
```bash
python run.py
```

The application will run at `http://localhost:5000`.

## 📊 Database Schema

### User Table
- `id`: Primary key
- `username`: Username (unique)
- `email`: Email address (unique)
- `password`: Hashed password
- `is_active`: Active status
- `created_at`: Account creation date

### Transaction Table
- `id`: Primary key
- `category`: Transaction category
- `amount`: Transaction amount
- `date`: Transaction date
- `type`: Transaction type (income/expense)
- `user_id`: User reference (Foreign Key)

### Budget Table
- `id`: Primary key
- `category`: Budget category
- `amount`: Budget amount
- `period`: Budget period (Monthly/Yearly)
- `date`: Budget creation date
- `user_id`: User reference (Foreign Key)

## 🎯 User Guide

### 1. Account Creation and Login
- Click "Get Started" button from the home page
- Create account with username, email and password
- Login and access the dashboard

### 2. Adding Transactions
- Select "Add Transaction" tab in dashboard
- Choose transaction type (Income/Expense)
- Enter category and amount
- Click "Add" button

### 3. Budget Management
- Select "Budget" tab
- Specify category, amount and period
- Track budget limits

### 4. Statistical Analysis
- Select "Statistics" tab
- Choose chart type (Expense/Income/Budget)
- Set time period
- View detailed analysis

### 5. Transaction Search
- Select "Search Transaction" tab
- Set search criteria
- Filter results

## 🧪 Testing System

The project includes a comprehensive test suite (`system_test.py`):

### Test Categories
1. **Unit Tests**: Model creation and validation
2. **Performance Tests**: SARIMA prediction and dashboard loading
3. **Security Tests**: Password security and unauthorized access
4. **User Experience Tests**: Form validation and error handling
5. **Data Validation Tests**: Transaction and budget controls

### Running Tests
```bash
python system_test.py
```

## 🔒 Security Features

- **Password Hashing**: Secure password storage with PBKDF2-SHA256
- **Session Management**: Secure session control with Flask-Login
- **CSRF Protection**: Form security with WTForms
- **Input Validation**: Validation of all user inputs
- **SQL Injection Protection**: Secure database queries with SQLAlchemy ORM

## 📈 Machine Learning Features

### SARIMA Prediction Model
- **Time Series Analysis**: Predictions based on historical expense data
- **Seasonal Adjustment**: Analysis of monthly cycles
- **6-Month Forecast**: Prediction of future expenses
- **Confidence Intervals**: Reliability analysis of predictions

### Smart Alert System
- **Budget Limit Control**: 80% and 100% limit alerts
- **Trend Analysis**: Expense increase/decrease trends
- **Anomaly Detection**: Unusual spending patterns

## 🎨 Design Features

### Glassmorphism Design
- **Transparent Cards**: Cards with modern glass effect
- **Backdrop Filter**: Blurred background effects
- **Gradient Backgrounds**: Multi-layer color transitions
- **Responsive Grid**: Flexible layout system

### Color Palette
- **Primary**: #1a365d (Dark blue)
- **Secondary**: #2c5282 (Medium blue)
- **Accent**: #48bb78 (Green)
- **Background**: rgba(247, 250, 252, 0.85) (Light gray)

## 🚀 Performance Optimizations

- **Database Indexing**: Indexes for frequently queried fields
- **Lazy Loading**: Loading related data when needed
- **Caching**: Caching of static data
- **Query Optimization**: Optimization of database queries

## 🔧 Development and Contributing

### Development Environment Setup
1. Fork the project
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Standards
- **PEP 8**: Python code style guide
- **Type Hints**: Type specification in function parameters
- **Docstrings**: Function and class documentation
- **Error Handling**: Comprehensive error handling

## 📝 License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## 👨‍💻 Developer

**Utkay Güngör Battal**
- GitHub: [@UtkayBattal](https://github.com/UtkayBattal)
- LinkedIn: [Utkay Güngör Battal](https://www.linkedin.com/in/utkay-güngör-battal-951497263/)

## 🙏 Acknowledgments

- **Flask Community**: Amazing web framework
- **Chart.js**: Interactive chart library
- **Font Awesome**: Icon library
- **Google Fonts**: Poppins font family
- **Statsmodels**: Time series analysis tools

## 📞 Contact

For questions, suggestions, or bug reports:
- Use GitHub Issues
- Send an email
- Contact via LinkedIn

---

**Note**: This project is developed for educational purposes. Additional security measures are recommended for real financial data.
