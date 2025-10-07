import os, binascii, errno

def generate_key(length:int=16)->str:
    rand_bytes = os.urandom(length)
    return binascii.hexlify(rand_bytes).decode('ascii')

def load_env(path:str):
    if not os.path.exists(path) or not os.path.isfile(path):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), path)
    
    with open(path, 'r') as f:
        data = {}

        for line in f.readlines():
            line = line.strip()

            if not line or line.startswith('#'):
                continue

            key, value = line.split('=', 1)
            value = value.strip().strip('\"\'')
            data[key] = value
        return data


def create_default_env(env_path):
    # Default environment variables for the application
    default_env = [
        "FLASK_ENV=development",
        "FLASK_APP=app.py",
        "DATABASE_URL=sqlite:///database.db",
        "SECRET_KEY=your_secret_key",
        "DEBUG=True"
    ]

    # Write the defaults to the .env file
    with open(env_path, 'w') as f:
        f.write('\n'.join(default_env))
