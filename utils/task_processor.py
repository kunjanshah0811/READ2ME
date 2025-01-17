import asyncio
import logging
from threading import Thread, Event
from utils.task_file_handler import get_tasks, clear_tasks
from utils.synthesize import synthesize_text_to_speech as synthesize_edge_tts, read_text
from utils.env import setup_env
from utils.history_handler import add_to_history, check_history

output_dir, task_file, img_pth, sources_file = setup_env()

def process_tasks(stop_event):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    async def process():
        while not stop_event.is_set():
            tasks = await get_tasks()
            if tasks:
                logging.info(f"Tasks retrieved: {tasks}")

            for task in tasks:
                task_type = task.get('type')
                content = task.get('content')
                tts_engine = task.get('tts_engine')

                if not all([task_type, content, tts_engine]):
                    logging.error(f"Invalid task format: {task}")
                    continue

                # Check if the URL has been processed before
                if task_type == "url" and await check_history(content):
                    logging.info(f"URL {content} has already been processed. Skipping.")
                    continue

                if task_type == "url":
                    if tts_engine == "styletts2":
                        from utils.synthesize_styletts2 import say_with_styletts2
                        await say_with_styletts2(content, output_dir, img_pth)
                    elif tts_engine == "piper":
                        from utils.synthesize_piper import url_with_piper
                        await url_with_piper(content, output_dir, img_pth)
                    else:
                        await synthesize_edge_tts(content, output_dir, img_pth)
                    await add_to_history(content)  # Add URL to history after processing
                elif task_type == "text":
                    if tts_engine == "styletts2":
                        from utils.synthesize_styletts2 import text_to_speech_with_styletts2
                        await text_to_speech_with_styletts2(content,"Text", output_dir, img_pth)
                    elif tts_engine == "piper":
                        from utils.synthesize_piper import read_text_piper
                        await read_text_piper(content, output_dir, img_pth)

                    else:
                        await read_text(content, output_dir, img_pth)
            if tasks:
                await clear_tasks()
            await asyncio.sleep(5)

    loop.run_until_complete(process())

def start_task_processor(stop_event):
    thread = Thread(target=process_tasks, args=(stop_event,))
    thread.daemon = True
    thread.start()
    return thread