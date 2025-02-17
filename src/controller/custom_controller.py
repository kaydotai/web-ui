import asyncio
from pyparsing import C
import pyperclip
from typing import Optional, Type
from pydantic import BaseModel
from browser_use.agent.views import ActionResult
from browser_use.browser.context import BrowserContext
from browser_use.controller.service import Controller 
from main_content_extractor import MainContentExtractor
from browser_use.controller.views import (
    ClickElementAction,
    DoneAction,
    ExtractPageContentAction,
    GoToUrlAction,
    InputTextAction,
    OpenTabAction,
    ScrollAction,
    SearchGoogleAction,
    SendKeysAction,
    SwitchTabAction,
)
from src.controller.views import Coordinates, Coordinates, TypeAction, WaitTime
import logging

logger = logging.getLogger(__name__)


class CustomController(Controller):
    def __init__(self, exclude_actions: list[str] = [],
                 output_model: Optional[Type[BaseModel]] = None,
                 ):
        super().__init__(exclude_actions=exclude_actions, output_model=output_model)
        self._register_custom_actions()

    def _register_custom_actions(self):
        """Register all custom browser actions"""

        @self.registry.action("Move the cursor to a specified (x, y) pixel coordinate on the screen",param_model=Coordinates)
        async def move_mouse(browser: BrowserContext, coordinates: Coordinates):
            if not coordinates or not coordinates.x or not coordinates.y:
                return ActionResult(extracted_content="No coordinates provided")
            x = coordinates.x
            y = coordinates.x
            page = await browser.get_current_page()
            await page.mouse.move(x, y)
            return ActionResult(extracted_content=f"Moved mouse to position ({x}, {y})", include_in_memory=True)


        @self.registry.action("Click the left mouse button")
        async def left_click(browser: BrowserContext):
            # TODO (@aman): Get mouse position
            x, y = 1000, 1000          
            button = "right"
            button = "left"
            page = await browser.get_current_page()
            await page.mouse.click(x, y, button=button)
            return ActionResult(extracted_content=f"Clicked left mouse button", include_in_memory=True)

        @self.registry.action("Click the right mouse button")
        async def right_click(browser: BrowserContext):
            # TODO (@aman): Get mouse position
            x, y = 1000, 1000          
            button = "right"
            page = await browser.get_current_page()
            await page.mouse.click(x, y, button=button)
            return ActionResult(extracted_content=f"Clicked right mouse button", include_in_memory=True)


        @self.registry.action("Double-click the left mouse button")
        async def double_click(browser: BrowserContext):
            # TODO (@aman): Get mouse position
            x, y = 1000, 1000
            page = await browser.get_current_page()
            await page.mouse.dblclick(x, y, button="left")
            return ActionResult(extracted_content=f"Double clicked on left mouse button", include_in_memory=True)

        @self.registry.action("Type a string of text on the keyboard", param_model=TypeAction)
        async def type(browser: BrowserContext, params: TypeAction):
            page = await browser.get_current_page()

            # focus on element via mouse click

            # type backspace ten times to clear the field
            for _ in range(10):
                await page.keyboard.press('Backspace')

            await page.keyboard.type(params.text, delay=100)

            return ActionResult(extracted_content=f"Typed text: {params.text}", include_in_memory=True)


        @self.registry.action("Wait specified seconds for the change to happen.", param_model=WaitTime)
        async def wait(browser: BrowserContext, params: WaitTime):
            await asyncio.sleep(params.time)

            return ActionResult(extracted_content=f"Waited for {params.time} seconds", include_in_memory=True)

