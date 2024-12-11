import argparse
import os
import sqlite3
import sys
import time

DB_PATH = os.getenv("DB_PATH", "PhoneFactor")
CANOKEY_PIN = os.getenv("CANOKEY_PIN", "123456")


def read_from_db() -> list:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT name, username, oath_secret_key FROM accounts")
    res = c.fetchall()
    conn.close()
    return res


def read_from_errorfile() -> list:
    res = []
    with open("./error_list.txt", "r", encoding="utf-8") as file:
        for line in file:
            elements = line.strip().split()
            if len(elements) == 3:
                res.append(tuple(elements))
    return res


def write_to_canokey(_name: str, _username: str, _oath_secret_key: str) -> bool:
    _name = _name.replace(" ", "")
    _username = _username.replace(" ", "")
    res = os.system(f"ckman oath accounts add -p {CANOKEY_PIN} -i {_name} {_username} {_oath_secret_key}")
    if res != 0:
        err_list.append((_name, _username, _oath_secret_key))
        if input("Continue to import next? (y/n) ").lower() != "y":
            print("Exiting...")
            return False
    return True


if __name__ == '__main__':
    # Change working directory to script directory
    os.chdir(sys.path[0])
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", '--retry-error', action='store_true', help='retry from error list file.')
    args = parser.parse_args()
    # Read data
    data = read_from_errorfile() if args.retry_error else read_from_db()
    # Write data to canokey
    err_list = []
    for row in data:
        print(f"Writing {row[0]} {row[1]}...")
        if write_to_canokey(row[0], row[1], row[2]):
            time.sleep(3)
        else:
            break
    # Write error list to file
    if err_list:
        with open("error_list.txt", "w", encoding="utf-8") as f:
            f.write("\n".join([f"{x[0]} {x[1]} {x[2]}" for x in err_list]))
        print("\nError(maybe) list written to error_list.txt")
    # Done
    print("Done!")
