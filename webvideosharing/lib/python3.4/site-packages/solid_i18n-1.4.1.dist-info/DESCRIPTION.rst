Django solid\_i18n urls
=======================

|Build Status| |Coverage Status| |Pypi version|

solid\_i18n contains middleware and url patterns to use default language
at root path (without language prefix).

Default language is set in settings.LANGUAGE\_CODE.

Deprecation notice
------------------

Starting from `Django
1.10 <https://docs.djangoproject.com/en/dev/releases/1.10/#internationalization>`__,
built-in ``i18n_patterns`` accept optional argument
``prefix_default_language``. If it is ``False``, then Django will serve
url without language prefix by itself. Look
`docs <https://docs.djangoproject.com/en/dev/topics/i18n/translation/#django.conf.urls.i18n.i18n_patterns>`__
for more details.

This package can still be useful in following cases (look below for
settings details): - You need
``settings.SOLID_I18N_USE_REDIRECTS = True`` behaviour - You need
``settings.SOLID_I18N_HANDLE_DEFAULT_PREFIX = True`` behaviour - You
need ``settings.SOLID_I18N_DEFAULT_PREFIX_REDIRECT = True`` behaviour -
You need ``settings.SOLID_I18N_PREFIX_STRICT = True`` behaviour

In all other cases no need in current package, just use Django>=1.10.

Requirements
------------

-  python (2.7, 3.4, 3.5)
-  django (1.8, 1.9, 1.10)

Release notes
-------------

`Here <https://github.com/st4lk/django-solid-i18n-urls/blob/master/RELEASE_NOTES.md>`__

Behaviour
---------

There are two modes:

1. ``settings.SOLID_I18N_USE_REDIRECTS = False`` (default). In that case
   i18n will not use redirects at all. If request doesn't have language
   prefix, then default language will be used. If request does have
   prefix, language from that prefix will be used.

2. ``settings.SOLID_I18N_USE_REDIRECTS = True``. In that case, for root
   paths (without prefix), django will `try to
   discover <https://docs.djangoproject.com/en/dev/topics/i18n/translation/#how-django-discovers-language-preference>`__
   user preferred language. If it doesn't equal to default language,
   redirect to path with corresponding prefix will occur. If preferred
   language is the same as default, then that request path will be
   processed (without redirect). Also see notes below.

Quick start
-----------

1. Install this package to your python distribution:

   ::

       pip install solid_i18n

2. Set languages in settings.py:

   ::

       # Default language, that will be used for requests without language prefix
       LANGUAGE_CODE = 'en'

       # supported languages
       LANGUAGES = (
           ('en', 'English'),
           ('ru', 'Russian'),
       )

       # enable django translation
       USE_I18N = True

       # Optional. If you want to use redirects, set this to True
       SOLID_I18N_USE_REDIRECTS = False

3. Add ``SolidLocaleMiddleware`` instead of
   `LocaleMiddleware <https://docs.djangoproject.com/en/dev/ref/middleware/#django.middleware.locale.LocaleMiddleware>`__
   to ``MIDDLEWARE_CLASSES``:

   ::

       MIDDLEWARE_CLASSES = (
          'django.contrib.sessions.middleware.SessionMiddleware',
          'solid_i18n.middleware.SolidLocaleMiddleware',
          'django.middleware.common.CommonMiddleware',
       )

4. Use ``solid_i18n_patterns`` instead of
   `i18n\_patterns <https://docs.djangoproject.com/en/dev/topics/i18n/translation/#django.conf.urls.i18n.i18n_patterns>`__

   ::

       from django.conf.urls import patterns, include, url
       from solid_i18n.urls import solid_i18n_patterns

       urlpatterns = solid_i18n_patterns(
           url(r'^about/$', 'about.view', name='about'),
           url(r'^news/', include(news_patterns, namespace='news')),
       )

5. Start the development server and visit http://127.0.0.1:8000/about/
   to see english content. Visit http://127.0.0.1:8000/ru/about/ to see
   russian content. If ``SOLID_I18N_USE_REDIRECTS`` was set to ``True``
   and if your preferred language is equal to Russian, request to path
   http://127.0.0.1:8000/about/ will be redirected to
   http://127.0.0.1:8000/ru/about/. But if preferred language is
   English, http://127.0.0.1:8000/about/ will be shown.

