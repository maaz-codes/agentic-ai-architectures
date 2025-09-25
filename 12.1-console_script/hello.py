import argparse

def main():
    print("Hello from console-script!")

    parser = argparse.ArgumentParser(description="Say Hello")
    parser.add_argument("--name", required=True, help="Your name")
    args = parser.parse_args()

    print(f"Hello {args.name}")


if __name__ == "__main__":
    main()
