# -*- coding: utf-8 -*-

from functools import wraps, partial

from django.conf import settings
from django.core.cache import cache


def model_cached_property(method=None, timeout=getattr(settings, "MODEL_CACHED_PROPERTY_TIMEOUT", 60)):

    # @wraps(method)
    # def function_wrapper(object, **kwargs):
    #     # print(method.__name__)
    #     for item in object.all():
    #         print(item.id)
    #     print(object.all())
    #
    # return function_wrapper

    if method is None:
        return partial(model_cached_property, timeout=timeout)


    def function_wrapper(model_object, *args, **kwargs):
        cache_key = 'nsp_core_model_cached_property_{}_{}_{}_{}_'.format(
            model_object.model._meta.db_table, model_object.first().id, method.__name__,
            "{} {}".format(args, kwargs).replace(" ", "_")
        )
        result = cache.get(cache_key)
        print('Article')
        print(model_object.first().id)
        print(cache_key)

        if result is not None:
            return result
        result = method(model_object, *args, **kwargs)
        print(result)
        cache.set(cache_key, result, timeout=timeout)
        return result

    return function_wrapper