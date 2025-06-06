from django.shortcuts import render, get_object_or_404, redirect
from django.db import models
from .models import Tour, Review, User
from django import forms

class TourForm(forms.ModelForm):
    class Meta:
        model = Tour
        fields = ['title', 'description', 'price_numeric', 'duration_interval', 'start_location', 'end_location', 'max_participants', 'available_dates', 'status']
        widgets = {
            'available_dates': forms.DateInput(attrs={'type': 'date'}),
        }

def home(request):
    tours = Tour.objects.all().order_by('-available_dates')[:10]
    avg_rating = Review.objects.aggregate(models.Avg('rating'))['rating__avg'] or 0
    non_empty_reviews = Review.objects.exclude(review_text='')
    recommended_tours = Tour.objects.all().order_by('-available_dates')[:3]
    return render(request, 'ecotourism/home.html', {
        'tours': tours,
        'reviews_count': non_empty_reviews.count(),
        'avg_rating': avg_rating,
        'recommended_tours': recommended_tours
    })

def search(request):
    query = request.GET.get('q', '')
    tours = Tour.objects.filter(
        models.Q(title__icontains=query) |
        models.Q(description__icontains=query) |
        models.Q(start_location__icontains=query)
    )
    return render(request, 'ecotourism/search_results.html', {'tours': tours, 'query': query})

def tour_list(request):
    tours = Tour.objects.all().order_by('available_dates')
    return render(request, 'ecotourism/tour_list.html', {'tours': tours})

def tour_detail(request, tour_id):
    tour = get_object_or_404(Tour, pk=tour_id)
    reviews = Review.objects.filter(tour=tour)
    return render(request, 'ecotourism/tour_detail.html', {'tour': tour, 'reviews': reviews})

def add_tour(request):
    if request.method == 'POST':
        form = TourForm(request.POST)
        if form.is_valid():
            tour = form.save(commit=False)
            # Проверяем, есть ли пользователи, если нет — создаём временного
            if User.objects.exists():
                tour.created_by = User.objects.first()
            else:
                # Создаём временного пользователя, если таблица пуста
                default_user = User.objects.create(name="Admin", email="admin@example.com", password="admin123", role="Админ")
                tour.created_by = default_user
            tour.save()
            return redirect('ecotourism:home')
    else:
        form = TourForm()
    return render(request, 'ecotourism/add_tour.html', {'form': form})

def edit_tour(request, tour_id):
    tour = get_object_or_404(Tour, pk=tour_id)
    if request.method == 'POST':
        form = TourForm(request.POST, instance=tour)
        if form.is_valid():
            form.save()
            return redirect('ecotourism:tour_detail', tour_id=tour_id)
    else:
        form = TourForm(instance=tour)
    return render(request, 'ecotourism/edit_tour.html', {'form': form, 'tour': tour})

def delete_tour(request, tour_id):
    tour = get_object_or_404(Tour, pk=tour_id)
    if request.method == 'POST':
        tour.delete()
        return redirect('ecotourism:home')
    return render(request, 'ecotourism/delete_tour.html', {'tour': tour})