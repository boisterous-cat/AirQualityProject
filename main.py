import asyncio

'''
мы должны импортировать только то, что будем использовать!
асинх функция может вызывать только асин функцию
асинхронность только на уровне языка, процессорную асинхроность она не трогает
ппроверка на то какой файл 
начала выполняется первый таск потом торой
future - асинх функция в которой есть елд, ждет когда future сбудется.

'''
async def dummy():
    return

async def print_nums(n):
    count=0
    while True:
        if count % 10==0:
            print(n, count)
        count += 1
        await dummy()
        #await asyncio.sleep(0.1)
        if count ==1000:
            return

async def main():
    #task это как сопрограмма
   task1=asyncio.create_task(print_nums(1))
   task2 = asyncio.create_task(print_nums(2))

   await asyncio.gather(task2, task1) #ждем выполенниея тасков

if __name__=="__main__":
    asyncio.run(main())


