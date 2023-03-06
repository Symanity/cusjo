import os
database_path = "databases"
csv_folder_name = "window_magic_data"

csv_location = os.path.join(database_path, csv_folder_name)

# Service object positions
Customer_Id     = 0
Service_Date    = 1
Service_Type    = 2
Service_Price   = 3
Employee        = 4
Service_Duration = 5
# Invoice = 6
Service_Frequency = 7