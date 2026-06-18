MAP ?= maps/easy/01_linear_path.txt

.PHONY: install run visual menu debug clean lint lint-strict test-maps test-challenger

install:
	uv sync

run:
	uv run python -m src --visual --menu

visual:
	uv run python -m src --visual $(MAP)

menu:
	uv run python -m src --menu

debug:
	uv run python -m pdb -m src $(MAP)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .mypy_cache .pytest_cache .ruff_cache

lint:
	uv run flake8 .
	uv run mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	uv run flake8 .
	uv run mypy . --strict --ignore-missing-imports

test-maps:
	uv run python -m src maps/easy/01_linear_path.txt
	uv run python -m src maps/easy/02_simple_fork.txt
	uv run python -m src maps/easy/03_basic_capacity.txt
	uv run python -m src maps/medium/01_dead_end_trap.txt
	uv run python -m src maps/medium/02_circular_loop.txt
	uv run python -m src maps/medium/03_priority_puzzle.txt
	uv run python -m src maps/hard/01_maze_nightmare.txt
	uv run python -m src maps/hard/02_capacity_hell.txt
	uv run python -m src maps/hard/03_ultimate_challenge.txt

test-challenger:
	uv run python -m src maps/challenger/01_the_impossible_dream.txt
