import pytest
import sys

def run_all_tests():
    sys.exit(pytest.main([], plugins=[]))

if __name__ == "__main__":
    run_all_tests()