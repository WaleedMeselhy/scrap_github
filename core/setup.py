from setuptools import find_packages, setup

setup(
    name='database_core',
    description='database schema and migrations',
    author='Waled Meselhy',
    packages=find_packages(),
    zip_safe=False,
    version='0.1',
    install_requires=[
        'schematics==2.1.0',
        'SQLAlchemy==1.2.11',
        'psycopg2==2.7.3.1',
        'alembic==1.0.0',
        'sqlalchemy-utils==0.33.3',
        # 'toolspy==0.2.30'
    ])
