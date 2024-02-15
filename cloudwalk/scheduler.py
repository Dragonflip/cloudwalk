import asyncio
from rocketry import Rocketry
from rocketry.conds import daily

from cloudwalk.email_handler import SmtpHandler, SendMail
from cloudwalk.settings import Settings

app = Rocketry(execution='async')


@app.task(daily.at('00:00'))
async def do_things():
    print('enviando emails...')
    smtp = SmtpHandler(Settings())    # type: ignore
    send_mail = SendMail(smtp)
    task = asyncio.create_task(send_mail.run())
    await task
