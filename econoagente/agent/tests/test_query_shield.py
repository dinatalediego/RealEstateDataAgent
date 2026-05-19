from decidecasa_agentos.security.query_shield import QueryShield


def test_select_is_allowed():
    shield = QueryShield(("gold",), max_rows=50)
    result = shield.validate("select * from gold.dim_project")
    assert result.allowed
    assert "limit 50" in result.sql.lower()


def test_delete_is_blocked():
    shield = QueryShield(("gold",), max_rows=50)
    result = shield.validate("delete from gold.dim_project")
    assert not result.allowed


def test_unauthorized_schema_is_blocked():
    shield = QueryShield(("gold",), max_rows=50)
    result = shield.validate("select * from raw.secret_table")
    assert not result.allowed
