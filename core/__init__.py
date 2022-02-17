import datetime

class SystemInfo:
    def __init__(self):
        pass
    
    def get_time():
        now = datetime.datetime.now()
        answer = 'É exatamente {} horas e {} minutos, senhor.'.format(now.hour, now.minute)
        return answer

    def get_day():
        now = datetime.datetime.now()
        answer = 'Estamos no dia {} do mês {} senhor'.format(now.day, now.month)
        return answer

    def get_congratulations():
        answer = 'Eu que agradeço!'
        return answer
        