from flask import Blueprint, render_template, flash, request, redirect, url_for, session
from .models import Transaction, Budget, User
from .forms import TransactionForm, SearchForm, BudgetForm
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from sqlalchemy import extract
from flask_login import login_user, current_user, login_required, logout_user

# Blueprint tanımlama
main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Successfully logged out!', 'success')
    return redirect(url_for('main.index'))

@main.route('/auth/<action>', methods=['GET', 'POST'])
def auth(action):
    if action == 'login':
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            user = User.query.filter_by(email=email).first()
            
            if user and check_password_hash(user.password, password):
                login_user(user)
                session['user_id'] = user.id
                flash('Successfully logged in!', 'success')
                return redirect(url_for('main.dashboard'))
            else:
                flash('Invalid email or password!', 'error')
                
        return render_template('auth.html', title='Login', action=action)
    
    elif action == 'register':
        if request.method == 'POST':
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')

            existing_user = User.query.filter(
                (User.email == email) | (User.username == username)
            ).first()
            if existing_user:
                flash('This email or username is already in use.', 'error')
                return redirect(url_for('main.auth', action='register'))

            if not username:
                flash('Username cannot be empty.', 'error')
                return redirect(url_for('main.auth', action='register'))

            new_user = User(
                username=username, 
                email=email,
                is_active=True
            )
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! You can now login.', 'success')
            return redirect(url_for('main.auth', action='login'))

    return render_template('auth.html', title='Register', action=action)

