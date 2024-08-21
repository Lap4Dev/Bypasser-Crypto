import base64
from urllib import parse

from src.config import settings


class Security:
    def __init__(self, secret_key: str):
        self.__secret_key = secret_key

    @staticmethod
    def _generate_key(string, key):
        key_arr = []
        for i in range(len(string)):
            key_arr.append(ord(key[i % len(key)]) % len(string))
        return key_arr

    def _un_shuffle_string(self, string):
        key_arr = self._generate_key(string, self.__secret_key)
        arr = list(string)
        for i in range(len(arr) - 1, -1, -1):
            j = (i + key_arr[i]) % len(arr)
            arr[i], arr[j] = arr[j], arr[i]
        return ''.join(arr)

    def _shuffle_string(self, string):
        key_arr = self._generate_key(string, self.__secret_key)
        arr = list(string)
        for i in range(len(arr)):
            j = (i + key_arr[i]) % len(arr)
            arr[i], arr[j] = arr[j], arr[i]
        return ''.join(arr)

    def encode_string(self, string: str) -> str:
        shuffled = self._shuffle_string(string)
        base64_encoded = base64.b64encode(shuffled.encode('utf-8')).decode('utf-8')
        return base64_encoded

    def decode_string(self, encoded_str: str) -> str:
        try:
            base64_decoded = base64.b64decode(encoded_str).decode('utf-8')
            original = self._un_shuffle_string(base64_decoded)
            # return parse.unquote(original)
            return original
        except:
            return ''


# sec = Security(settings.SECRET_ENCODE_KEY)
# encoded = sec.encode_string('user=%7B%22id%22%3A761299691%2C%22first_name%22%3A%22Sasha%22%2C%22last_name%22%3A%22%22%2C%22username%22%3A%22san4o_prog%22%2C%22language_code%22%3A%22ru%22%2C%22allows_write_to_pm%22%3Atrue%7D&chat_instance=9099920266820416594&chat_type=private&start_param=kentId761299691&auth_date=1724099954&hash=7dd32c013ade1d6fa21b086561b41f9e476e1e7133cc11c4c11a299a580e08b2')
# decoded = sec.decode_string(encoded)
#
# print(f'{encoded=}')
# print(f'{decoded=}')
