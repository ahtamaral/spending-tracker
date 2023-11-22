import textwrap

class transaction:

    def __init__(self, description, type, value, date):
        self.description = description.replace("\n", " ")
        self.type = type
        self.value = value
        self.date = date
    
    def print(self, format="pretty"):

        if format == "pretty":
            print("---\nDescription: {0}\nType: {1}\nValue: {2}\nDate: {3}\n---".format(self.description, self.type, self.value, self.date))
        elif format == "row":
            # if (len(self.description) > 31):
            #     d = "Dummy text"
            # else:
            #     d = self.description
            d = self.description
            if len(self.description) > 48:
                d = d[0:48]
            print("{0: <50}\t{1: <15}\t{2: <10}\t{3: <12}".format(d, self.type, self.value, str(self.date)))
        elif format == "csv":
            d = self.description
            if len(self.description) > 48:
                d = d[0:48]
            print("{0},{1},{2},{3}".format(d, self.type, self.value, str(self.date)))