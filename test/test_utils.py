import pytest

from main import safe_database_url, _mask_db_url


def test_safe_database_url_encodes_non_ascii():
    src = "postgresql+psycopg2://usér:päss@localhost:5432/mydb"
    out = safe_database_url(src)
    assert "%C3%A9" in out and "%C3%A4" in out


def test_safe_database_url_returns_same_on_invalid():
    src = "not-a-dsn"
    out = safe_database_url(src)
    assert out == src


def test_mask_db_url_valid():
    src = "postgresql+psycopg2://user:pass@host:123/db"
    masked = _mask_db_url(src)
    assert masked.startswith("postgresql+psycopg2://user:***@host:123/db")


def test_mask_db_url_invalid():
    src = "::not-a-dsn::"
    masked = _mask_db_url(src)
    assert masked == "(invalid-dsn)"


def test_on_startup_runs(client):
    # calling on_startup should create tables without error
    from main import on_startup

    on_startup()


def test_engine_unicode_error(monkeypatch):
    import runpy
    import sqlalchemy

    def raise_unicode(*a, **k):
        raise UnicodeDecodeError('utf-8', b'\xe7', 0, 1, 'invalid')

    monkeypatch.setattr(sqlalchemy, 'create_engine', raise_unicode)

    try:
        with pytest.raises(UnicodeDecodeError):
            runpy.run_path('main.py', run_name='__main__')
    finally:
        # no cleanup required
        pass
