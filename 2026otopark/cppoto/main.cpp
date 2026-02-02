#include <iostream>
#include <string>
#include <vector>
#include <sqlite3.h>
#include "crow.h"  // Crow web framework

// Simple User struct
struct User {
    int kod;
    std::string plaka;
    std::string name;
    std::string surname;
    std::string tel;
    std::string eposta;
    std::string arac_marka;
    std::string durum;
    std::string passw;
};

// Database functions
sqlite3* db;

void init_db() {
    sqlite3_open("otopark.db", &db);
    const char* create_user = "CREATE TABLE IF NOT EXISTS user (kod INTEGER PRIMARY KEY AUTOINCREMENT, plaka TEXT UNIQUE, name TEXT, surname TEXT, tel TEXT, eposta TEXT, arac_marka TEXT, durum TEXT, passw TEXT);";
    const char* create_rights = "CREATE TABLE IF NOT EXISTS rights (kod INTEGER PRIMARY KEY AUTOINCREMENT, plaka TEXT, start_date TEXT, finish_date TEXT, durum TEXT, odeme REAL, gunluk_fiat REAL, FOREIGN KEY (plaka) REFERENCES user (plaka));";
    const char* create_password = "CREATE TABLE IF NOT EXISTS password (kod INTEGER PRIMARY KEY AUTOINCREMENT, passw TEXT);";
    sqlite3_exec(db, create_user, nullptr, nullptr, nullptr);
    sqlite3_exec(db, create_rights, nullptr, nullptr, nullptr);
    sqlite3_exec(db, create_password, nullptr, nullptr, nullptr);
    // Insert default admin password
    sqlite3_exec(db, "INSERT OR IGNORE INTO password (kod, passw) VALUES (1, 'admin123');", nullptr, nullptr, nullptr);
}

std::vector<User> get_users() {
    std::vector<User> users;
    sqlite3_stmt* stmt;
    sqlite3_prepare_v2(db, "SELECT * FROM user;", -1, &stmt, nullptr);
    while (sqlite3_step(stmt) == SQLITE_ROW) {
        User u;
        u.kod = sqlite3_column_int(stmt, 0);
        u.plaka = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 1));
        u.name = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 2));
        u.surname = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 3));
        u.tel = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 4));
        u.eposta = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 5));
        u.arac_marka = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 6));
        u.durum = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 7));
        u.passw = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 8));
        users.push_back(u);
    }
    sqlite3_finalize(stmt);
    return users;
}

int main() {
    init_db();

    crow::SimpleApp app;

    CROW_ROUTE(app, "/")([](){
        std::string html = "<h1>Akıllı Otopark</h1><a href='/users'>Kullanıcılar</a>";
        return html;
    });

    CROW_ROUTE(app, "/users")([](){
        auto users = get_users();
        std::string html = "<h1>Kullanıcılar</h1><ul>";
        for (const auto& u : users) {
            html += "<li>" + u.name + " " + u.surname + " - " + u.plaka + "</li>";
        }
        html += "</ul>";
        return html;
    });

    app.port(8080).multithreaded().run();

    sqlite3_close(db);
    return 0;
}