from django.contrib import admin
from .models import DataLog,Location, Sensor, SensorType, Measurement, SensorStatus, DataLogLevel, MeasurementStatus
# from .models import DataPoint


# @admin.register(DataPoint)
# class DataPointAdmin(admin.ModelAdmin):
#     list_display = ('source', 'timestamp', 'value')

@admin.register(Measurement)
class MeasurementAdmin(admin.ModelAdmin):
    list_display = ('id', 'sensor', 'value', 'status', 'timestamp')
    list_filter = (
        'status',
        'sensor__location__room',
        'sensor__type__name'
    )
    date_hierarchy = 'timestamp'
    search_fields = ('sensor__name', 'sensor__location__room')


@admin.register(DataLog)
class DataLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'level', 'message', 'measurement')
    list_filter = ('level', 'timestamp')
    date_hierarchy = 'timestamp'
    search_fields = ('message',)


@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'type', 'location', 'last_communication')
    list_filter = ('status', 'type__name', 'location__room')
    search_fields = ('name', 'location__room')

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'room', 'floor')
    list_filter = ('floor',)
    search_fields = ('room',)

@admin.register(SensorType)
class SensorTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'default_unit', 'min_value', 'max_value')
    search_fields = ('name', 'default_unit')