resource "snowflake_warehouse" "data_ops" {
  name                 = var.name
  warehouse_size       = var.size
  auto_suspend         = 60           
  auto_resume          = true
  initially_suspended  = true
 }

