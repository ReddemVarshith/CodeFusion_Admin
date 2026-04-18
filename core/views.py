from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from .models import Team, TeamMember
import csv

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'core/login.html')

@login_required
def dashboard(request):
    total_teams = Team.objects.count()
    total_members = TeamMember.objects.count()
    
    # Stats by team size
    team_size_stats = Team.objects.values('team_size').annotate(count=Count('id')).order_by('team_size')
    
    # Recently registered teams
    recent_teams = Team.objects.all().order_by('-created_at')[:5]
    
    context = {
        'total_teams': total_teams,
        'total_members': total_members,
        'team_size_stats': team_size_stats,
        'recent_teams': recent_teams,
    }
    return render(request, 'core/dashboard.html', context)

@login_required
def team_list(request):
    teams = Team.objects.all()
    
    # Filtering
    search_query = request.GET.get('search', '')
    if search_query:
        teams = teams.filter(
            Q(team_name__icontains=search_query) | 
            Q(utr_id__icontains=search_query)
        )
        
    team_size = request.GET.get('team_size')
    if team_size:
        teams = teams.filter(team_size=team_size)
        
    college_code = request.GET.get('college_code')
    if college_code:
        teams = teams.filter(members__college_code__icontains=college_code).distinct()
    
    context = {
        'teams': teams,
        'search_query': search_query,
    }
    return render(request, 'core/teams.html', context)

@login_required
def member_list(request):
    members = TeamMember.objects.all()
    
    # Filtering
    search_query = request.GET.get('search', '')
    if search_query:
        members = members.filter(
            Q(name__icontains=search_query) | 
            Q(email__icontains=search_query) |
            Q(roll_no__icontains=search_query)
        )
        
    college = request.GET.get('college')
    if college:
        members = members.filter(college_name__icontains=college)
        
    college_code = request.GET.get('college_code')
    if college_code:
        members = members.filter(college_code__icontains=college_code)
        
    tshirt_size = request.GET.get('tshirt_size')
    if tshirt_size:
        members = members.filter(tshirt_size=tshirt_size)
    
    context = {
        'members': members,
        'search_query': search_query,
    }
    return render(request, 'core/members.html', context)

@login_required
def export_to_excel(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="teams_data.csv"'

    writer = csv.writer(response)
    writer.writerow(['team name', 'team member name', 'member_email', 'phone number'])

    members = TeamMember.objects.select_related('team').all()
    for member in members:
        # User format requires member_email, I'll use the email field from the model.
        writer.writerow([
            member.team.team_name,
            member.name,
            member.email,
            member.phone_number,
        ])
    return response

@login_required
def export_college_team_count(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="college_team_count.csv"'

    writer = csv.writer(response)
    writer.writerow(['College code', 'No.ofteams'])

    # Count each team exactly once using its first member's college code
    teams = Team.objects.prefetch_related('members').all()
    college_counts = {}
    
    for team in teams:
        members = team.members.all()
        code = members[0].college_code if members else 'No Members'
        code = str(code).upper() # Normalize casing to prevent duplicates
        college_counts[code] = college_counts.get(code, 0) + 1

    # Sort so the highest count is on top
    sorted_counts = sorted(college_counts.items(), key=lambda x: x[1], reverse=True)
    
    for code, count in sorted_counts:
        writer.writerow([
            code,
            f"{count} teams"
        ])
        
    return response
