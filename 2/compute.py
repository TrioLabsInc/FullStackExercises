import random
import threading

def worker(done_event: threading.Event) -> None:
    for _ in range(5000):
        100 // random.choice((0, 1, 2, 5))
    done_event.set()


def main() -> None:
    done_event = threading.Event()
    thread = threading.Thread(target=worker, args=(done_event,))
    thread.start()

    print("waiting for worker to finish")
    done_event.wait()
    thread.join()
    print("worker finished")


if __name__ == "__main__":
    main()
