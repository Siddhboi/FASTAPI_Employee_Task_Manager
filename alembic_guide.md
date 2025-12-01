# 🗄️ Alembic Migration Guide - Complete Setup

## What is Alembic?

Alembic is a database migration tool that tracks changes to your database schema. Think of it as "Git for your database".

**Why use it?**
- Track database schema changes
- Upgrade/downgrade database versions
- Team collaboration on database changes
- Safe schema modifications in production

---

## 📁 Required Directory Structure

```
fastapi_task/
├── alembic/
│   ├── versions/          # Migration files go here
│   ├── env.py            # Alembic environment config
│   └── script.py.mako    # Migration template
├── alembic.ini           # Alembic configuration
├── database.py           # Your database setup
├── models.py             # Your SQLAlchemy models
└── config.py             # Your app config
```

---

## 🚀 Quick Setup (3 Steps)

### Step 1: Verify Files Exist

Check that you have all required files:
```bash
# Should exist
ls alembic/env.py
ls alembic/script.py.mako
ls alembic.ini
ls alembic/versions/
```

If `alembic/versions/` doesn't exist:
```bash
mkdir -p alembic/versions
```

### Step 2: Create Initial Migration

```bash
# This creates a migration file based on your models
alembic revision --autogenerate -m "Initial migration"
```

### Step 3: Apply Migration

```bash
# This creates the tables in your database
alembic upgrade head
```

**Done!** Your database now has all tables from your models.

---

## 📋 Common Alembic Commands

### Check Status

```bash
# Show current database version
alembic current

# Show migration history
alembic history

# Show migration history with details
alembic history --verbose
```

### Create Migrations

```bash
# Auto-generate migration from model changes
alembic revision --autogenerate -m "Add user table"

# Create empty migration (manual)
alembic revision -m "Custom migration"
```

### Apply Migrations

```bash
# Apply all pending migrations
alembic upgrade head

# Apply next migration only
alembic upgrade +1

# Upgrade to specific version
alembic upgrade abc123
```

### Rollback Migrations

```bash
# Rollback one migration
alembic downgrade -1

# Rollback to specific version
alembic downgrade abc123

# Rollback all migrations
alembic downgrade base
```

---

## 🔧 Automated Setup Script

Use the provided script for easy setup:

```bash
python setup_alembic.py
```

This will:
1. Check your Alembic structure
2. Show current status
3. Create new migration (with your message)
4. Optionally apply the migration
5. Show final status

---

## 🎯 Common Workflows

### Workflow 1: First Time Setup

```bash
# 1. Create initial migration
alembic revision --autogenerate -m "Initial schema"

# 2. Check what will be created
cat alembic/versions/*.py

# 3. Apply to database
alembic upgrade head

# 4. Verify
alembic current
```

### Workflow 2: Adding New Model

Let's say you add a new `Department` model:

```python
# models.py
class Department(Base):
    __tablename__ = "departments"
    id = Column(Integer, primary_key=True)
    name = Column(String)
```

```bash
# 1. Generate migration
alembic revision --autogenerate -m "Add department table"

# 2. Review the migration file
cat alembic/versions/*.py

# 3. Apply it
alembic upgrade head
```

### Workflow 3: Modifying Existing Model

Let's say you add a field to Employee:

```python
# models.py - Add new field
class Employee(Base):
    # ... existing fields ...
    phone = Column(String, nullable=True)  # NEW FIELD
```

```bash
# 1. Generate migration
alembic revision --autogenerate -m "Add phone to employee"

# 2. Apply it
alembic upgrade head
```

### Workflow 4: Rollback Mistake

```bash
# Oh no! The migration has issues

# 1. Rollback the last migration
alembic downgrade -1

# 2. Fix your models.py

# 3. Delete the bad migration file
rm alembic/versions/bad_migration_file.py

# 4. Create new migration
alembic revision --autogenerate -m "Fixed migration"

# 5. Apply it
alembic upgrade head
```

---

## 🐛 Troubleshooting

### Problem: "No module named 'alembic'"

**Solution:**
```bash
pip install alembic
```

### Problem: "Target database is not up to date"

**Solution:**
```bash
# Check current version
alembic current

# Apply pending migrations
alembic upgrade head
```

### Problem: "Can't locate revision identified by '...'"

**Solution:**
```bash
# Database and migration files are out of sync
# Option 1: Stamp current version
alembic stamp head

# Option 2: Reset (CAUTION: This drops data!)
# Drop all tables, then:
alembic upgrade head
```

### Problem: "ModuleNotFoundError: No module named 'models'"

**Solution:** Check `alembic/env.py` has:
```python
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from models import User, Employee, Task  # Import ALL models
```

### Problem: Alembic doesn't detect model changes

**Solutions:**

1. **Import all models in env.py**
```python
# alembic/env.py
from models import User, Employee, Task  # ALL models!
```

