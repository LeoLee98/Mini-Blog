pip install mysql-connector
pip install Flask


#!/usr/bin/env python
import os
import sys

if __name__ == '__main__':
    try:
        from Flask import flask
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Flask. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    finally:
        try:
            import mysql.connector
        except ImportError as exc:
            raise ImportError(
                "Couldn't import mysql. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            ) from exc
