try:
    from threading import local
except ImportError:
    from django.utils._threading_local import local  # noqa

thread_local = local()


# Create your helper functions here.


def set_current_localize_application(localize_application):
    setattr(thread_local, "localize_application", localize_application)


def unset_current_localize_application():
    setattr(thread_local, "localize_application", None)


def current_localize_application():
    return getattr(thread_local, "localize_application", None)


def current_localize_application_id():
    return getattr(current_localize_application(), 'id', 0)


def current_localize_application_hash():
    return getattr(current_localize_application(), 'hash', '')
