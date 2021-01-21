#!/usr/bin/python3.7
import argparse
from abc import abstractmethod, ABC
import requests
import sys
import json


KV_URL = "http://localhost:8080"


def api_request(url, method="get", body={}, params={}, headers= {}):
    if method == "get":
        try:
            resp = requests.get(url, params=params,headers=headers)
        except:
            print("Unable to contact server")
            sys.exit(1)

        if resp.status_code in [200, 204]:
            try:
                return resp.json()
            except:
                print("Unable to prase the data from server")
                sys.exit(1)
        elif resp.status_code == 404:
            print("The provided key doesn't exist in server")
            sys.exit(1)
        elif resp.status_code == 405:
            print("Un-allowed method used")
            sys.exit(1)
        else:
            print(f"Received {resp.status_code} with response: {resp.text}")
            sys.exit(1)

    elif method == "post":
        try:
            print(body)
            print(headers)
            print(url)
            resp = requests.post(url, json=json.dumps(body), headers=headers)
        except Exception as e:
            print(f"Unable to contact server: {e}")
            sys.exit(1)

        if resp.status_code in [200, 204]:
            try:
                return resp.json()
            except:
                print("Unable to parse the data from server")
                sys.exit(1)
        elif resp.status_code == 405:
            print("Un-allowed method used")
            sys.exit(1)
        else:
            print(f"Received {resp.status_code} with response: {resp.text}")
            sys.exit(1)
    else:
        raise Exception(f"Un-supported method: {method}")


class MainParser:
    """
    Main parser class
    """
    sub_command_classes = []

    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.subparser = self.parser.add_subparsers(dest="subcommand")

    def get_parser(self):
        return self.parser

    def get_sub_parser(self):
        return self.subparser


class SubCommand(ABC):
    """
    Interface class for sub commands. All sub commands implement this class.
    """

    @abstractmethod
    def add_sub_command(self):
        """ Method to add sub command to parser """
        pass

    @abstractmethod
    def process(self, sub_command, args):
        """ Method to handle the sub-commands """
        pass


class GetCommand(SubCommand):
    def __init__(self, main_parser):
        self.p = main_parser
        self.sub_parser = main_parser.get_sub_parser()
        self.add_sub_command()
        self.p.sub_command_classes.append(self)

    def add_sub_command(self):
        get_k = self.sub_parser.add_parser("get", help="Use get <KEY> to fetch the value of that key from kv store.")
        get_k.add_argument(
            "key",
            action="store",
            help="Key name to fetch the value"
        )

    def process(self, sub_command, args):
        if sub_command == "get":
            url = f"{KV_URL}/key/{args.key}"
            data = api_request(url)
            print(data)


class SetCommand(SubCommand):
    def __init__(self, main_parser):
        self.p = main_parser
        self.sub_parser = main_parser.get_sub_parser()
        self.add_sub_command()
        self.p.sub_command_classes.append(self)

    def add_sub_command(self):
        get_k = self.sub_parser.add_parser("set", help="Use set <KEY> <VALUE> to create/update the key with given value in kv store.")
        get_k.add_argument(
            "key",
            action="store",
            help="name for the key to set"
        )
        get_k.add_argument(
            "value",
            action="store",
            help="Value for the key to set"
        )

    def process(self, sub_command, args):
        if sub_command == "set":
            url = f"{KV_URL}/key"
            body = {
                "name" : args.key,
                "value": args.value
            }
            headers = {
                "Content-Type" : "application/json"
            }
            data = api_request(url, method="post", body=body, headers=headers)
            print("key successfully set in the server \n", data)


class WatchCommand(SubCommand):
    def __init__(self, main_parser):
        self.p = main_parser
        self.sub_parser = main_parser.get_sub_parser()
        self.add_sub_command()
        self.p.sub_command_classes.append(self)

    def add_sub_command(self):
        self.sub_parser.add_parser("watch", help="Use watch to watch updates to any keys in kv store.")

    def process(self, sub_command, args):
        if sub_command == "watch":
            pass


if __name__ == "__main__":
    p = MainParser()
    parser = p.get_parser()
    GetCommand(p)
    SetCommand(p)

    # show help if no sub commands are provided.
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    arg_data = parser.parse_known_args()[0]
    cmd = arg_data.subcommand
    for _ in p.sub_command_classes:
        _.process(cmd, arg_data)

