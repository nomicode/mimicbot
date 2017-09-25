from mimicbot import filter, generate, process

__version__ = "0.0.0"

class Bot:

    generator = None

    filter = None

    processor = None

    def __init__(self):
        self.generator = generate.Generator()
        self.filter = filter.Filter()
        self.processor = process.Processor()

    def get_text(self):
        text = None
        for i in range(100000):
            text = self.generator.run()
            # print(text)
            try:
                self.filter.run(text)
            except Exception as error:
                print("error: %s" % error)
                continue
            return self.processor.run(text)
        raise Exception("too many failed attempts to filter text")

