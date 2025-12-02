"""
Invokes django-admin when the django module is run as a script.

Example: python -m django check
"""

from apps import manager

if __name__ == "__main__":
        manager = manager.Manager()
        manager.exec()

