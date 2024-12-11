dcam: # apply alembic migrations
	docker-compose exec app alembic upgrade head