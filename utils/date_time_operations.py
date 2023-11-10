from datetime import datetime, timezone, timedelta, date
import re

def today():
    timezone_offset = -3.0
    tzinfo = timezone(timedelta(hours=timezone_offset))
    data = str(datetime.now(tzinfo).strftime("%d/%m/%Y"))
    return data

def mp_today():
    timezone_offset = -3.0
    tzinfo = timezone(timedelta(hours=timezone_offset))
    # data = str(datetime.now(tzinfo).strftime("%Y-%m-%d"))
    # data = str(datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ'))
    # data = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    data = str(datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z"))
    return data

def now():
    timezone_offset = -3.0
    tzinfo = timezone(timedelta(hours=timezone_offset))
    data = str(datetime.now(tzinfo).strftime("%d/%m/%Y - %H:%M:%S"))
    return data


def delta_timestamp(delta_sec):
    """
    Calculate the expiration timestamp based on the current UTC time and the provided ttl (time-to-live).

    Args:
    - delta_sec (int): The time-to-live in seconds.

    Returns:
    - str: The expiration timestamp in UTC format.
    """
    timezone_offset = -3.0
    tzinfo = timezone(timedelta(hours=timezone_offset))
    current_utc_time = datetime.now(tzinfo)
    delta_time = current_utc_time + timedelta(seconds=delta_sec)

    # Convertendo para uma string no formato 'YYYY-MM-DD HH:MM:SS'
    return delta_time.strftime('%Y-%m-%d %H:%M:%S')


def seconds_from_now(timestamp_str):
    """
    Calculate the seconds from the current time to the provided timestamp.

    Args:
    - timestamp_str (str): The timestamp in the format 'YYYY-MM-DD HH:MM:SS'.

    Returns:
    - int: The number of seconds from the current time to the provided timestamp.
    """
    timezone_offset = -3.0
    tzinfo = timezone(timedelta(hours=timezone_offset))
    current_time = datetime.now(tzinfo)

    # Convertendo a string para um objeto datetime
    target_time = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S').replace(tzinfo=tzinfo)

    # Calculando a diferença em segundos
    delta = target_time - current_time
    return int(delta.total_seconds())


def now_simple():
    timezone_offset = -3.0
    tzinfo = timezone(timedelta(hours=timezone_offset))
    data = str(datetime.now(tzinfo).strftime("%d/%m/%Y - %H:%M"))
    return data

def hour():
    timezone_offset = -3.0
    tzinfo = timezone(timedelta(hours=timezone_offset))
    data = str(datetime.now(tzinfo).strftime("%H:%M"))
    return data

def week_day():
    dia = datetime.now().strftime("%d")
    dia = int(dia)
    mes = datetime.now().strftime("%m")
    mes = int(mes)
    ano = datetime.now().strftime("%Y")
    ano = int(ano)
    data = date(year=ano, month=mes, day=dia)
    week_day = data.isoweekday()
    return week_day

def change_day(days):
    days = int(days)
    return (datetime.now() + timedelta(days=days)).strftime('%d/%m/%Y')

def now_inprint():
    timezone_offset = -3.0
    tzinfo = timezone(timedelta(hours=timezone_offset))
    data = str(datetime.now(tzinfo).strftime("%d%m%Y-%H-%M-%S"))
    return data

def string_to_datetime(trigger_date, trigger_hour):
    """Converte string de data e hora para objeto datetime."""
    timezone_offset = -3.0
    tzinfo = timezone(timedelta(hours=timezone_offset))

    # Concatena a data e a hora
    full_string = f"{trigger_date} {trigger_hour}"

    # Converte para datetime
    dt = datetime.strptime(full_string, "%d/%m/%Y %H:%M")

    # Ajusta o timezone
    dt = dt.replace(tzinfo=tzinfo)

    return dt



def convert_to_standard_date(input_date: str) -> str or None:
    input_date = re.sub(r'\s+', ' ', input_date).strip()

    possible_formats = ['%d/%m/%Y', '%d.%m.%Y', '%d-%m-%Y', '%d/%m', '%d de %B de %Y']
    month_mapping = {
        'Jan': '01', 'Fev': '02', 'Mar': '03', 'Abr': '04', 'Mai': '05', 'Jun': '06',
        'Jul': '07', 'Ago': '08', 'Set': '09', 'Out': '10', 'Nov': '11', 'Dez': '12',
        'Janeiro': '01', 'Fevereiro': '02', 'Março': '03', 'Abril': '04', 'Maio': '05', 'Junho': '06',
        'Julho': '07', 'Agosto': '08', 'Setembro': '09', 'Outubro': '10', 'Novembro': '11', 'Dezembro': '12'
    }

    for fmt in possible_formats:
        try:
            if fmt == '%d/%m':
                input_date_with_year = f"{input_date}/{date.today().year}"
                dt = datetime.strptime(input_date_with_year, '%d/%m/%Y')
            else:
                dt = datetime.strptime(input_date, fmt)
            return dt.strftime('%d/%m/%Y')
        except ValueError:
            continue

    try:
        day, month, year = re.split(r'\sde\s', input_date)
        month_number = month_mapping.get(month, '')
        if month_number:
            dt = datetime.strptime(f"{day}/{month_number}/{year}", '%d/%m/%Y')
            return dt.strftime('%d/%m/%Y')
    except ValueError:
        pass

    try:
        day, month, year = input_date.split('/')
        month_number = month_mapping.get(month, '')
        if month_number:
            dt = datetime.strptime(f"{day}/{month_number}/{year}", '%d/%m/%Y')
            return dt.strftime('%d/%m/%Y')
    except ValueError:
        pass

    return None

def convert_date_format_ymd_to_dmy(date_str: str) -> str:
    try:
        # Divide a string de data usando o separador '-'
        yyyy, mm, dd = date_str.split('-')

        # Reorganiza e usa '/' como o novo separador
        new_date_str = f"{dd}/{mm}/{yyyy}"

        return new_date_str
    except ValueError:  # Caso a string não possa ser dividida em três partes
        return "Formato de data inválido"

if __name__ == "__main__":
    d = today()
    print(d)