2. **Check target_metadata**
```python
# alembic/env.py
from database import Base
target_metadata = Base.metadata  # This line must exist!
```

3. **Try explicit migration**
```bash
# Instead of autogenerate, create manually:
alembic revision -m "Manual migration"
# Then edit the generated file
```

### Problem: "FAILED: Multiple head revisions are present"

**Solution:**
```bash
# Merge the heads
alembic merge heads -m "Merge migrations"
alembic upgrade head
```

---

## 📝 Migration File Structure

When you create a migration, Alembic creates a file like:
```
alembic/versions/2024_01_15_1234-abc123def456_initial_migration.py
```

**Contents:**
```python
"""Initial migration

Revision ID: abc123def456
Revises: 
Create Date: 2024-01-15 12:34:56.789012

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = 'abc123def456'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Commands to apply the migration
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade() -> None:
    # Commands to rollback the migration
    op.drop_table('users')
```

---

## ✅ Best Practices

1. **Always review generated migrations**
   - Alembic isn't perfect
   - Check the migration file before applying

2. **Use descriptive messages**
   ```bash
   # Good
   alembic revision --autogenerate -m "Add email verification to users"
   
   # Bad
   alembic revision --autogenerate -m "Update"
   ```

3. **Test migrations**
   ```bash
   # Test upgrade
   alembic upgrade head
   
   # Test downgrade
   alembic downgrade -1
   
   # Re-apply
   alembic upgrade head
   ```

4. **One migration per logical change**
   - Don't combine unrelated changes
   - Easier to track and rollback

5. **Never edit applied migrations**
   - If a migration is already applied (in production), create a new one
   - Don't modify existing migration files

6. **Backup before production migrations**
   ```bash
   # Always backup before running migrations in production!
   pg_dump mydb > backup.sql
   alembic upgrade head
   ```

---

## 🔄 Integration with Your App

### Option 1: Run Migrations Manually (Recommended)

```bash
# Development
alembic upgrade head
python main.py

# Production
alembic upgrade head
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Option 2: Auto-migrate on Startup (Not Recommended)

```python
# main.py
from alembic import command
from alembic.config import Config

alembic_cfg = Config("alembic.ini")
command.upgrade(alembic_cfg, "head")

# Then start app
app = FastAPI(...)
```

**Why not recommended?**
- Migrations should be deliberate
- Can cause issues in production
- Better to run migrations separately

---

## 🐳 Using with Docker

### In docker-compose.yml

Your current setup already handles this:

```yaml
api:
  command: >
    sh -c "
      echo 'Creating database tables...' &&
      python -c 'from database import Base, engine; Base.metadata.create_all(bind=engine)' &&
      ...
    "
```

**To use Alembic instead:**

```yaml
api:
  command: >
    sh -c "
      echo 'Running migrations...' &&
      alembic upgrade head &&
      echo 'Creating default users...' &&
      python create_default_users.py &&
      uvicorn main:app --host 0.0.0.0 --port 8000
    "
```

---

## 📊 Example: Complete Migration Flow

```bash
# 1. Check current status
alembic current
# Output: (no version)

# 2. Create first migration
alembic revision --autogenerate -m "Initial schema with users, employees, tasks"
# Output: Generating migration file...

# 3. Review the generated file
cat alembic/versions/2024_01_15_*.py

# 4. Apply migration
alembic upgrade head
# Output: Running upgrade -> abc123, Initial schema

# 5. Verify
alembic current
# Output: abc123 (head)

# 6. Add new feature (add phone to Employee model in code)

# 7. Generate migration for new feature
alembic revision --autogenerate -m "Add phone to employee"
# Output: Generating migration file...

# 8. Apply it
alembic upgrade head
# Output: Running upgrade abc123 -> def456, Add phone to employee

# 9. Check history
alembic history
# Output:
# abc123 -> def456 (head), Add phone to employee
# <base> -> abc123, Initial schema

# 10. If needed, rollback
alembic downgrade -1
# Output: Running downgrade def456 -> abc123

# 11. Re-apply
alembic upgrade head
```

---

## ✅ Verification Checklist

After setup, verify everything works:

- [ ] `alembic current` shows current version
- [ ] `alembic history` shows migration history
- [ ] Database tables exist (check with SQL client)
- [ ] `alembic upgrade head` works without errors
- [ ] `alembic downgrade -1` works
- [ ] `alembic upgrade head` works again
- [ ] New migrations can be created
- [ ] App starts without errors

---

## 🎓 Summary

```bash
# Essential commands you need to know:
alembic current                              # Where am I?
alembic revision --autogenerate -m "message" # Create migration
alembic upgrade head                         # Apply migrations
alembic downgrade -1                         # Undo last migration
alembic history                              # Show all migrations
```

**That's it!** You now have a fully working Alembic setup! 🎉