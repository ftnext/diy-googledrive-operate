import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source_id")
    args = parser.parse_args()
    print(args.source_id)


if __name__ == "__main__":
    main()
