import django.dispatch

meal_added = django.dispatch.Signal(providing_args=['instance'])

meal_removed = django.dispatch.Signal(providing_args=['instance'])