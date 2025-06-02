from boofuzz import Session, Target, TCPSocketConnection
from boofuzz import FuzzLoggerText, FuzzLoggerCsv
from boofuzz import logging
import sys

# Уровень логирования для файлов: только ошибки
LOG_LEVEL = logging.ERROR

# Кастомный фильтр для логгеров (пропускает только ошибки)
class ErrorOnlyFilter(logging.Filter):
    def filter(self, record):
        return record.levelno >= LOG_LEVEL

def log_server_response(target, fuzz_data_logger, session, *args, **kwargs):
    try:
        response = target.recv(4096)
        if response:
            fuzz_data_logger.log_check(f"Server response: {response}")
    except Exception as e:
        fuzz_data_logger.log_check(f"Error reading response: {e}")

def main():
    # Создаем соединение
    connection = TCPSocketConnection("127.0.0.1", 8080)

    # Цель
    target = Target(connection=connection)

    # Файловые логгеры с фильтром ошибок
    txt_file = open("fuzz_log.txt", "w")
    csv_file = open("fuzz_log.csv", "w")

    txt_logger = FuzzLoggerText(file_handle=txt_file)
    csv_logger = FuzzLoggerCsv(file_handle=csv_file)

    # Применяем фильтр ошибок к файловым логгерам
    for handler in txt_logger.handlers:
        handler.addFilter(ErrorOnlyFilter())

    for handler in csv_logger.handlers:
        handler.addFilter(ErrorOnlyFilter())

    # Сессия: веб-интерфейс показывает всё, файлы — только ошибки
    session = Session(
        target=target,
        post_test_case_callbacks=[log_server_response],
        fuzz_loggers=[txt_logger, csv_logger],
        web_port=26000,
        log_level=logging.INFO  # Веб-интерфейс: все события
    )
    s_initialize("http_request")
    with s_block("request_line"):
        s_group("method", ["GET", "POST", "PUT", "DELETE", "HEAD", "PATCH", "OPTIONS"])
        s_delim(" ")
        s_string("/")
        s_delim(" ")
        s_string("HTTP/1.1")
        s_static("\r\n")

    # Тестирование различных заголовков
    with s_block("headers"):
        # Host header
        s_static("Host: ")
        s_string("localhost")
        s_static("\r\n")

        # User-Agent
        s_static("User-Agent: ")
        s_group("user_agent", [
            "Boofuzz",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
            "curl/7.68.0"
        ])
        s_static("\r\n")

        # Content-Type
        s_static("Content-Type: ")
        s_group("content_type", [
            "application/x-www-form-urlencoded",
            "multipart/form-data",
            "application/json",
            "text/xml",
            "application/javascript"
        ])
        s_static("\r\n")

        # Authorization
        s_static("Authorization: ")
        s_group("auth_type", ["Basic ", "Bearer "])
        with s_block("auth_value"):
            s_string("test")
            s_string("admin:password")
            s_string("!@#$%^&*()")
            s_string("A" * 1000)  # Длинное значение
        s_static("\r\n")

        # Accept
        s_static("Accept: ")
        s_string("*/*")
        s_string(", ")
        s_string("text/html,application/xhtml+xml")
        s_static("\r\n")

        # Connection
        s_static("Connection: ")
        s_group("connection", ["keep-alive", "close", "upgrade"])
        s_static("\r\n")

        # Special characters in header
        s_static("X-Special-Chars: ")
        s_string("!\"#$%&'()*+,-./:;<=>?@[$$^_`{|}~")
        s_static("\r\n")

    # Тестирование Content-Length
    s_static("Content-Length: ")
    s_size("body", output_format="ascii", inclusive=False)
    s_static("\r\n\r\n")

    # Тестирование multipart/form-data
    with s_block("multipart_form_data"):
        s_static("--BOUNDARY\r\n")
        s_static("Content-Disposition: form-data; name=\"file\"; filename=\"test.txt\"\r\n")
        s_static("Content-Type: text/plain\r\n\r\n")
        s_string("This is a test file content")
        s_static("\r\n--BOUNDARY--\r\n")

    # Тестирование длинных значений
    with s_block("long_values"):
        s_static("\r\n--LONG-VALUES--\r\n")
        s_string("A" * 10000)  # 10,000 A's
        s_string("\r\n")
        s_string("B" * 100000)  # 100,000 B's
        s_static("\r\n")

    # Тестирование специальных символов
    with s_block("special_chars"):
        s_static("\r\n--SPECIAL-CHARS--\r\n")
        s_string("!\"#$%&'()*+,-./:;<=>?@[$$^_`{|}~")
        s_string("àáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿ")
        s_string("АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ")
        s_string("%00%00%00%00")  # Null bytes
        s_string("\x00\x01\x02\x03\x04\x05")  # Binary data
        s_static("\r\n")

    # Основное тело запроса
    with s_block("body"):
        s_string("test")
        s_string("key=value&key2=value2")
        s_string("{\"json\": \"test\"}")
        s_string("<xml><test>data</test></xml>")

    session.connect(s_get("http_request"))
    
    try:
        session.fuzz()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)  # Настройка логирования
    main()
ebar3 compile
erl -pa _build/default/lib/*/ebin
cover:start().
cover:compile_beam_directory("_build/default/lib/cowboy/ebin").
cover:compile_beam_directory("_build/default/lib/cowlib/ebin").
cover:compile_beam_directory("_build/default/lib/ranch/ebin").
application:start(crypto).
application:start(cowlib).
application:start(asn1).
application:start(public_key).
application:start(ssl).
application:start(ranch).
application:start(cowboy).
application:start(fuzz_cowboy).
cover:analyse_to_file({application, fuzz_cowboy}, "fuzz_cowboy_coverage.html").
