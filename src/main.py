from src.parser import Parser


def main() -> None:
    m = Parser().parse("maps/easy/01_linear_path.txt")
    print(m)
