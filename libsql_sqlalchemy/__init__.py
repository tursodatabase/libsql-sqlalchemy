from sqlalchemy.dialects import registry as _registry
from .aiolibsql import SQLiteDialect_aiolibsql
from .libsql import SQLiteDialect_libsql

__version__ = "0.1.0-pre"

_registry.register("sqlite.libsql", "libsql_sqlalchemy.libsql", "SQLiteDialect_libsql")
_registry.register(
    "sqlite.aiolibsql", "libsql_sqlalchemy.aiolibsql", "SQLiteDialect_aiolibsql"
)
