from django.shortcuts import render , redirect , HttpResponse , get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import Http404 , HttpResponse , HttpResponseForbidden , JsonResponse
from .models import Bank , Branch

# Create your views here.
@login_required
def add_bank_view(request):
    if request.method == "POST":
        name = request.POST.get('name')
        swift_code = request.POST.get('swift_code')
        institution_number = request.POST.get('institution_number')
        description = request.POST.get('description')
        errors = {}
        
        if not name:
            errors['name'] = 'This field is required'
        
        if not swift_code:
            errors['swift_Code'] = "This field is required"
        
        if not institution_number:
            errors['institution_number'] = "This field is required"
        
        if not description:
            errors['description'] = 'This field is required'
        
        if not errors:
            bank = Bank.objects.create(name=name , swift_code=swift_code , institution_number=institution_number , description=description , owner = request.user)
            bank.save()
            return redirect(f'/banks/{bank.id}/details/')
        else:
            return render(request , 'banks/add_bank.html' , {'errors':errors , 'form':request.POST})
    else:
        return render(request , 'banks/add_bank.html')
    
def add_branch_view(request , bank_id):
    bank = get_object_or_404(Bank , id=bank_id)
    if bank.owner != request.user:
        return HttpResponseForbidden()
    if request.method == "POST":
        name = request.POST.get('name')
        transit_number = request.POST.get('transit_number')
        address = request.POST.get('address')
        email = request.POST.get('email')
        capacity = request.POST.get('capacity')
        errors = {}
        
        if not name:
            errors['name'] = 'This field is required'
        if not transit_number:
            errors['transit_number'] = "This field is required"
        if not address:
            errors['address'] = 'This field is required'
        if not email:
            errors['email'] = "Please enter a valid email"
        if not capacity and int(capacity) < 0:
            errors['capacity'] = 'Ensure that the value is greater than 0 or equal to 0'
        if not errors:
            branch = Branch.objects.create(name=name , transit_number=transit_number , address=address , email=email , capacity =capacity , bank=bank)
            branch.save()
            return redirect(f'/banks/branch/{branch.id}/details/')
        else:
            return render(request , 'banks/add_branch.html' , {'errors':errors , 'form':request.user , 'bank':bank})
    else:
        return render(request , 'banks/add_branch.html' , {'bank':bank})
    
def  list_banks_view(request):
    banks = Bank.objects.all()
    return render(request , 'banks/list_banks.html' , {'banks':banks})

def bank_details_view(request , bank_id):
    bank = get_object_or_404(Bank , id=bank_id)
    branches = bank.branches.all()
    return render(request , "banks/bank_details.html" , {'bank':bank , 'branches':branches})

def branch_details_view(request , branch_id):
    branch = get_object_or_404(Branch , id=branch_id)
    if branch.bank.owner != request.user:
        return HttpResponseForbidden()
    return JsonResponse({
        'id' : branch.id,
        'name':branch.name,
        'transit_number':branch.transit_number,
        'address':branch.address,
        'email':branch.email,
        'capacity':branch.capacity,
        'last_modified':branch.last_modified,    
    })
    

        