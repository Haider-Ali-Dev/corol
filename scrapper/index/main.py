import pandas
import asyncio
import sys
sys.path.append("..")
from db import create_connection
from genericpath import exists
from operator import truediv
import uuid
import aiohttp
from bs4 import BeautifulSoup




class PageAlreadyExists(Exception):
    def __init__(self, msg="This page already exists.") -> None:
        self.msg = msg
        super().__init__(msg)

    def __str__(self) -> str:
        return self.msg


class IndexStructure:
    def __init__(self, title: str, meta: dict[str, str], url: str):
        self.title = title
        self.meta = meta
        self.url = url

    def as_dict(self):
        return {
            "title":  self.title,
            "meta": self.meta,
            "url": self.url
        }

    async def exists(self):
        connection = await create_connection()
        url = await connection.fetchval("SELECT url from page where url = $1", self.url)
        connection.close()
        if url == self.url:
            return True
        else:
            return False

    async def save(self):
        connection = await create_connection()
        if await self.exists():
            raise PageAlreadyExists()
        id = uuid.uuid4()
        structure = self.as_dict()
        await connection.execute("""
        INSERT INTO page(title, description, id, keywords, author, url) VALUES($1, $2, $3, $4, $5, $6)
        """, structure["title"],
            structure["meta"].get("description"),
            id.hex, structure["meta"].get("keywords"),
            structure["meta"].get("author"),
            structure["url"]
        )
        connection.close()


class HtmlParser:
    _scrapper = None

    def __init__(self, url: str):
        self.url = url

    async def request(self):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.url) as response:
                    html = await response.text()
                    self._scrapper = BeautifulSoup(html, 'html.parser')
                    return self
        except:
            raise aiohttp.ClientError

    def scrap_website(self) -> IndexStructure:
        title = self._scrapper.select_one('title').text
        meta = self._scrapper.select("meta")
        meta_structure = {}
        for m in meta:
            name = m.attrs.get("name")
            if name == None:
                property_attr = m.attrs.get("property")
                if property_attr == "og:author" or property_attr == "author":
                    meta_structure["author"] = m.attrs.get("content")
                elif property_attr == "og:description" or property_attr == "description":
                    meta_structure["description"] = m.attrs.get("content")
                elif property_attr == "og:keywords" or property_attr == "keywords":
                    meta_structure["keywords"] = m.attrs.get("content")

            if name == "author" or name == "og:author":
                meta_structure["author"] = m.attrs.get("content")
            elif name == "description" or name == "og:description":
                meta_structure["description"] = m.attrs.get("content")
            elif name == "keywords" or name == "og:keywords":
                meta_structure["keywords"] = m.attrs.get("content")

        return IndexStructure(title, meta_structure, self.url)


class XmlParser:
    pass



# async def index_url():
#     urls = pandas.read_csv('../../urldata.csv')
#     urls_secure = urls[urls["label"] != "bad"]
#     count = 0

#     for url in urls_secure.values.tolist():
#         if count >= 44:
#             print("DONE")
#             break
#         if url[0][0].isdigit():
#             print(f"{url[0][0]} starts with a digit skipping")
#         try:
#             print(f"Doing: {url[0]}")
#             parser = await HtmlParser(f"https://{url[0]}").request()
#             await parser.scrap_website().save()
#             print(f"Finished {url[0]} -- Count -> {count}")
#             count += 1
#         except:
#             print(f"{url[0]} Errored")
#             continue

# loop = asyncio.get_event_loop()
# loop.run_until_complete(index_url())