Settings
--------

-  | ``SOLID_I18N_USE_REDIRECTS = False``
   | If ``True``, redirect to url with non-default language prefix from
     url without prefix, if user's language is not equal to default.
     Otherwise url without language prefix will always render default
     language content (see `behaviour section <#behaviour>`__ and
     `notes <#notes>`__ for details).

-  | ``SOLID_I18N_HANDLE_DEFAULT_PREFIX = False``
   | If ``True``, both urls ``/...`` and ``/en/...`` will render default
     language content (in this example 'en' is default language).
     Otherwise, ``/en/...`` will return 404 status\_code.

-  | ``SOLID_I18N_DEFAULT_PREFIX_REDIRECT = False``
   | If ``True``, redirect from url with default language prefix to url
     without any prefix, i.e. redirect from ``/en/...`` to ``/...`` if
     'en' is default language.

-  | ``SOLID_I18N_PREFIX_STRICT = False``
   | Experimental. If ``True``, paths like ``/my-slug/`` will call your
     view on that path, if language my-slug doesn't exists (here ``my``
     is supported language).

   Example.

   ::

       # settings.py
       LANGUAGES = (
           ('en', 'English'),
           ('my', 'Burmese'),
       )

       # urls.py
       urlpatterns = solid_i18n_patterns('',
           url(r'^my-slug/$', some_view),
       )

   If ``SOLID_I18N_PREFIX_STRICT=False``, then url /my-slug/ will
   respond with 404, since language ``my-slug`` is not found. This
   happens, because we have a registered language tag ``my``. Language
   tag can have form like this:

   ::

       language-region

   So django in this case tries to find language 'my-slug'. But it fails
   and that is why django respond 404. And your view ``some_view`` will
   not be called.

   But, if we set ``SOLID_I18N_PREFIX_STRICT=True``, then resolve system
   will get language only from exact 'my' prefix. In case of /my-slug/
   url the prefix is not exact, and our ``some_view`` will be found and
   called.

Example site
------------

Located
`here <https://github.com/st4lk/django-solid-i18n-urls/tree/master/example>`__,
it is ready to use, just install solid\_i18n (this package):

::

    pip install solid_i18n

clone example site:

::

    git clone https://github.com/st4lk/django-solid-i18n-urls.git

step in example/ and run development server:

::

    cd django-solid-i18n-urls/example
    python manage.py runserver

Notes
-----

-  When using ``SOLID_I18N_USE_REDIRECTS = True``, there is some nasty
   case. Suppose django has determined user preferred language
   incorrectly (maybe in user's browser preferred language is not equal
   to his realy preferred language, because for example it is not his
   computer) and it is Russian. Then on access to url without prefix,
   i.e. ``'/'``, he will be redirected to ``'/ru/'`` (according to
   browsers preferred language). He wants to look english content (that
   is default language), but he can't, because he is always being
   redirected to ``'/ru/'`` from ``'/'``. To avoid this, it is needed to
   set preferred language in his cookies (just
   ``<a href="{{ specific language url}}">`` will not work). For that
   purporse django's `set\_language redirect
   view <https://docs.djangoproject.com/en/dev/topics/i18n/translation/#the-set-language-redirect-view>`__
   shall be used. See example in this package.

-  Of course, you must specify translation for all languages you've
   marked as supported. For details look here:
   https://docs.djangoproject.com/en/dev/topics/i18n/translation/.

-  Don't mix together settings ``SOLID_I18N_HANDLE_DEFAULT_PREFIX`` and
   ``SOLID_I18N_DEFAULT_PREFIX_REDIRECT``. You should choose only one of
   them.

.. |Build Status| image:: https://travis-ci.org/st4lk/django-solid-i18n-urls.svg?branch=master
   :target: https://travis-ci.org/st4lk/django-solid-i18n-urls
.. |Coverage Status| image:: https://coveralls.io/repos/st4lk/django-solid-i18n-urls/badge.svg?branch=master
   :target: https://coveralls.io/r/st4lk/django-solid-i18n-urls?branch=master
