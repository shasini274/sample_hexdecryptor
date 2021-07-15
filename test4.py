import logging
from glob import glob
from pathlib import Path
import csv
import ntpath
from logging.handlers import TimedRotatingFileHandler
import re
from xml.etree import ElementTree as ET

formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
handler = TimedRotatingFileHandler('logs/logfile.log',
                                   when='midnight',
                                   backupCount=10)
handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.INFO)
col_list = ["Filename", "Directory", "Camera", "Object Class", "xmin"
    , "ymin", "xmax", "ymax", "Image Width", "Image Height"]

coloumnHeading = "Filename;Directory;Camera;Object Class" \
                 ";xmin;ymin;xmax;ymax;Image Width" \
                 ";Image Height" + '\n'


class Extractor():

    def __init__(self):
        logger.info("Extracting info started..")

    def annotations_create(self):
        # check the comments underneath the 'data_merge' function
        def data_merger(annotateTree):
            """
                :param annotateTree: This should be the XML identifier - <xml.etree.ElementTree.ElementTree object at 0x00000255988C6160>
                                        to extract elements from the xml file and write it on csv
            """

            global imageWidth, imageHeight
            root = annotateTree.getroot()
            xMin = []
            yMin = []
            xMax = []
            yMax = []
            classesFound = []
            filename = root[1].text
            directory = root[2].text
            pathWithoutFilename = directory.split('/')
            requiredPath = "/" + '/'.join(directory.split('/')[1:-1])
            cameraType = (pathWithoutFilename[-1].split('_'))[0]

            for value in annotateTree.iterfind('size'):
                imageWidth = value.findtext('width')
                imageHeight = value.findtext('height')

            for item in annotateTree.iterfind('object'):
                classesFound.append(item.findtext('name'))

            for dimension in annotateTree.findall("./object/bndbox"):
                xMin.append(dimension.findtext('xmin'))
                yMin.append(dimension.findtext('ymin'))
                xMax.append(dimension.findtext('xmax'))
                yMax.append(dimension.findtext('ymax'))

            with open('fieldtest_annotations.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                for i in range(len(classesFound)):
                    writer.writerow([filename, requiredPath, cameraType, classesFound[i],
                                     xMin[i], yMin[i], xMax[i], yMax[i], imageWidth, imageHeight])

        #############################################################################################
        annotationFileName = 'fieldtest_annotations.csv'
        annotationFilePath = Path(annotationFileName)

        if annotationFilePath.is_file():
            logger.info("fieldtest_annotations.csv already exist")

            for filepath in glob('data\\*.xml'):
                # get ONLY the xml filename (without the .xml extention)
                # ntpath.basename - means extracts the 'Cam02_0010 13-44-67.xml' from 'data/Cam02_0010 13-44-67.xml'
                # ntpath.splitext and [0] - means getting only the first part --> Cam02_0010 13-44-67
                # Extra note - 'ntpath' method is used to make it compatible with windows environment, as in windows environment
                # paths can be denote from forward slash and backward slash both unlike in linux
                # Otherwise if this was used in Linux environment, 'os.path' method can be easily used instead of 'ntpath'
                name = ntpath.splitext(ntpath.basename(filepath))[0]

                # load the fieldtest_annotations.csv
                with open(annotationFileName, 'rt') as f:
                    reader = csv.reader(f, delimiter=',')
                    for row in reader:
                        # check if the variable name(xml file name) exist in the column1
                        # re.search means -- it searches for a content which is similar to xml name Ex: Cam02_0010 13-44-67
                        # in each row first column
                        # thats why it has a row[0] like below -> it only consider the first column value of each row
                        if re.search(name, row[0]):
                            # if it does exist it breaks the loop and go to the outer loop, without check in the other rows
                            logger.info("%s.xml already exist" % name)
                            break
                    else:
                        # if the file name does not exist in any row of the csv, the program will lead to the next step
                        logger.info("%s.xml does not exist" % name)
                        annotateTree = ET.parse(filepath)
                        data_merger(annotateTree)
        else:
            logger.info("fieldtest_annotations.csv does not exist")
            with open(annotationFileName, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(col_list)

            for filepath in glob('data\\*.xml'):
                annotateTree = ET.parse(filepath)
                data_merger(annotateTree)

    def training_create(self):

        def fetch_from_classes(getClassName):
            """
                :param getClassName: This is a string, which is extracted from the 'fieldtest_annotations.csv' file
                :return: If detect_classes.txt is provieded with classes assigned, the classID which corresponds
                        to the classname will return else, return none

            """
            try:
                fin = open("detect_classes.txt", 'r')
                content = fin.read()
                words = content.split("\n")
                fin.close()
                actualData = words[0:len(words) - 1]
                classData = [0 for x in range(len(words) - 1)]

                for j in range(0, len(words[0:len(words) - 1])):
                    classData[j] = str(j)

                mapping = dict(zip(actualData, classData))
                classId = mapping[getClassName]
                return classId

            except IOError:
                logger.error("No prior classes assigned")
                return None

        def create_text(syntaxValidate):
            """
               :param syntaxValidate: This is a string of corresponding row, which is extracted from the 'fieldtest_annotations.csv' file
               :return: the required syntax which should be written in the annotations_for_training.txt file
            """
            syntaxSplit = syntaxValidate.split(';')
            classId = fetch_from_classes(syntaxSplit[3])
            if classId is not None:
                requiredSyntax = (syntaxSplit[1] + "/" + syntaxSplit[0] + " " + syntaxSplit[4] + ","
                                  + syntaxSplit[5] + "," + syntaxSplit[6] + "," + syntaxSplit[7] + "," + classId)
                return requiredSyntax
            else:
                logger.error("classId is none")
                return None

        with open('annotations_for_training.txt', "w") as my_output_file:
            with open('fieldtest_annotations.csv', "r") as my_input_file:
                for row in csv.reader(my_input_file):
                    syntaxValidate = ";".join(row) + '\n'
                    if (syntaxValidate == coloumnHeading):
                        logger.info("Coloumn heading neglected")
                    else:
                        createTextStatus = create_text(syntaxValidate)
                        if createTextStatus is not None:
                            my_output_file.write(createTextStatus + '\n')
            my_output_file.close()


if __name__ == '__main__':
    m = Extractor()
    m.annotations_create()
    # m.training_create()