@main.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if not current_user.is_authenticated:
        flash('Please login first!', 'error')
        return redirect(url_for('main.auth', action='login'))

    user_id = current_user.id
    add_form = TransactionForm()
    search_form = SearchForm()
    budget_form = BudgetForm()
    transactions = []
    
    # Form kategorilerini güncelle
    add_form.update_category_choices()
    search_form.update_category_choices()
    
    # Varsayılan değerleri tanımla
    active_section = request.args.get('active_section', 'add')
    selected_graph_type = request.form.get('graph_type', 'expense')
    period_type = request.form.get('period_type', 'monthly')
    selected_year = int(request.form.get('selected_year', datetime.now().year))
    selected_month = int(request.form.get('selected_month', datetime.now().month))
    months = ['January', 'February', 'March', 'April', 'May', 'June', 
             'July', 'August', 'September', 'October', 'November', 'December']
    
    # Grafik verileri için varsayılan değerler
    category_labels = []
    category_data = []
    daily_data = {}
    monthly_data = {}
    budget_warnings = []  # Bütçe uyarıları için liste

    if request.method == 'POST':
        if active_section == 'add' and add_form.validate_on_submit():
            try:
                new_transaction = Transaction(
                    category=add_form.category.data,
                    amount=add_form.amount.data,
                    type=add_form.type.data,
                    user_id=user_id,
                    date=datetime.utcnow()
                )
                db.session.add(new_transaction)
                db.session.commit()
                flash('Transaction added successfully!', 'success')
                return redirect(url_for('main.dashboard', active_section='add'))
            except Exception as e:
                flash(f'Error adding transaction: {e}', 'error')

        # Search işlemi
        elif active_section == 'search' and search_form.validate_on_submit():
            query = Transaction.query.filter_by(user_id=user_id)

            if search_form.category.data:
                query = query.filter(Transaction.category == search_form.category.data)
            if search_form.min_amount.data:
                query = query.filter(Transaction.amount >= search_form.min_amount.data)
            if search_form.max_amount.data:
                query = query.filter(Transaction.amount <= search_form.max_amount.data)
            if search_form.type.data:
                query = query.filter(Transaction.type == search_form.type.data)

            transactions = query.all()

        # Budget ekleme işlemi
        elif active_section == 'budget' and budget_form.validate_on_submit():
            try:
                new_budget = Budget(
                    category=budget_form.category.data,
                    amount=budget_form.amount.data,
                    period=budget_form.period.data,
                    user_id=user_id,
                    date=datetime.utcnow()
                )
                db.session.add(new_budget)
                db.session.commit()
                flash('Budget added successfully!', 'success')
                return redirect(url_for('main.dashboard', active_section='budget'))
            except Exception as e:
                flash(f'Error adding budget: {e}', 'error')

    # İstatistikler için veri hazırlama
    if active_section == 'statistics':
        # Tarih aralığını belirle
        if period_type == 'yearly':
            start_date = datetime(selected_year, 1, 1)
            end_date = datetime(selected_year + 1, 1, 1)
        else:  # monthly
            start_date = datetime(selected_year, selected_month, 1)
            if selected_month == 12:
                end_date = datetime(selected_year + 1, 1, 1)
            else:
                end_date = datetime(selected_year, selected_month + 1, 1)

        # Seçilen grafik türüne göre veri hazırla
        if selected_graph_type in ['expense', 'income']:
            # Transaction verilerini getir
            transactions = Transaction.query.filter(
                Transaction.user_id == user_id,
                Transaction.type == selected_graph_type,
                Transaction.date >= start_date,
                Transaction.date < end_date
            ).all()

            # Kategori bazlı toplamları hesapla
            category_totals = {}
            daily_data = {}
            monthly_data = {}

            # Kategorileri belirle
            categories = ['Clothing', 'Food', 'Market', 'Entertainment', 'Other'] if selected_graph_type == 'expense' else \
                        ['Salary/Wages', 'Freelancing/Consulting', 'Investment Income', 'Rental Income', 'Business Income', 'Other']

            # Kategori toplamlarını hesapla
            for transaction in transactions:
                if transaction.category not in category_totals:
                    category_totals[transaction.category] = 0
                    daily_data[transaction.category] = [0] * 31
                    monthly_data[transaction.category] = [0] * 12
                
                category_totals[transaction.category] += transaction.amount
                
                # Günlük dağılım için
                if period_type == 'monthly':
                    day_idx = transaction.date.day - 1
                    daily_data[transaction.category][day_idx] += transaction.amount
                
                # Aylık dağılım için
                month_idx = transaction.date.month - 1
                monthly_data[transaction.category][month_idx] += transaction.amount

            # Grafik verilerini hazırla
            category_labels = []
            category_data = []
            
            # Her kategori için veri ekle (sıfır değerler dahil)
            for category in categories:
                category_labels.append(category)
                category_data.append(category_totals.get(category, 0))

        elif selected_graph_type == 'budget':
            print(f"Selected date range: {start_date} to {end_date}")  # Debug log
            
            # Bütçe verilerini getir
            budgets = Budget.query.filter(
                Budget.user_id == user_id,
                Budget.date >= start_date,
                Budget.date < end_date
            ).all()
            
            category_totals = {}
            expense_totals = {}
            forecast_data = {}  # Tahmin verilerini saklamak için
            
            # Bütçe toplamlarını hesapla
            for budget in budgets:
                if budget.category not in category_totals:
                    category_totals[budget.category] = 0
                    expense_totals[budget.category] = 0
                category_totals[budget.category] += budget.amount

            # Harcama verilerini getir
            expenses = Transaction.query.filter(
                Transaction.user_id == user_id,
                Transaction.type == 'expense',
                Transaction.date >= start_date,
                Transaction.date < end_date
            ).all()
            
            # Harcama toplamlarını hesapla
            total_expenses = 0  # Debug için toplam harcama
            for expense in expenses:
                if expense.category in expense_totals:
                    expense_totals[expense.category] += expense.amount
                    total_expenses += expense.amount
            
            print(f"Total expenses for the period: {total_expenses}")  # Debug log
            
            # Tahmin verilerini hazırla
            forecast_result = Transaction.predict_future_expenses(
                user_id, 
                start_date=start_date,
                end_date=end_date
            )
            
            if forecast_result is not None:
                # Ay etiketlerini hazırla
                next_months = []
                current_date = end_date
                
                for _ in range(6):
                    next_months.append(current_date.strftime('%B %Y'))
                    if current_date.month == 12:
                        current_date = datetime(current_date.year + 1, 1, 1)
                    else:
                        current_date = datetime(current_date.year, current_date.month + 1, 1)
                
                forecast_data = {
                    'Total': {
                        'forecast': forecast_result['forecast'],
                        'actual': forecast_result['actual'],
                        'months': next_months
                    }
                }
                print(f"Forecast data prepared: {forecast_data}")  # Debug log
            else:
                next_months = []
                current_date = end_date
                for _ in range(6):
                    next_months.append(current_date.strftime('%B %Y'))
                    if current_date.month == 12:
                        current_date = datetime(current_date.year + 1, 1, 1)
                    else:
                        current_date = datetime(current_date.year, current_date.month + 1, 1)
                
                forecast_data = {
                    'Total': {
                        'forecast': [0] * 6,
                        'actual': [0] * 6,
                        'months': next_months
                    }
                }

            # Grafik verilerini hazırla
            category_labels = list(category_totals.keys())
            category_data = {
                'budget': [category_totals[cat] for cat in category_labels],
                'expense': [expense_totals[cat] for cat in category_labels],
                'forecast': forecast_data
            }

            # Bütçe uyarılarını hazırla
            budget_warnings = []
            for category in category_totals:
                if category in expense_totals and category_totals[category] > 0:
                    percentage = (expense_totals[category] / category_totals[category]) * 100
                    if percentage >= 80:
                        warning = {
                            'category': category,
                            'message': 'Budget limit is almost reached!' if percentage < 100 else 'Budget limit exceeded!',
                            'percentage': percentage
                        }
                        budget_warnings.append(warning)

    return render_template(
        'dashboard.html',
        add_form=add_form,
        search_form=search_form,
        budget_form=budget_form,
        transactions=transactions,
        active_section=active_section,
        selected_graph_type=selected_graph_type,
        period_type=period_type,
        selected_year=selected_year,
        selected_month=selected_month,
        months=months,
        category_labels=category_labels,
        category_data=category_data,
        daily_data=daily_data,
        monthly_data=monthly_data,
        budget_warnings=budget_warnings  # Uyarıları template'e gönder
    )

