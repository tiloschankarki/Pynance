from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import GoalForm
from .models import Goal


@login_required
def goals_page(request):
    goals = Goal.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'goals/goals.html', {'goals': goals})


@login_required
def goal_create(request):
    if request.method == 'POST':
        form = GoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            return redirect('goals:page')
    else:
        form = GoalForm()

    return render(request, 'goals/goal_form.html', {'form': form, 'page_title': 'Add Goal'})


@login_required
def goal_update(request, pk):
    goal = get_object_or_404(Goal, pk=pk, user=request.user)

    if request.method == 'POST':
        form = GoalForm(request.POST, instance=goal)
        if form.is_valid():
            form.save()
            return redirect('goals:page')
    else:
        form = GoalForm(instance=goal)

    return render(request, 'goals/goal_form.html', {'form': form, 'page_title': 'Edit Goal'})


@login_required
def goal_delete(request, pk):
    goal = get_object_or_404(Goal, pk=pk, user=request.user)

    if request.method == 'POST':
        goal.delete()
        return redirect('goals:page')

    return render(request, 'goals/goal_confirm_delete.html', {'goal': goal})