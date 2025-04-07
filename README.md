To run, use
```sh
docker compose up
```

<hr>

If any changes are made to the database schema, run
```sh
docker compose exec backend alembic revision --autogenerate -m "your message here"
```

And then run the migration
```sh
docker compose exec backend alembic upgrade head
```

<hr>

Run tests with 
```sh
docker compose run --rm backend pytest
```