class Mock_Comm():

    def __init__(self, tag_list):
        self.tag_list = tag_list

    def Read(self, tag):
        if tag not in self.tag_list:
            return Response(tag, Value=None, Status='Connection failure')
        else:
            return Response(tag, Value=self.tag_list[tag])


class Response():
    def __init__(self, tag, Value=None, Status='Success'):
        self.TagName = tag
        self.Value = Value
        self.Status = Status
