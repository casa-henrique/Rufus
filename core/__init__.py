import datetime

class SystemInfo:
    def __init__(self):
        pass
    
    @staticmethod
    def get_time():
        now = datetime.datetime.now()
        answer = 'É exatamente {} horas e {} minutos.'.format(now.hour, now.minute)
        return answer

    @staticmethod
    def get_date():
        now = datetime.datetime.now()
        answer = 'Estamos no dia {} do mês {}.'.format(now.day, now.month)
        return answer

    @staticmethod
    def get_congratulations():
        answer = 'Eu que agradeço!'
        return answer
        