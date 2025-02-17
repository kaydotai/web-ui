import pdb

import pyperclip
from typing import Optional, Type
from pydantic import BaseModel
from browser_use.agent.views import ActionResult
from browser_use.browser.context import BrowserContext
from browser_use.controller.service import Controller, DoneAction
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
from src.controller.views import CoordinatesAction, ClickAction, TypeAction
import logging

logger = logging.getLogger(__name__)


class CustomController(Controller):
    def __init__(self, exclude_actions: list[str] = [],
                 output_model: Optional[Type[BaseModel]] = None
                 ):
        super().__init__(exclude_actions=exclude_actions, output_model=output_model)
        self._register_custom_actions()

    def _register_custom_actions(self):
        """Register all custom browser actions"""

        @self.registry.action("Move mouse to a specific position on playwright page")
        async def move_mouse(browser: BrowserContext, coordinates: CoordinatesAction):
            if not coordinates or not coordinates.get("x") or not coordinates.get("y"):
                return ActionResult(extracted_content="No coordinates provided")
            x = coordinates.get("x")
            y = coordinates.get("y")
            page = await browser.get_current_page()
            await page.mouse.move(x, y)
            return ActionResult(extracted_content=f"Moving mouse to position ({x}, {y})")

        @self.registry.action("Click page on some coordinates")
        async def click_page(browser: BrowserContext, action: ClickAction):
            if not action or not action.get("x") or not action.get("y"):
                return ActionResult(extracted_content="No coordinates provided")
            x = action.get("x")
            y = action.get("y")
            button = action.get("button", "left")
            page = await browser.get_current_page()
            await page.mouse.click(x, y, button=button)
            return ActionResult(extracted_content=f"Clicking on position ({x}, {y})")

        @self.registry.action("Double click page on some coordinates")
        async def double_click_page(browser: BrowserContext, action: ClickAction):
            if not action or not action.get("x") or not action.get("y"):
                return ActionResult(extracted_content="No coordinates provided")
            x = action.get("x")
            y = action.get("y")
            page = await browser.get_current_page()
            await page.mouse.dblclick(x, y, button=action.button)
            return ActionResult(extracted_content=f"Double clicking on position ({x}, {y})")

        @self.registry.action("Type some text on playwright page")
        async def type_text(browser: BrowserContext, params: TypeAction):
            page = await browser.get_current_page()

            # focus on element via mouse click

            # type backspace ten times to clear the field
            for _ in range(10):
                await page.keyboard.press('Backspace')

            await page.keyboard.type(params.text, delay=100)

            return ActionResult(extracted_content=f"Typed text: {text}")


        @self.registry.action("Copy text to clipboard")
        def copy_to_clipboard(text: str):
            pyperclip.copy(text)
            return ActionResult(extracted_content=text)

        @self.registry.action("Paste text from clipboard")
        async def paste_from_clipboard(browser: BrowserContext):
            text = pyperclip.paste()
            # send text to browser
            page = await browser.get_current_page()
            await page.keyboard.type(text)

            return ActionResult(extracted_content=text)
