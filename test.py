import xml.etree.ElementTree as ET
from plugins import XMLGenerator


class MainGenerator(XMLGenerator):
    def __int__(self, *plugins) -> None:
        """
        init
        :param plugins: None
        :return: None
        """
        super.__init__()
        self.mainPath = self.rootPath + 'pedestrian_simulation/'
        self.appList = [app for app in plugins]

    def writeMainLaunch(self, path):
        """
        Create configure file of package 'sim_env' dynamically.
        :param path: the path of file(.launch.xml) to write.
        :return:
        """
        launch = MainGenerator.createElement('launch')

        # other applications
        for app in self.appList:
            assert isinstance(app, XMLGenerator), "Expected XMLGenerator"
            appRegister = app.plugin()
            for appElement in appRegister:
                launch.append(appElement)
        # include
        include = MainGenerator.createElement(
            "include",
            props={"file": "$(find sim_env)/launch/config.launch"})
        include.append(MainGenerator.createElement(
            "arg",
            props={"name": "world", "value": "$(arg world_parameter"}))
        include.append(MainGenerator.createElement(
            "arg",
            props={"name": "map", "value": self.userCFG["map"]}))
        include.append(MainGenerator.createElement(
            "arg",
            props={"name": "robot_number", "value": self.userCFG["robots_config"]}))
        include.append(MainGenerator.createElement(
            "arg",
            props={"name": "rviz_file", "value": self.userCFG["rviz_file"]}))

        launch.append(include)
        MainGenerator.indent(launch)

        with open(path, "wb+") as f:
            ET.ElementTree(launch).write(f, encoding='utf-8', xml_declaration=True)

        def plugin(self):
            pass
mainGen = MainGenerator()

mainGen.writeMainLaunch(mainGen.rootPath+"sim_env/launch/main.launch")

