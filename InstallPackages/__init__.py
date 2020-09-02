import os

class InstallPackage:
    def __init__(self, pipmanagername, filepath):
        self.filepath = filepath
        self.pipmanagername = pipmanagername
        self.totalPackages = []
        self.packagesFailedToInstall = []
        self.packagesInstalled = []
        print("*********************************************************")
        print("*            The program is written by asv              *")
        print("*********************************************************")

    def begin(self):
        self.ReadFile()
        self.StartInstallation()
        self.Analyse()

    def AddPackage(self, package):
        self.totalPackages.append(package)

    def InstallPackageName(self, pythonpackage):
        os.system(self.pipmanagername+" install "+pythonpackage)

    def StartInstallation(self):
        for name in self.totalPackages:
            try:
                self.InstallPackageName(name)
            except:
                self.packagesFailedToInstall.append(name)
            finally:
                self.packagesInstalled.append(name)

    def Analyse(self):
        print("******************************************************")
        print("Total number of packages to be installed : "+ str(len(self.totalPackages)))
        print("Number of packages installed successfully : "+ str(len(self.packagesInstalled)))
        print("Number of packages failed to install : "+ str(len(self.packagesFailedToInstall)))
        print("------------------------------------------------------")
        print("Total packages : "+str(self.totalPackages))
        print("Packages installed : "+str(self.packagesInstalled))
        if len(self.packagesFailedToInstall) is 0:
            print("Congratulations. All went well. Say thanks to asv.")
        else:
            print("Packages to be installed manually, due to failure in the automation process : "+str(self.packagesFailedToInstall))
            print(r"skip '\n' while you are installing manually")
        print("******************************************************")


    def ReadFile(self):
        file = open(self.filepath, "r")

        try:
            file = open(self.filepath, "r")
        except :
            print("Requested file not found at the location : "+self.filepath)
            print("please check the file and run the program again")
            exit(0)
        finally:
            print("Reading requirements.txt file...")
            file.seek(0, 2)
            endoffile = file.tell()
            file.seek(0)
            while True:
                packageName = file.readline()
                if packageName == "" and file.tell() == endoffile:
                    print("All packages in the requirements file is loaded successfully.")
                    file.close()
                    break
                self.AddPackage(packageName)
