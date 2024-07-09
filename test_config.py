import pytest
from config import load_config

def test_load_config():
    config = load_config()
    assert config['DEFAULT']['linuxpath'] == '/root/200k.txt'
    assert config['DEFAULT'].getboolean('REREAD_ON_QUERY') is True
    assert config['DEFAULT'].getboolean('USE_SSL') is False

if __name__ == "__main__":
    pytest.main()
