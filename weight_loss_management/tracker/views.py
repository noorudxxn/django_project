from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SignupForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import WeightForm
from .models import Weight
from django.utils import timezone
from django.contrib import messages
from django.db import IntegrityError, transaction
from django.core.paginator import Paginator
from django.utils.dateparse import parse_date
from django.shortcuts import get_object_or_404
from django.contrib.auth import logout

def signup(request):

    if request.method == 'POST':

        form = SignupForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(request, 'Registration successful. Please login.')

            return redirect('login')

    else:

        form = SignupForm()

    return render(request, 'tracker/signup.html', {'form': form})


#login
def user_login(request):

    if request.method == 'POST':

        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():

            user = form.get_user()

            login(request, user)

            return redirect('dashboard')

    else:

        form = AuthenticationForm()

    return render(request, 'tracker/login.html', {'form': form})


#dashboard
@login_required
def dashboard(request):

    return render(request, 'tracker/dashboard.html')




#Add weight
@login_required
def add_weight(request):

    if request.method == 'POST':

        form = WeightForm(request.POST)

        if form.is_valid():

            today = timezone.localdate()

            exists = Weight.objects.filter(
                user=request.user,
                date=today
            ).exists()

            if exists:

                messages.error(
                    request,
                    'You have already added your weight today!'
                )

                return redirect('add_weight')

            weight = form.save(commit=False)

            weight.user = request.user
            weight.date = today

            try:

                with transaction.atomic():
                    weight.save()

                messages.success(
                    request,
                    'Weight added successfully!'
                )

                return redirect('dashboard')

            except IntegrityError:

                messages.error(
                    request,
                    'You have already added your weight today!'
                )

                return redirect('add_weight')

    else:

        form = WeightForm()

    return render(request, 'tracker/add_weight.html', {'form': form})





#weight_list
@login_required
def weight_list(request):

    weights = Weight.objects.filter(
        user=request.user
    ).order_by('-date', '-created_at')

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date:
        start = parse_date(start_date)

        if start:
            weights = weights.filter(date__gte=start)

    if end_date:
        end = parse_date(end_date)

        if end:
            weights = weights.filter(date__lte=end)

    # Count all filtered records
    total_records = weights.count()

    # Calculate weight difference
    oldest_weight = None
    newest_weight = None
    weight_difference = None
    difference_type = None

    has_weight_difference = total_records >= 2

    if has_weight_difference:

        oldest_weight = weights.order_by(
            'date', 'created_at'
        ).first()

        newest_weight = weights.order_by(
            '-date', '-created_at'
        ).first()

        weight_difference = newest_weight.weight - oldest_weight.weight

        if weight_difference > 0:
            difference_type = 'gained'

        elif weight_difference < 0:
            difference_type = 'lost'

        else:
            difference_type = 'no_change'

    # Pagination
    paginator = Paginator(weights, 1)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    return render(request, 'tracker/weight_list.html', {
        'weights': page_obj,
        'start_date': start_date or '',
        'end_date': end_date or '',
        'has_weight_difference': has_weight_difference,
        'weight_difference': abs(weight_difference) if weight_difference is not None else None,
        'difference_type': difference_type,
        'oldest_weight': oldest_weight,
        'newest_weight': newest_weight,
    })






#edit_weight
@login_required
def edit_weight(request, id):

    weight = get_object_or_404(
        Weight,
        id=id,
        user=request.user
    )

    if request.method == 'POST':

        form = WeightForm(request.POST, instance=weight)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Weight updated successfully!'
            )

            return redirect('weight_list')

    else:

        form = WeightForm(instance=weight)

    return render(request, 'tracker/edit_weight.html', {'form': form})




#delete_weight
@login_required
def delete_weight(request, id):

    weight = get_object_or_404(
        Weight,
        id=id,
        user=request.user
    )

    if request.method == 'POST':

        weight.delete()

        messages.success(
            request,
            'Weight record deleted successfully!'
        )

    return redirect('weight_list')


#user_logout
@login_required
def user_logout(request):

    if request.method == 'POST':

        logout(request)

        messages.success(
            request,
            'You have logged out successfully!'
        )

        return redirect('login')

    return redirect('dashboard')