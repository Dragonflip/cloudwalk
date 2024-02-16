import asyncio
from rocketry import Rocketry
from rocketry.conds import daily, weekly

from cloudwalk.email_handler import (
    SmtpHandler,
    OnGoingLoansEmail,
    SummarizingOperationMail,
)
from cloudwalk.settings import Settings

app = Rocketry(execution='async')


@app.task(daily.at('00:00'))
async def on_going_loans_email():
    print('enviando emails...')
    smtp = SmtpHandler(Settings())    # type: ignore
    send_mail = OnGoingLoansEmail(smtp)
    task = asyncio.create_task(send_mail.run())
    await task


@app.task(weekly.at('00:00'))
async def summarizing_operation_email():
    print('enviando emails...')
    smtp = SmtpHandler(Settings())    # type: ignore
    send_mail = SummarizingOperationMail(smtp)
    task = asyncio.create_task(send_mail.run())
    await task
