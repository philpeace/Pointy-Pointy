class Manager(object):
    def __init__(self):
        pass

    @staticmethod
    def getModuleAndControllerNames(path):
        if path.find(':') == -1:
            module_name = 'controllers.%s' % path
            class_name = path
        else:
            module_name, class_name = path.split(':', 1)

        return (module_name, class_name)