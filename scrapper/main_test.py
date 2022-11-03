import struct
from index.main import HtmlParser
import unittest
import asyncio

class HtmlParserTest(unittest.TestCase):
    def setUp(self) -> HtmlParser:
        self.parser = HtmlParser("https://stackoverflow.com/")
    
    def runTest(self):
        loop = asyncio.get_event_loop()
        result  = loop.run_until_complete(self.parser.request())
        structure = result.scrap_website()
        print(structure.as_dict())
        loop.run_until_complete(structure.save())
        self.assertEqual(structure, structure)


unittest.main()

        
    
