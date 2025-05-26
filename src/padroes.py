import re
from typing import NamedTuple


class Padroes(NamedTuple):
    """Classe para concentrar as expressões regulares
    """
    NOME_DO_ARQUIVO = re.compile(r"(\d{4})\s(\d{8})")
    BELT_SPEED = re.compile(
        r'(\d+,\d+\.\d+): Stacker Diag: Belt Speed ips; section (\d+); T1:(\d+\.\d+) T2:(\d+\.\d+)')
    BELT_SPEED_LDU = re.compile(
        r'(\d+,\d+\.\d+): Stacker Diag: Belt Speed ips; the LDU; T1:(\d+\.\d+) T2:(\d+\.\d+) T5:(\d+\.\d+) \(vertical belts\)')
    SLOWEST_SPEED = re.compile(
        r'(\d+,\d+\.\d+): Stacker Diag: Slowest Speed in section (\d+) is at Port=(\d+) and is: (\d+) mm/sec')
    TEMPERATURE = re.compile(
        r'(\d+,\d+\.\d+): Stacker Diag: Temperature Celsius; section (\d+)( with UTurn)? at Port=(\d+) is: (\d+)')
    UNABLE_DECODE = re.compile(
        r'(\d+,\d+\.\d+): Stacker Diag: Belt Speed ips; section (\d+); T1:Unable to decode! Response=A\d+ \* OK')
    UNABLE_DECODE_LDU = re.compile(
        r'(\d+,\d+\.\d+): Stacker Diag: Belt Speed ips; the LDU; T1:Unable to decode! Response=A\d+ \* OK')
