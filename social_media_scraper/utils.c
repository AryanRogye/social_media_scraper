#include <sqlite3.h>    // FOR DB
#include <stdio.h>      // LOGGING
#include <dirent.h>     // DIR STUFF
#include <unistd.h>     // FOR F_OK
#include <sys/stat.h>   // MAKING FILE
#include <string.h>

sqlite3 *db;            // DB NAME
// FOR BETTER FILES
#define LOGS_FOLDER "logs/"
#define DB_FILE "indexedUsers.db"

int checkAndCreateFile(char* filePath) {
    // Try To Read the file first
    FILE *fptr = fopen(filePath, "r");
    // Check if the file is There
    if (fptr == NULL) {
        // Append the file if it doesnt exist
        fptr = fopen(filePath, "a");
        if (fptr == NULL) {
            perror("Error opening or creating the file");
            return -1;
        }
    }    
    fclose(fptr);
    return 0;
}
int checkDirectory() {
    // Create File Path To Use within the function
    char filePath[1024];
    snprintf(filePath, sizeof(filePath), "%s%s", LOGS_FOLDER, DB_FILE);
    // First we should validate if the db is even there or else we can make the file
    DIR *dirptr;
    if (access(LOGS_FOLDER, F_OK) == 0) {
        if((dirptr = opendir(LOGS_FOLDER)) != NULL) {
            // Exists and is a dir
            closedir(dirptr);
            // Check if the file exsits now
            if (checkAndCreateFile(filePath) != 0 ) {
                printf("There was Something Wrong With Creating or Viewing File Exists\n");
                return -1;
            }
            return 0;
        } else {
            // Exists but is not a dir its a file
            printf("File Exists But is Not a Dir (Dont know What to do)\n");
            return -1;
        }
    } else {
        // Does Not Exist at all
        printf("Doesnt Exist At All\n");
        // Need to make the dir in here
        if (mkdir(LOGS_FOLDER, 0777) == -1) {
            printf("SomeThing went wrong with creating the foler\n");
            return -1;
        } else {
            printf("Made the file\n");
        }
        // Now That thats done we want to make the file if it doesnt exist
        if (checkAndCreateFile(filePath) != 0 ) {
            printf("There was Something Wrong With Creating or Viewing File Exists\n");
            return -1;
        }
    }
    return 0;
}

int start() {
    // Check if the dir is there if it isnt it makes it
    int dir = checkDirectory();
    if(dir != 0) {
        return 0;
    }
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
    char people_table_sql[] =
             "CREATE TABLE IF NOT EXISTS user_instagram_account ("
             "person_id INTEGER UNIQUE NOT NULL,"
             "link TEXT UNIQUE NOT NULL,"
             ")";
    char create_table_sql[] =
             "CREATE TABLE IF NOT EXISTS links ("
             "user_instagram_account INTEGER,"
             "link_id INTEGER,"
             "link TEXT UNIQUE NOT NULL"
             ");";
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
