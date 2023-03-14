up_local:
		uvicorn app.main:app --reload

up:
		docker-compose -f ./environment/dev/docker-compose.yaml up --build

stop:
		docker-compose -f ./environment/dev/docker-compose.yaml stop

down:
		docker-compose -f ./environment/dev/docker-compose.yaml down

test_down:
		docker-compose -f ./environment/test/docker-compose.yaml down

test: test_down
		docker-compose -f ./environment/test/docker-compose.yaml build
		docker-compose -f ./environment/test/docker-compose.yaml run -e POSTGRES_DB=tests app pytest tests
		docker-compose -f ./environment/test/docker-compose.yaml down

test_module: down
		docker-compose -f ./environment/test/docker-compose.yaml build
		docker-compose -f ./environment/test/docker-compose.yaml run -e POSTGRES_DB=tests app pytest $(MODULE) -vv
		docker-compose -f ./environment/test/docker-compose.yaml down

bandit:
	bandit -r ./app
