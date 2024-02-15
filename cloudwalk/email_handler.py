from email import message
import aiosmtplib
from sqlalchemy import text

from cloudwalk.db.engine import get_session
from cloudwalk.settings import Settings


class SmtpHandler:
    def __init__(self, settings: Settings):
        self.smpt_url = settings.SMTP_URL
        self.smpt_port = 465
        self.smpt_user = settings.EMAIL_SENDER
        self.smpt_password = settings.EMAIL_PASSWORD

    async def sendmail(self, body: str, subject: str, email_receiver: list):
        em = message.EmailMessage()
        em['From'] = self.smpt_user
        em['Subject'] = subject
        em.set_content(body)
        smtp = aiosmtplib.SMTP(
            hostname=self.smpt_url, port=self.smpt_port, use_tls=True
        )

        await smtp.connect()
        await smtp.login(self.smpt_user, self.smpt_password)
        await smtp.sendmail(self.smpt_user, email_receiver, em.as_string())
        await smtp.quit()


class SendMail:
    def __init__(self, smtp: SmtpHandler):
        self.smtp = smtp

    def get_users(self):
        session = get_session()
        sql = text(
            """
            SELECT DISTINCT user_id
            FROM loans
            WHERE 		status = 'ongoing'
                AND 	extract(day from (CURRENT_DATE - created_at))%30 = 0
        """
        )
        results = [
            str(item[0]) + '@cloudwalk.com' for item in session.execute(sql)
        ]
        return results[:10]

    async def run(self):
        users = self.get_users()
        subject = 'Lembrete de Pagamento de Empréstimo'
        body = """
        Caro Cliente,
        Esperamos que este email o encontre bem.
        Gostaríamos de lembrar a todos os nossos valiosos clientes que é fundamental manter-se em dia com os pagamentos de empréstimos. Entendemos que a gestão financeira pode ser desafiadora, e estamos aqui para ajudar a tornar o processo o mais simples possível.
        Por favor, verifique a data de vencimento do seu empréstimo e assegure-se de que o pagamento seja efetuado até essa data. Manter-se em dia com os pagamentos é essencial para evitar quaisquer encargos adicionais ou penalidades.
        Se você já efetuou o pagamento, agradecemos sinceramente sua cooperação. Caso contrário, pedimos que tome as medidas necessárias para garantir que o pagamento seja realizado a tempo.
        Lembre-se de que estamos aqui para ajudar. Se precisar de qualquer assistência adicional ou tiver alguma dúvida sobre o seu empréstimo, não hesite em nos contatar. Estamos disponíveis para ajudá-lo da melhor forma possível.
        Agradecemos pela sua atenção e cooperação contínuas.
        """
        await self.smtp.sendmail(body, subject, users)
