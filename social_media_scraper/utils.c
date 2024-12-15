#include <sqlite3.h>
#include <stdio.h>

sqlite3 *db;

int start() {
    int rc = sqlite3_open("logs/indexedUsers.db", &db);
    if (rc) {
        fprintf(stderr, "Can't open database: %s\n", sqlite3_errmsg(db));
        return(0);
    }
    return 0;
}
void closeDB(){
    sqlite3_close(db);
}

int createTable(char* user_account) {
    // make sure user_account isnt dumb
    if (user_account == NULL || *user_account == '\0') {
        fprintf(stderr, "Invalid table name\n");
        return -1;
    }
    char create_table_sql[512];
    snprintf(create_table_sql, sizeof(create_table_sql), 
             "CREATE TABLE IF NOT EXISTS %s ("
             "id INTEGER PRIMARY KEY AUTOINCREMENT,"
             "name TEXT NOT NULL,"
             "email TEXT UNIQUE NOT NULL"
             ");",
             user_account);
    char* errMsg = NULL;
    int rc = sqlite3_exec(db, create_table_sql, 0, 0, &errMsg);
    if (rc != SQLITE_OK) {
        fprintf(stderr, "SQL error: %s\n", errMsg);
        sqlite3_free(errMsg);
        return rc;
    }
    printf("Table created successfully\n");
    return 0;
}
