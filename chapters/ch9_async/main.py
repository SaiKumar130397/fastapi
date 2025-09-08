from tables import create_tables, drop_tables
import asyncio
from services import *

async def main():

  await create_user("sai", "sai@gmail.com")
  # await create_user("kumar", "kumar@gmail.com")
  # await update_user_email(1, "ssk@gmail.com")

asyncio.run(main()) 
