import threading
import asyncio
import psutil
from youtubezeno import SEA, start_streaming

resource_pressure = False  # نستخدمه للتحكم في التهدئة داخل الكود

async def monitor_resources():
    global resource_pressure
    warned = False
    while True:
        cpu = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory().percent

        if cpu > 85 or ram > 85:
            resource_pressure = True
            if not warned:
                print(f"[⚠️] ضغط عالي - CPU: {cpu}%, RAM: {ram}% — تهدئة بسيطة...")
                warned = True
        else:
            resource_pressure = False
            warned = False

        await asyncio.sleep(3)

async def main():
    room_id = "67c0e1513a71d9519de45efa"
    token = "04ce03641be3557f70593f7edc070d25fa5e8ae5aefd4d1464f3c8f6a872f87a"
    bot_instance = SEA()

    # تشغيل البث في ثريد منفصل
    streaming_thread = threading.Thread(target=start_streaming, args=(bot_instance,))
    streaming_thread.daemon = True
    streaming_thread.start()

    # تشغيل مراقبة الموارد
    asyncio.create_task(monitor_resources())

    while True:
        try:
            await bot_instance.run(room_id, token)
            # تهدئة بسيطة فقط لو الضغط عالي
            if resource_pressure:
                await asyncio.sleep(10)
            else:
                await asyncio.sleep(3)
        except Exception as e:
            print(f"Bot error: {e}. Restarting in 5 seconds...")
            await asyncio.sleep(5)

if __name__ == '__main__':
    asyncio.run(main())
