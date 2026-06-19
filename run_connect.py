import os
import logging
import psycopg2

logging.basicConfig(level=logging.DEBUG)

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql+psycopg2://postgres:postgres@localhost:5432/produtos_db')
print('repr(DATABASE_URL)=', repr(DATABASE_URL))

# psycopg2 expects a libpq-style dsn; remove the prefix if present
if DATABASE_URL.startswith('postgresql+psycopg2://'):
    dsn = DATABASE_URL.replace('postgresql+psycopg2://', 'postgresql://', 1)
else:
    dsn = DATABASE_URL

print('repr(dsn)=', repr(dsn))
try:
    conn = psycopg2.connect(dsn)
    print('connected ok')
    conn.close()
except Exception as e:
    print('connect raised:', type(e), e)
    import traceback
    traceback.print_exc()