.. |Pypi version| image:: https://img.shields.io/pypi/v/solid_i18n.svg
   :target: https://pypi.python.org/pypi/solid_i18n


solid\_i18n release notes
=========================

v1.4.1
------

-  Fix minor issue with SolidLocaleRegexURLResolver

Issues:
`#40 <https://github.com/st4lk/django-solid-i18n-urls/issues/40>`__

v1.4.0
------

-  Add django 1.10 support
-  Add deprecation notice

Issues:
`#35 <https://github.com/st4lk/django-solid-i18n-urls/issues/35>`__

v1.3.0
------

-  Add SOLID\_I18N\_PREFIX\_STRICT setting to handle urls starting with
   language code

Issues:
`#34 <https://github.com/st4lk/django-solid-i18n-urls/issues/34>`__

v1.2.0
------

-  Add django 1.9 support
-  Drop django 1.4 support
-  Drop python 3.2 support
-  Simplify tox settings

Issues:
`#32 <https://github.com/st4lk/django-solid-i18n-urls/issues/32>`__,
`#23 <https://github.com/st4lk/django-solid-i18n-urls/issues/23>`__,
`#21 <https://github.com/st4lk/django-solid-i18n-urls/issues/21>`__

v1.1.1
------

-  fix django 1.8 ``AppRegistryNotReady("Apps aren't loaded yet.")``

Issues:
`#29 <https://github.com/st4lk/django-solid-i18n-urls/issues/29>`__

v1.1.0
------

-  Use 301 redirect in case of ``SOLID_I18N_DEFAULT_PREFIX_REDIRECT``
-  Upload wheel

Issues:
`#24 <https://github.com/st4lk/django-solid-i18n-urls/issues/24>`__,
`#20 <https://github.com/st4lk/django-solid-i18n-urls/issues/20>`__

v1.0.0
------

-  Add django 1.8 support

Issues:
`#8 <https://github.com/st4lk/django-solid-i18n-urls/issues/8>`__,
`#19 <https://github.com/st4lk/django-solid-i18n-urls/issues/19>`__

v0.9.1
------

-  fix working with
   `set\_language <https://docs.djangoproject.com/en/dev/topics/i18n/translation/#set-language-redirect-view>`__
   and ``SOLID_I18N_HANDLE_DEFAULT_PREFIX = True``

Issues:
`#17 <https://github.com/st4lk/django-solid-i18n-urls/issues/17>`__

v0.8.1
------

-  fix url reverse in case of
   ``SOLID_I18N_HANDLE_DEFAULT_PREFIX = True``
-  simplify django version checking

Issues:
`#13 <https://github.com/st4lk/django-solid-i18n-urls/issues/13>`__,
`#14 <https://github.com/st4lk/django-solid-i18n-urls/issues/14>`__

v0.7.1
------

-  add settings ``SOLID_I18N_HANDLE_DEFAULT_PREFIX`` and
   ``SOLID_I18N_DEFAULT_PREFIX_REDIRECT``

Issues:
`#12 <https://github.com/st4lk/django-solid-i18n-urls/issues/12>`__

v0.6.1
------

-  handle urls with default language prefix explicitly set

Issues:
`#10 <https://github.com/st4lk/django-solid-i18n-urls/issues/10>`__

v0.5.1
------

-  add django 1.7 support
-  add python 3.4 support

Issues:
`#6 <https://github.com/st4lk/django-solid-i18n-urls/issues/6>`__

v0.4.3
------

-  fix http header 'Vary Accept-Language'

Issues:
`#4 <https://github.com/st4lk/django-solid-i18n-urls/issues/4>`__

v0.4.2
------

-  stop downgrading Django from 1.6.x to 1.6
-  include requirements.txt in distribution
-  minor docs updates

Issues:
`#3 <https://github.com/st4lk/django-solid-i18n-urls/issues/3>`__

v0.4.1
------

Add python 3.2, 3.3 support.

Issues:
`#2 <https://github.com/st4lk/django-solid-i18n-urls/issues/2>`__

v0.3.1
------

Add django 1.6 support

v0.2.1
------

Update README and data for pypi

v0.2
----

First version in pypi


