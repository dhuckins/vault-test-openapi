import schemathesis

schema = schemathesis.from_pytest_fixture("vault_openapi_schema")


@schema.parametrize()
def test_all(case: schemathesis.Case, vault_container):
    case.call_and_validate()
