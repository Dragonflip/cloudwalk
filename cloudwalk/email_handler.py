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


class OnGoingLoansEmail:
    def __init__(self, smtp: SmtpHandler):
        self.smtp = smtp

    def _get_users(self):
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
        users = self._get_users()
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


class SummarizingOperationMail:
    def __init__(self, smtp: SmtpHandler):
        self.smtp = smtp

    def get_data(self):
        session = get_session()
        sql = text(
        """
        WITH default_rate_year as ( 
        SELECT  extract(month from created_at),
                extract(year from created_at),
                SUM(CASE WHEN status='default' THEN loan_amount ELSE 0 END)/SUM(loan_amount) as default_rate
        FROM loans
        WHERE created_at::date < '2023-11-01'::date
        GROUP BY extract(year from created_at), extract(month from created_at)
        ORDER BY 2,1
        ),
        default_rate_avg as (
        SELECT AVG(default_rate) default_rate_avg
        FROM default_rate_year
        )

        SELECT 
            EXTRACT(WEEK FROM l.created_at) AS week,
            EXTRACT(YEAR FROM l.created_at) AS year,
            COUNT(*) AS total_loans,
            SUM(CASE WHEN l.status = 'default' THEN 1 ELSE 0 END) AS defaulted_loans,
            SUM(CASE WHEN l.status = 'ongoing' THEN 1 ELSE 0 END) AS ongoing_loans,
            ROUND(SUM(l.due_amount)::numeric, 2) AS total_revenue,
            ROUND(SUM(l.loan_amount)::numeric, 2) AS total_loan_amount,
            ROUND(SUM(l.amount_paid - l.loan_amount)::numeric, 2) AS profit,
            ROUND(
                (
                    SUM(CASE 
                            WHEN l.status = 'ongoing' THEN (l.amount_paid - l.loan_amount) + (l.due_amount - l.amount_paid)*(1 - d.default_rate_avg)
                            ELSE 0
                        END)
                )::numeric, 2
            ) AS on_going_profit	
        FROM	loans as l CROSS JOIN default_rate_avg as d
        WHERE 
            EXTRACT(WEEK FROM created_at) = EXTRACT(WEEK FROM CURRENT_DATE) - 4
            AND EXTRACT(YEAR FROM created_at) = EXTRACT(YEAR FROM CURRENT_DATE)
        GROUP BY 
            EXTRACT(WEEK FROM created_at), EXTRACT(YEAR FROM created_at);
        """
        )
        try:
            results = [
                {
                    'week': item[0],
                    'year': item[1],
                    'qnt_loans': item[2],
                    'qnt_defaulted_loans': item[3],
                    'qnt_ongoing_loans': item[3],
                    'total_revenue': item[4],
                    'total_loan_amount': item[5],
                    'profit': item[6],
                    'ongoing_profit': item[7],
                }
                for item in session.execute(sql)
            ][0]
        except Exception:
            print('error on sql')
            results = {}
        return results

    async def run(self):
        data = self.get_data()
        subject = 'Resumo Semanal - Operações de Empréstimo'
        body = f"""
        Espero que esta mensagem o encontre bem. Segue abaixo o resumo das atividades semanais de nossas operações de empréstimo:

        Semana: {data.get('week')}, Ano: {data.get('year')}
        Total de Empréstimos Emitidos: {data.get('qnt_loans')}
        Número de Empréstimos em Inadimplência: {data.get('qnt_defaulted_loans')}
        Receita Total Gerada: {data.get('total_revenue')}
        Valor Total dos Empréstimos: {data.get('total_loan_amount')}
        Lucro: {data.get('profit')}
        Lucro Presumido: {data.get('ongoing_profit')}

        Fique à vontade para entrar em contato caso precise de mais informações ou tenha alguma dúvida.

        Atenciosamente,
        Cloudwalk
        """
        await self.smtp.sendmail(
            body, subject, ['joao.marques.016@ufrn.edu.br']
        )
