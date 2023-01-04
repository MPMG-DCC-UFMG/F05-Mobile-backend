Generic single-database configuration.

## Create migration revision

Same commands you must run each time when you make some changes in DB Models and want to apply these changes to your DB Schema.

```bash
alembic revision -m "first migration" --autogenerate --head head
```

If you have any problems relative to package imports similar to this example:

```bash
File "alembic/env.py", line 7, in <module>
    from app.application.core.database import Base
ModuleNotFoundError: No module named 'app'
```

Install your project locally with **pip install -e .**
 
After the successful run of alembic revision in folder alembic/versions you will see a file with new migration.

## Applying migration

To apply a created migration to the database, in the same folder of ***alembic.ini*** run the command:

```bash
alembic upgrade head
```