@main.route('/add_budget', methods=['POST'])
def add_budget():
    if 'user_id' not in session:
        flash('Lütfen giriş yapın!', 'danger')
        return redirect(url_for('main.auth', action='login'))

    form = BudgetForm()
    if form.validate_on_submit():
        try:
            new_budget = Budget(
                category=form.category.data,
                amount=form.amount.data,
                period=form.period.data,
                date=datetime.utcnow(),  # Şu anki tarihi ekle
                user_id=session['user_id']
            )
            db.session.add(new_budget)
            db.session.commit()
            flash('Bütçe başarıyla eklendi!', 'success')
        except Exception as e:
            flash(f'Bütçe eklenirken bir hata oluştu: {e}', 'danger')
    
    return redirect(url_for('main.dashboard', active_section='budget'))

@main.route('/add_transaction', methods=['GET', 'POST'])
def add_transaction():
    if 'user_id' not in session:
        flash('Lütfen giriş yapın!', 'danger')
        return redirect(url_for('main.auth', action='login'))

    form = TransactionForm()
    if form.validate_on_submit():
        try:
            new_transaction = Transaction(
                category=form.category.data,
                amount=form.amount.data,
                type=form.type.data,
                user_id=session['user_id']
            )
            db.session.add(new_transaction)
            db.session.commit()
            flash('İşlem başarıyla eklendi!', 'success')
            return redirect(url_for('main.dashboard', active_section='add'))
        except Exception as e:
            flash('İşlem eklenirken bir hata oluştu.', 'danger')
    return render_template('add_transaction.html', form=form)

@main.route('/search_transactions', methods=['GET', 'POST'])
def search_transactions():
    if 'user_id' not in session:
        flash('Lütfen giriş yapın!', 'danger')
        return redirect(url_for('main.auth', action='login'))

    form = SearchForm()
    transactions = []

    if form.validate_on_submit():
        # Parametreleri kontrol et
        category = form.category.data
        min_amount = form.min_amount.data
        max_amount = form.max_amount.data
        transaction_type = form.type.data

        # Veritabanı sorgusu
        query = Transaction.query.filter_by(user_id=session['user_id'])
        if category:
            query = query.filter(Transaction.category == category)
        if min_amount:
            query = query.filter(Transaction.amount >= min_amount)
        if max_amount:
            query = query.filter(Transaction.amount <= max_amount)
        if transaction_type:
            query = query.filter(Transaction.type == transaction_type)

        transactions = query.all()
        if transactions:
            flash('Arama sonuçları başarıyla getirildi.', 'success')
        else:
            flash('Arama kriterlerinize uygun sonuç bulunamadı.', 'info')

    return render_template('search_transactions.html', form=form, transactions=transactions)
