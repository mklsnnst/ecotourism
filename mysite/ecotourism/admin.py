from django.contrib import admin
from .models import Tour, Booking, Review, Favorite, User, TourUser

class TourUserInline(admin.TabularInline):
    model = TourUser
    extra = 1

class BookingInline(admin.TabularInline):
    model = Booking
    extra = 1

class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1

class FavoriteInline(admin.TabularInline):
    model = Favorite
    extra = 1

@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ('title', 'price_numeric', 'duration_interval', 'status', 'get_available_dates')
    list_filter = ('status', 'available_dates', 'created_by')
    inlines = [TourUserInline, BookingInline, ReviewInline]
    date_hierarchy = 'available_dates'
    search_fields = ('title', 'description')
    list_display_links = ('title',)
    raw_id_fields = ('created_by',)  # Теперь это ForeignKey, всё ок

    @admin.display(description="Дата проведения")
    def get_available_dates(self, obj):
        return obj.available_dates

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'tour', 'booking_date', 'participant_count', 'status')
    list_filter = ('status', 'booking_date')
    date_hierarchy = 'booking_date'
    search_fields = ('user__name', 'tour__title')  # Обновили для ForeignKey
    list_display_links = ('id',)
    raw_id_fields = ('user', 'tour')  # Теперь это ForeignKey, всё ок
    readonly_fields = ('total_price',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'tour', 'rating', 'get_created_date')
    list_filter = ('rating', 'created_date')
    date_hierarchy = 'created_date'
    search_fields = ('review_text',)
    list_display_links = ('id',)

    @admin.display(description="Дата создания")
    def get_created_date(self, obj):
        return obj.created_date

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'tour')
    list_filter = ('user',)
    search_fields = ('user__name', 'tour__title')
    list_display_links = ('id',)
    raw_id_fields = ('user', 'tour')  # Теперь это ForeignKey, всё ок

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'role', 'get_registration_date')
    list_filter = ('role', 'registration_date')
    inlines = [FavoriteInline]
    date_hierarchy = 'registration_date'
    search_fields = ('name', 'email')
    list_display_links = ('name',)
    # Убрали filter_horizontal, так как role — это CharField

    @admin.display(description="Дата регистрации")
    def get_registration_date(self, obj):
        return obj.registration_date

@admin.register(TourUser)
class TourUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'tour', 'user', 'role')
    list_filter = ('role', 'tour')
    search_fields = ('tour__title', 'user__name')
    list_display_links = ('id',)
    raw_id_fields = ('tour', 'user')  # Теперь это ForeignKey, всё ок