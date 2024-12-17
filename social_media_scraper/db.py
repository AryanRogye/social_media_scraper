import ctypes
import os

class db:
    def __init__(self) -> None:
        self.lib_path = os.path.abspath("./social_media_scraper/libc/sqlCImp.so")
        self.lib = ctypes.CDLL(self.lib_path)
        self.lib.start.restype = ctypes.c_int
        self.lib.createTable.restype = ctypes.c_int
        self.lib.createTable.argtypes = [ctypes.c_char_p]

        # Call the C functions
        if self.lib.start() == 0:  # Call `start()` from C
            print("Database started successfully")
            return
        
            # Example usage of `createTable`
            table_name = b"testing"  # Pass a byte string for the table name
            result = self.lib.createTable(table_name)
        
            if result == 0:
                print(f"Table '{table_name.decode()}' created successfully")
            else:
                print(f"Failed to create table '{table_name.decode()}'")
        
            self.lib.closeDB()  # Call `closeDB()` from C
        else:
            print("Failed to start database")
    
