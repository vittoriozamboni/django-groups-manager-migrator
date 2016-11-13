# Django groups manager migrator

This application tests compatibility between different django-groups-manager versions.

## Requirements

    - django-groups-manager and it's requirements.

## Installation

1. Install requirements (this will install the latest stable release of ``django-groups-manager``):

```bash
pip install -r requirements.txt
```

2. Create a database for django and launch migrate:

    ```bash
    python manage.py migrate
    ```

3. Launch migration tester command with ``start`` argument:

    ```bash
    python manage.py migratortester start
    ```


4. Remove the stable version:

    ```bash
    pip uninstall django-groups-manager
    ```

5. Install the latest version:

    ```bash
    pip install -e git+https://github.com/vittoriozamboni/django-groups-manager.git#egg=django_groups_manager
    ```

6. Launch migration tester command with ``validate`` argument:

    ```bash
    python manage.py migrate
    python manage.py migratortester test
    ```
