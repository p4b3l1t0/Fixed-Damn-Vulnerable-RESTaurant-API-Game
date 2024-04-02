import subprocess


def get_disk_usage(parameters: str):
    allowed_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_/ "
    if not all(c in allowed_chars for c in parameters):
        raise ValueError("Invalid characters in parameters")
        
    command = "df -h " + parameters

    try:
        result = subprocess.run(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
        )
        usage = result.stdout.strip().decode()
    except:
        raise Exception("An unexpected error was observed")
    return usage
