# SeedingTime

## Configuration

## Logic

* When the number of players is between min_players and full_players, a server is considered to be seeding. 
* When no server is seeding, and the own server is not above seeded_players, it's seeding time. 
* Servers are considered, when the name matches and no exclude matches the name. 

## Direct messages

* Send the message "seeding" to the bot by direct message to get an update on seeding as response

## Background task

* Servers statistics are polled regularly.
* If the own server is above seeded_players or it's before seeding_
