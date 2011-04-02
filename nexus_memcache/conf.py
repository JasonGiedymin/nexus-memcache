'''
To avoid backend validation for custom backends, supply 'NEXUS_MEMCACHE_BACKEND'.
Validation only occurs for 'default' entries supplied by Django 1.3.x.
Fallback to 'CACHE_BACKEND' on Django Versions prior to 1.3.x.

Currently does try to loop through found memcached backends, easier
to just set the key described above manually however.

I consider this a hack until Nexus-Memcache is able to read the entire
CACHES dictionary (nexus_modules.py) in place of the work done up front
here.
'''

import django
from django.conf import settings
from django.core import cache


_NEXUS_MEM_KEY = 'NEXUS_MEMCACHE_BACKEND'

_NEXUS_IMPORT_ERR_MSG = 'Nexus Memcached default backend improperly configured. ' + \
                        'Try NEXUS_MEMCACHE_BACKEND in settings.py.'


class NexusCacheImproperlyConfigured(Exception):
    '''
    Nexus Memcached backend declaration is somehow improperly configured.
    Try to set NEXUS_MEMCACHE_BACKEND in settings.py manually.
    '''
    pass


if float(django.get_version()) < 1.3: # For all versions prior to 1.3.x
    BACKEND = getattr(settings, NEXUS_MEM_KEY, settings.CACHE_BACKEND)
else: # For all versions 1.3.x and after
    # Does a defined default exist?
    if not settings.CACHES.has_key(cache.DEFAULT_CACHE_ALIAS):
        raise NexusCacheImproperlyConfigured(_NEXUS_IMPORT_ERR_MSG)
    else: # Grab all the backends
        backend, location, params = cache.parse_backend_conf(cache.DEFAULT_CACHE_ALIAS)
        location_string = ';'.join(location)
        BACKEND = ('memcached://%s/' % location_string)


