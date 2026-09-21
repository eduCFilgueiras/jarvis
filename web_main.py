from src.core.env import load_env
from src.interfaces.web import ControlServer

load_env()

if __name__ == "__main__":
    ControlServer().serve()
