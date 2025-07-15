from flask_wtf import FlaskForm
from wtforms import FloatField, SelectField, SubmitField, StringField
from wtforms.validators import DataRequired, Optional, NumberRange

# Form for adding a new transaction
class TransactionForm(FlaskForm):
    # Expense categories
    CATEGORY_CHOICES_EXPENSE = [
        ('Clothing', 'Clothing'),
        ('Food', 'Food'),
        ('Market', 'Market'),
        ('Entertainment', 'Entertainment'),
        ('Other', 'Other')
    ]

    # Income categories
    CATEGORY_CHOICES_INCOME = [
        ('Salary/Wages', 'Salary/Wages'),
        ('Freelancing/Consulting', 'Freelancing/Consulting'),
        ('Investment Income', 'Investment Income'),
        ('Rental Income', 'Rental Income'),
        ('Business Income', 'Business Income'),
        ('Other', 'Other')
    ]

    # Field for entering the transaction amount (must be positive)
    amount = FloatField('Amount', validators=[DataRequired(), NumberRange(min=0, message="Amount must be positive")])

    # Dropdown for selecting a category (dynamically updated based on type)
    category = SelectField('Category', choices=[], validators=[DataRequired()])

    # Dropdown for selecting the type of transaction (income or expense)
    type = SelectField('Type', choices=[('income', 'Income'), ('expense', 'Expense')], validators=[DataRequired()])

    # Submit button for the form
    submit = SubmitField('Submit')

    def update_category_choices(self):
        """Update category choices based on the selected transaction type"""
        if self.type.data == 'income':
            self.category.choices = self.CATEGORY_CHOICES_INCOME
        else:
            self.category.choices = self.CATEGORY_CHOICES_EXPENSE


# Form for searching transactions
class SearchForm(FlaskForm):
    # Expense categories
    CATEGORY_CHOICES_EXPENSE = [
        ('Clothing', 'Clothing'),
        ('Food', 'Food'),
        ('Market', 'Market'),
        ('Entertainment', 'Entertainment'),
        ('Other', 'Other')
    ]

    # Income categories
    CATEGORY_CHOICES_INCOME = [
        ('Salary/Wages', 'Salary/Wages'),
        ('Freelancing/Consulting', 'Freelancing/Consulting'),
        ('Investment Income', 'Investment Income'),
        ('Rental Income', 'Rental Income'),
        ('Business Income', 'Business Income'),
        ('Other', 'Other')
    ]

    # Field for specifying the minimum transaction amount
    min_amount = FloatField('Minimum Amount', validators=[Optional(), NumberRange(min=0, message="Amount must be positive")])

    # Field for specifying the maximum transaction amount
    max_amount = FloatField('Maximum Amount', validators=[Optional(), NumberRange(min=0, message="Amount must be positive")])

    # Dropdown for selecting a category (dynamically updated based on type)
    category = SelectField('Category', choices=[], validators=[Optional()])

    # Dropdown for selecting the type of transaction (income or expense)
    type = SelectField('Type', choices=[('income', 'Income'), ('expense', 'Expense')], validators=[Optional()])

    # Submit button for the search form
    submit = SubmitField('Search')

    def update_category_choices(self):
        #Update category choices based on the selected transaction type #
        if self.type.data == 'income':
            self.category.choices = self.CATEGORY_CHOICES_INCOME
        else:
            self.category.choices = self.CATEGORY_CHOICES_EXPENSE


# Form for adding a budget
class BudgetForm(FlaskForm):
    CATEGORY_CHOICES = [
        ('Clothing', 'Clothing'),
        ('Food', 'Food'),
        ('Market', 'Market'),
        ('Entertainment', 'Entertainment'),
        ('Other', 'Other')
    ]
    
    category = SelectField('Category', choices=CATEGORY_CHOICES, validators=[DataRequired()])
    amount = FloatField('Amount', validators=[DataRequired(), NumberRange(min=0, message="Amount must be positive")])
    period = SelectField('Period', choices=[('monthly', 'Monthly'), ('yearly', 'Yearly')], validators=[DataRequired()])
    submit = SubmitField('Add Budget')

