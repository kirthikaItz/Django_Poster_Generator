from django.contrib import admin
from .models import EventPoster

@admin.register(EventPoster)
class EventPosterAdmin(admin.ModelAdmin):
    # This determines which columns are visible in the admin list view
    list_display = ('title', 'resource_person', 'event_date', 'recipient_email', 'created_at')
    
    # This adds a search bar to filter by title or speaker
    search_fields = ('title', 'resource_person', 'recipient_email')
    
    # This adds a sidebar filter for dates
    list_filter = ('event_date', 'created_at')
    
    # This makes the list ordered by the most recent creation date
    ordering = ('-created_at',)