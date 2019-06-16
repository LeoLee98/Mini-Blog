#!/usr/bin/env python
import os
import sys

if __name__ == '__main__':
    try:
        from flask import Flask
        print("Flask has been intalled")
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Flask. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    finally:
        os.system('pip install Flask')
        os.system('pip install flask-session')  
        try:
            import mysql.connector
            print("mysql has been intalled")
        except ImportError as exc:
            raise ImportError(
                "Couldn't import mysql. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            ) from exc
        finally:
            os.system('pip install mysql-connector')
            try:
                import redis
                print("redis has been intalled")
            except ImportError as exc:
                raise ImportError(
                    "Couldn't import redis. Are you sure it's installed and "
                    "available on your PYTHONPATH environment variable? Did you "
                    "forget to activate a virtual environment?"
                ) from exc
            finally:
                os.system('pip install redis')
    os.system('pip install flask-sqlalchemy=2.1')             
                                
                

