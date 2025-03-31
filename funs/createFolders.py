import os 
from settings import runSettings as settings 

def createSubmissionFolders(submissionName = "submissionTemplate_RD1_V1"):

    submissionName = os.path.join(os.getcwd(), submissionName)

    if os.path.isdir(submissionName):
        print("Folder exists already, delete folder or choose a new name")
        return
    
    folders = list(settings['sim folder repacking'].keys())
    os.makedirs(submissionName)
    for folder in folders:
        folder_path = os.path.join( submissionName, folder ) 
        os.makedirs( folder_path )
        
        filename = "Put_your_{}_stls_here".format(folder)
        with open(os.path.join(folder_path, filename), "w") as f:
            f.write(filename)

    print("Submission folder created.")
    return

if __name__ == "__main__":
    createSubmissionFolders()
