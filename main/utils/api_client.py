import aiohttp
import asyncio
import threading

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QMetaObject, Qt, QTimer, pyqtSignal, QObject, Q_ARG


class APIClient:
    def __init__(self, api_headers):
        self.api_headers = api_headers

        self.loop = asyncio.new_event_loop()

        self.session = None

        # Run in separate thread
        self.thread = threading.Thread(target=self.run_loop, daemon=True)
        self.thread.start()

    def run_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    async def start_session(self):
        if self.session is None:
            # Limit concurrent requests to 10
            connector = aiohttp.TCPConnector(limit=10)

            self.session = aiohttp.ClientSession(headers=self.api_headers, connector=connector)

    async def fetch(self, url, for_loading_screen=False, progress_bar=None, start_value=None, end_value=None, counter=None):
        if self.session is None:
            await self.start_session()

        if url == "":
            return ""

        async with self.session.get(url) as response:
            if for_loading_screen:
                content = await response.json()
                counter["completed"] += 1

                percentage = int(((counter["completed"] + start_value) / end_value) * 100)

                # This safely updates the progress bar in the main thread
                # Q_ARG wraps percentage, it converts it into QGenericArgument
                QMetaObject.invokeMethod(progress_bar, "setValue", Qt.ConnectionType.QueuedConnection,
                                         Q_ARG(int, percentage))

                return content
            else:
                return await response.json()

    async def multi_fetch(self, urls, progress_bar, start_value, end_value):
        counter = {"completed": 0}
        tasks = [self.fetch(url, True, progress_bar, start_value, end_value, counter) for url in urls]

        # * means that a list is unpacked into separate arguments
        # In other words, one argument for item in the list
        return await asyncio.gather(*tasks)

    async def fetch_image(self, url, for_loading_screen=False, progress_bar=None, start_value=None, end_value=None, counter=None):
        if self.session is None:
            await self.start_session()

        if url == "":
            return ""

        async with self.session.get(url) as response:
            if for_loading_screen:
                image_content = await response.content.read()
                counter["completed"] += 1

                percentage = int(((counter["completed"] + start_value) / end_value) * 100)

                # This safely updates the progress bar in the main thread
                QMetaObject.invokeMethod(progress_bar, "setValue", Qt.ConnectionType.QueuedConnection,
                                         Q_ARG(int, percentage))

                return image_content
            else:
                return await response.content.read()

    async def fetch_all_images(self, urls, progress_bar, start_value, end_value):
        # Create a list of tasks
        counter = {"completed": 0}
        tasks = [self.fetch_image(url, True, progress_bar, start_value, end_value, counter) for url in urls]

        # * means that a list is unpacked into separate arguments
        # In other words, one argument for item in the list
        return await asyncio.gather(*tasks)

    async def close_session(self):
        if self.session:
            future = asyncio.run_coroutine_threadsafe(self.session.close(), self.loop)
            future.result()

        self.loop.call_soon_threadsafe(self.loop.stop)
        self.thread.join()

