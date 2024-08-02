import sys
import argparse
import glob
import os

from . import Client


def main():
    parser = argparse.ArgumentParser(description="simple_catalog")
    parser.add_argument("--host", help="database host", required=True)
    parser.add_argument("--user", help="database user", required=True)
    parser.add_argument("--password", help="database password", required=True)
    parser.add_argument("--database", help="database", required=True)
    parser.add_argument("--file", help="file to actions", required=True)
    parser.add_argument("--file_password", help="archive file password", required=False)
    parser.add_argument("--dir", help="dir to register", required=False)
    parser.add_argument("--salt", help="seed value used for hashing", required=False)
    parser.add_argument("--db", help="seed value used for hashing", required=False)
    parser.add_argument("--product", help="product name", required=False)
    parser.add_argument("--revision", help="revision number", required=False)
    parser.add_argument("--hash", help="repository hash", required=False)
    parser.add_argument("--add", action="store_true", help="add file to catalog")
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument(
        "--delete", action="store_true", help="delete file from catalog"
    )
    parser.add_argument(
        "--check", action="store_true", help="check if file exists in catalog"
    )
    parser.add_argument("--inspect", action="store_true", help="inspect zip file")

    try:
        args = parser.parse_args()
    except argparse.ArgumentError as e:
        print(f"Argument parsing error: {e}")
        parser.print_help()
        sys.exit(-1)

    if not args.add and not args.delete and not args.check and not args.inspect:
        parser.print_help()
        sys.exit(-1)

    if args.db:
        p = args.db.split("|")
        if len(p) < 5:
            parser.print_help()
            sys.exit(-1)
        args.host = p[0]
        args.user = p[1]
        args.password = p[2]
        args.database = p[3]
        args.salt = p[4]

    client = Client(
        args.host,
        args.user,
        args.password,
        args.database,
        args.salt,
        args.product,
        args.revision,
        args.hash,
        args.verbose,
    )

    if args.add:
        if args.file:
            client.add(args.file)

        if args.dir:
            files = glob.glob(os.path.join(args.dir, "**/*"), recursive=True)
            if len(files):
                client.add_files(files)

    elif args.delete:
        result = client.delete(args.file)
        if result is None:
            print("Entry not found")
        else:
            print(result)
    elif args.check:
        result = client.check(args.file)
        if result is None:
            print("No matching hash found")
        else:
            for entry in result:
                print(entry)
    elif args.inspect:
        client.inspect(args.file, args.file_password)


if __name__ == "__main__":
    main()
