from pypdf import PdfReader
import ebooklib
from ebooklib import epub

class Action:
    @staticmethod
    def __action__():
        return {
            "name": "reader",
            "author": "Kai",
            "version": "0.0",
            "features": [],
            "group": "",
        }

    def __help__(self, ctx):
        return """
            Default help.
        """

    def __run__(self, ctx): 
        line = ctx.get_string()

        if line.endswith(".pdf"):
            reader = PdfReader(line)
            number_of_pages = len(reader.pages)
            page = reader.pages[0]
            text = page.extract_text()
            print(number_of_pages)
            print(page)
            print(text)
            with ctx.console.pager():
                for page in reader.pages:
                    ctx.console.print(page.extract_text())
        elif line.endswith(".epub"):
            book = epub.read_epub(line)
            with ctx.console.pager():
                for item in book.get_items():
                    if item.get_type() == ebooklib.ITEM_DOCUMENT:
                        ctx.console.print('==================================')
                        ctx.console.print('NAME : ', item.get_name())
                        ctx.console.print('----------------------------------')
                        ctx.console.print(str(item.get_body_content()))
                        ctx.console.print('==================================')
        return ctx

    def __error__(self, ctx, error):
        pass

    def __finish__(self, ctx):
        pass

