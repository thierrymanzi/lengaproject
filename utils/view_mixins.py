"""
The classes here a borrowed from rest frame_work generics classes.
The have been updated to save custom headers(fcm-key and app-version). All Mobile
App views should inherit from one of these classes
"""

from functools import wraps

from rest_framework import mixins
from rest_framework.generics import GenericAPIView

from users.models import User


# Decorator function to hide saving of custom headers to the database
def save_headers(func):
    @wraps(func)  # We don't want to lose our method name
    def inner_method(*args, **kwargs):
        user = User.objects.filter(id=args[1].user.id)

        if user.exists():
            user = user[0]
            headers = args[1].headers
            updated = False

            if headers and headers.get('fcm-key'):
                user.fcm_key = headers.get('fcm-key')
                updated = True

            if headers and headers.get('app-version'):
                user.app_version = headers.get('app-version')
                updated = True
            # Only save when either one or both fields are updated
            if updated:
                user.save()
        return func(*args, **kwargs)
    return inner_method


class DestroyModelMixin(mixins.DestroyModelMixin):
    def perform_destroy(self, instance):
        try:
            instance.is_active = False
            instance.save(update_fields=['is_active'])
        except (ValueError, AttributeError):
            instance.delete()


class CreateAPIView(mixins.CreateModelMixin,
                    GenericAPIView):
    """
    Concrete view for creating a model instance.
    """
    @save_headers
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ListAPIView(mixins.ListModelMixin,
                  GenericAPIView):
    """
    Concrete view for listing a queryset.
    """
    @save_headers
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class RetrieveAPIView(mixins.RetrieveModelMixin,
                      GenericAPIView):
    """
    Concrete view for retrieving a model instance.
    """
    @save_headers
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class DestroyAPIView(DestroyModelMixin,
                     GenericAPIView):
    """
    Concrete view for deleting a model instance.
    """
    @save_headers
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class UpdateAPIView(mixins.UpdateModelMixin,
                    GenericAPIView):
    """
    Concrete view for updating a model instance.
    """
    @save_headers
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @save_headers
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class ListCreateAPIView(mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        GenericAPIView):
    """
    Concrete view for listing a queryset or creating a model instance.
    """
    @save_headers
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @save_headers
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class RetrieveUpdateAPIView(mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            GenericAPIView):
    """
    Concrete view for retrieving, updating a model instance.
    """
    @save_headers
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @save_headers
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @save_headers
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class RetrieveDestroyAPIView(mixins.RetrieveModelMixin,
                             DestroyModelMixin,
                             GenericAPIView):
    """
    Concrete view for retrieving or deleting a model instance.
    """
    @save_headers
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @save_headers
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class RetrieveUpdateDestroyAPIView(mixins.RetrieveModelMixin,
                                   mixins.UpdateModelMixin,
                                   DestroyModelMixin,
                                   GenericAPIView):
    """
    Concrete view for retrieving, updating or deleting a model instance.
    """
    @save_headers
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @save_headers
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @save_headers
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @save_headers
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
