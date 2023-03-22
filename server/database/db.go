package BookingSystemDB

import (

    "database/sql"
    "log"
    "os"
    "github.com/go-sql-driver/mysql"

)

func test() {

    db, err := sql.Open("mysql", os.Getenv("DSN"))

    if err != nil {

        log.Fatalf("failed to connect: %v", err)

    }

    defer db.Close()

    if err := db.Ping(); err != nil {

        log.Fatalf("failed to ping: %v", err)

    }

    log.Println("Successfully connected to PlanetScale!")

}
