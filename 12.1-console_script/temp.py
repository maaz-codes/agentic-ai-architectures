import argparse

def main():
    parser = argparse.ArgumentParser(description="Say Hello")
    parser.add_argument("--name", required=True, help="Your name")
    parser.add_argument("--number", required=False, default=42, help="Your number")

    args = parser.parse_args()
    print(f"Hello {args.name}, {args.number}")


if __name__ == "__main__":
    main()
