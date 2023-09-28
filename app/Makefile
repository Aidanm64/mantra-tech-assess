
backend:
	docker compose up --build tech_assess_backend

frontend:
	docker compose up --build tech_assess_frontend
	sleep 2
	xdg-open http://localhost:3000/

start:
	docker compose up --build -d
	sleep 2
	xdg-open http://localhost:3000/

stop:
	docker compose down

test_backend:
	docker compose up --build -d tech_assess_backend
	pytest tech_assess_backend
	docker compose down
