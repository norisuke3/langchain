from langserve import RemoteRunnable
from langchain_core.output_parsers import StrOutputParser
import time
import threading
import itertools
import sys
import argparse

HOST = 'localhost'
PORT = 8001

done = False

def getUrl() -> str:
    parser = argparse.ArgumentParser(description="Process some arguments.")
    parser.add_argument('--host', type=str, default=HOST, help='Host address')
    parser.add_argument('--port', type=int, default=PORT, help='Port number')
    parser.add_argument('path', type=str, help='File path')

    args = parser.parse_args()

    return f"http://{args.host}:{args.port}/{args.path}/"


def spinning_cursor():
    global done
    for cursor in itertools.cycle('|/-\\'):
        if done:
            break
        sys.stdout.write('\r' + cursor)
        sys.stdout.flush()
        time.sleep(0.1)


def main():
    global done
    url = getUrl()

    rr = RemoteRunnable(url)
    parser = StrOutputParser()

    chain = rr | parser

    while True:
        prompt = input("> ")
        if prompt.lower() in ["quit", "exit"]:
            print("Finished.")
            break

        # Start the spinner
        done = False
        spinner_thread = threading.Thread(target=spinning_cursor)
        spinner_thread.start()

        res = chain.invoke(
            {"input": prompt},
            config={"configurable": {"session_id": "1"}},
        )

        # Stop the spinner
        done = True
        spinner_thread.join()
        sys.stdout.write('\r')  # Clear the spinner character
        sys.stdout.flush()

        print(res)

if __name__ == "__main__":
    main()
