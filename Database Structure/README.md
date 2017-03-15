I kinda have to have this file now, because I can't remember.

# User Document

User Docuemnt will contain all the information related the user. It will not contain any other information.
It will be stored in the UserTable: each document represents a User

```
{
  "user_id": INT,
  "google_oauth_token": STR
}
```

# User_InteractBeacon Document

User_InteractBeacon will contain all the beacons a user has passed by and interacted with. Each document will be a different user.

```
{
  "user_id": INT,
  "interacted": [
    {
      "store_id": INT,
      "beacon_id": INT
    }
  ]
}
```

# Store Document
Each Document will represent a different store.

```
{
  "store_id": STR,
  "store_manager_id": STR,
  "beacons": [
    {
      "beacon_id": HYBRIDINTSTR
    }
  ]
}
```

# Store_Promotion Document

Each Document will contain the data about the current on-going promotion

```
{
  "promotion_id": int,
  "message": STRING,
  "title": STRING,
  "coupon": BOOLEAN,
  "present": BOOLEAN,
  "expires": DATE_TIME,
  "store_id": STR,
  "beacon_id": STR
}
```

# Beacon Document

This document will contain all the information about the beacons. Each Document will be a seperate beacon.

```
{
  "beacon_id": HYBRIDINTSTR,
  "uuid": UUID,
  "major": major,
  "minor": minor,
  "claimed": BOOLEAN,
  "owner": INT
}
```
