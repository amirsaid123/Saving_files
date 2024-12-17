class CustomConfigParser:

    def __init__(self):
        self._config = {}

    def read(self, filepath):
        self._config.clear()
        try:
            with open(filepath, 'r') as file:
                for line in file:
                    line = line.strip()
                    if not line:
                        continue
                    if line.startswith('[') and line.endswith(']'):
                        current_section = line[1:-1]
                        self._config[current_section] = {}
                    elif '=' in line:
                        if current_section is None:
                            raise ValueError(f"Invalid line in config file: {line}")
                        key, value = map(str.strip, line.split('=', 1))
                        self._config[current_section][key] = value
                    else:
                        raise ValueError(f"Invalid line in config file: {line}")
        except FileNotFoundError:
            raise FileNotFoundError(f"File {filepath} not found")
        print(self._config)

    def get(self, section, key):
        try:
            return self._config[section][key]
        except KeyError:
            raise KeyError('секция или ключ отсутствуют')

    def set(self, section, key, value):
        if section not in self._config:
            self._config[section] = {}
        self._config[section][key] = value
        print(self._config)


    def add_section(self, section):
        self._config[section] = {}
        print(self._config)

    def remove_section(self, section):
        try:
            del self._config[section]
        except KeyError:
            raise KeyError('секция отсутствует')
        print(self._config)

    def remove_option(self, section, key):
        try:
            del self._config[section][key]
        except KeyError:
            raise KeyError('секция или ключ отсутствуют')
        print(self._config)

    def write(self, filepath):
        with open(filepath, 'w') as file:
            for section, options in self._config.items():
                file.write(f"[{section}]\n")
                file.writelines(f"{key} = {value}\n" for key, value in options.items())
                file.write("\n")
        print(self._config)

if __name__ == "__main__":
    config = CustomConfigParser()


config.read("config_example.configus")
config.remove_section("database")
config.write("config_example.configus")
