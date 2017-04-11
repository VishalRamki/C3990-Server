## import rethinkdb
import rethinkdb as r

## fixed values;
dbName = "beaconrebuild" # @TODO PLEASE CHANGE BACK TO "beaconrebuild"

## connect to localhost;
r.connect("localhost", 28015).repl()

## create database;
response = r.db_create(dbName).run()
## print db response
print(response)
print("Database created.")
## create tables;
r.db(dbName).table_create("beacon").run()
r.db(dbName).table_create("beacon_orders").run()
r.db(dbName).table_create("promotionalmaterials").run()
r.db(dbName).table_create("store").run()
r.db(dbName).table_create("store_promotion").run()
r.db(dbName).table_create("user").run()
r.db(dbName).table_create("user_favouritestore").run()
r.db(dbName).table_create("user_interactbeacon").run()
print("Tables created")

## create secondary indexes.
## create secondary indexes on beacon;
r.db(dbName).table("beacon").index_create("beacon_id").run()
r.db(dbName).table("beacon").index_create("owner").run()
print("Secondary Indexes on `beacon` created.")
## create secondary indexes on store;
r.db(dbName).table("store").index_create("beacon_id").run()
r.db(dbName).table("store").index_create("store_id").run()
r.db(dbName).table("store").index_create("store_manager_id").run()
print("Secondary Indexes on `store` created.")
## create secondary indexes on store_promotion;
r.db(dbName).table("store_promotion").index_create("beacon_id").run()
r.db(dbName).table("store_promotion").index_create("store_id").run()
print("Secondary Indexes on `store_promotion` created")
## create secondary indexes on user;
r.db(dbName).table("user").index_create("google_oauth_token").run()
r.db(dbName).table("user").index_create("user_id").run()
print("Secondary Indexes on `user` created.")
## create secondary indexes on user_favouritestore;
r.db(dbName).table("user_favouritestore").index_create("user_id").run()
print("Secondary Indexes on `user_favouritestore` created.")
## create secondary indexes on user_interactbeacon
r.db(dbName).table("user_interactbeacon").index_create("user_id").run()
print("Secondary Indexes on `user_interactbeacon` created.")


## Tell The user hi!
print("RethinkDB has been setup with the appropriate Database. The tables has been inserted and the secondary indexes are active.")
