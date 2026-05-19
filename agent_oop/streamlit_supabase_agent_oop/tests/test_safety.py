from core.safety import SQLSafetyGuard


def test_select_is_allowed():
    guard = SQLSafetyGuard()
    result = guard.validate("select * from gold.fact_inventory")
    assert result.is_safe


def test_delete_is_blocked():
    guard = SQLSafetyGuard()
    result = guard.validate("delete from gold.fact_inventory")
    assert not result.is_safe
