
run:
	docker-compose up --build -d

test_all: run
	pytest backend
	docker-compose down
