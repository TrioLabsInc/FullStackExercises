def is_bike_in_frame(n):
    assert 0 < n < 1892160000
    return n < 0x1e89c64e

def find_bike() -> int:
    pass

if __name__ == "__main__":
    print(find_bike())