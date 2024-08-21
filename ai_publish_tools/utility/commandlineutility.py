import logging
import subprocess
import sys


def subprocess_may_error(command, error_str, log_output=True, encoding="utf-8", **kwargs):
    if sys.platform == "darwin":
        import shlex
        if isinstance(command, str):
            command = shlex.split(command)

    try:
        logging.info(f"run cmd {command}")
        cp = subprocess.run(command, capture_output=log_output, encoding=encoding,
                            universal_newlines=True, **kwargs)
    except Exception as e:
        logging.exception(error_str)
        raise e
    else:
        if cp.returncode != 0:
            logging.info(error_str)
            logging.error(f"returncode {cp.returncode}")
            logging.info(f"args : {cp.args}")
            logging.info(f"stdout : {cp.stdout}")
            logging.info(f"stderr : {cp.stderr}")

            raise RuntimeError("subprocess failed")
        else:
            if log_output:
                logging.info(f"stdout : {cp.stdout}")

        return cp

































