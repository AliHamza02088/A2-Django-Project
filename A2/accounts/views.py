from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        errors = {}
        
        if not username:
            errors['username'] = "This field is required"
        if not password1:
            errors['password1'] = "This field is required"
        if not password2:   
            errors['password2'] = "This field is required"
        if password1 and password2 and password1 != password2:
            errors['password2'] = "The two password fields didn't match"
        if password1 and len(password1) < 8:
            errors['password1'] = "This password is too short. It must contain at least 8 characters"
        if email and not User.objects.filter(email=email).exists():
            try:
                User.objects.get(email=email)
                errors['email'] = "Enter a valid email address"
            except User.DoesNotExist:
                pass
        if User.objects.filter(username=username).exists():
            errors['username'] = "A user with that username already exists"

        if not errors:
            user = User.objects.create_user(username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
            user.save()
            return redirect('/accounts/login/')
        else:
            return render(request, 'accounts/register.html', {'errors': errors, 'form': request.POST})
    else:
        return render(request, 'accounts/register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/accounts/profile/view/')
        else:
            return render(request, 'accounts/login.html', {'error': "Username or password is invalid", 'form': request.POST})
    else:
        return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect('/accounts/login/')

@login_required
def profile_view(request):
    user = request.user
    data = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
    }
    return JsonResponse(data)

def profile_edit_view(request):
    user = request.user
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        if password1 and password2 and password1 == password2:
            if len(password1) < 8:
                return render(request, 'accounts/profile_edit.html', {'error': 'This password is too short. It must contain at least 8 characters', 'form': request.POST})
            user.set_password(password1)
        elif password1 or password2:
            return render(request, 'accounts/profile_edit.html', {'error': 'The two password fields didn\'t match', 'form': request.POST})
        user.save()
        login(request, user)
        return redirect('/accounts/profile/view/')
    else:
        initial_data = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
        }
        return render(request, 'accounts/profile_edit.html', {'form': initial_data})
    











    '''
    
# Company owner creates account
@login_required
def create_account(request):
    if request.method == "POST":
        company_id = request.POST.get('company')
        company = get_object_or_404(Company, id=company_id, owner=request.user)
        Account.objects.create(company=company, balance=0.00)
        return redirect('dashboard')
    companies = Company.objects.filter(owner=request.user)
    return render(request, 'create_account.html', {'companies': companies})

# Website owner views all accounts
@login_required
def view_all_accounts(request):
    if request.user.is_superuser:
        accounts = Account.objects.all()
    else:
        accounts = Account.objects.filter(company__owner=request.user)
    return render(request, 'view_all_accounts.html', {'accounts': accounts})

# Admin adds income
@login_required
def add_income(request, account_id):
    account = get_object_or_404(Account, id=account_id)
    if request.method == "POST":
        amount = request.POST.get('amount')
        description = request.POST.get('description')
        if request.user.groups.filter(name='admin').exists():
            Income.objects.create(account=account, amount=amount, description=description, created_by=request.user)
            account.balance += float(amount)
            account.save()
            return redirect('view_all_accounts')
    return render(request, 'add_income.html', {'account': account})

# Regular users submit expense, admin approves
@login_required
def submit_expense(request, account_id):
    account = get_object_or_404(Account, id=account_id)
    if request.method == "POST":
        amount = request.POST.get('amount')
        description = request.POST.get('description')
        Expense.objects.create(account=account, amount=amount, description=description, submitted_by=request.user)
        return redirect('dashboard')
    return render(request, 'submit_expense.html', {'account': account})


@login_required
def approve_expense(request, expense_id):
    if request.user.groups.filter(name='admin').exists():
        expense = get_object_or_404(Expense, id=expense_id)
        expense.approved = True
        expense.account.balance -= expense.amount
        expense.save()
        return redirect('dashboard')
    return redirect('unauthorized')

    '''