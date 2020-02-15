from HTMLParser import HTMLParser


class MyHTMLParser(HTMLParser):
    def handle_data(self, data):
        print data
        task.description = data
    taskApi.updateTask(task)

data=${WorkItem}
#print data['System.History']
parser = MyHTMLParser()
parser.feed(data['System.History'])
parser.description = data
