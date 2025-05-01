resource "snowflake_database" "data_ops" {
  name = var.database_name
}

resource "snowflake_schema" "bronze" {
  name     = "BRONZE"
  database = snowflake_database.data_ops.name
}

resource "snowflake_schema" "silver" {
  name     = "SILVER"
  database = snowflake_database.data_ops.name
}

resource "snowflake_schema" "gold" {
  name     = "GOLD"
  database = snowflake_database.data_ops.name
}
