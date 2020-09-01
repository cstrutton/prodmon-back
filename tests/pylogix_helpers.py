class Mock_Comm():

    def __init__(self, tag_dict={}):
        self.tag_dict = tag_dict

    def __enter__(self):
        return Mock_Comm()

    def add(self, tag, value):
        self.tag_dict[tag] = value

    def Read(self, tag):
        if tag not in self.tag_dict:
            return Response(tag, Value=None, Status='Connection failure')
        else:
            return Response(tag, Value=self.tag_dict[tag])


class Response():
    def __init__(self, tag, Value=None, Status='Success'):
        self.TagName = tag
        self.Value = Value
        self.Status = Status
