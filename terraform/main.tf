terraform {
  required_providers {
    snowflake = {
      source  = "snowflakedb/snowflake"
      version = ">= 2.0.0"
    }
  }
}

provider "snowflake" {}


module "data_platform" {
  source        = "./modules/database_and_schemas"
  database_name = "DATAOPS_DB"

  providers = {
    snowflake = snowflake
  }
}


module "warehouse" {
  source = "./modules/warehouse"
  name   = "DATAOPS_WH"
  size   = "XSMALL"

  providers = {
    snowflake = snowflake
  }
}
