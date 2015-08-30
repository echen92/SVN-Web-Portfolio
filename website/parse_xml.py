import xml.etree.ElementTree as ET
import os
from Structures import *
from website.models import Project
BASE = os.path.dirname(os.path.abspath(__file__))


def get_file_type(filepath):
    """ Gets the file extension from a file path """
    filename, file_ext = os.path.splitext(filepath)
    if file_ext == '':
        return 'none'
    return file_ext


def parse_assignments():
    """ Parses all assignments in an XML log and returns a list of Assignments """
    xml_file = os.path.join(BASE, 'svn_list.xml')
    tree = ET.parse(xml_file)
    root = tree.getroot().find('list')

    # Create object for each project in logs
    projects = []
    for entry in root.findall('entry'):  # For each entry
        attribs = entry.attrib
        if attribs['kind'] == 'dir':  # If entry is a directory
            pname = entry.find('name').text
            if '/' not in pname:  # Is project root
                commit = entry.find('commit')
                rev_num = commit.get('revision')
                date = commit.find('date').text
                author = commit.find('author').text
                proj = Assignment(pname, date, rev_num, author)
                projects.append(proj)
                a, created = Project.objects.get_or_create(name=pname)
                a.save()
                # print True, name, rev, author, date
    print 'DEBUG: Found ' + str(len(projects)) + ' projects from logs'

    # Populate each projects file list and their revisions
    for project in projects:  # For each project
        proj_name = project.name
        for entry in root.findall('entry'):  # For each entry
            attribs = entry.attrib
            if attribs['kind'] == 'file':  # If entry is file
                file_path = entry.find('name').text
                if proj_name in file_path:  # If path of file includes project name, it belongs to that project
                    ftype = get_file_type(file_path)
                    size = entry.find('size').text
                    name = os.path.basename(file_path)  # Split the path into actual file name

                    file = File(name, size, ftype)

                    commit = entry.find('commit')
                    rev_num = commit.get('revision')
                    author = commit.find('author').text
                    date = commit.find('date').text

                    rev_info = RevInfo(date, author)
                    file.revisions[rev_num] = rev_info
                    project.files[file_path] = file

        parse_commits(project)
        print 'DEBUG: Parsed all revisions of files in ' + project.name

    return projects


def parse_commits(project):
    """
    Parses through commit history of XML log
    Populates the revisions hash table for each file of an Assignment
    Sets the projects commit message to that of the most recent revision
    """
    xml_file = os.path.join(BASE, 'svn_log.xml')
    tree = ET.parse(xml_file)
    root = tree.getroot()

    for entry in root.findall('logentry'):  # For each commit (revision number)
        rev_num = entry.get('revision')
        date = entry.find('date').text
        author = entry.find('author').text
        mesg = entry.find('msg').text

        # Account for no commit message in xml log
        if mesg is None:
            mesg = ''

        if project.revision == rev_num:
            project.message = mesg

        paths = entry.find('paths')
        for path in paths:  # For each path in paths
            if path.get('kind') == 'file':
                for key in project.files.keys():  # key is path of file in the project
                    if key == path.text[9:]:  # If file in revision matches project file, cuts off /chen320/ from path
                        __file = project.files[key]
                        if rev_num in __file.revisions.keys():
                            rev_info = __file.revisions[rev_num]
                            rev_info.message = mesg  # Update commit message for file
                        else:
                            rev_info = RevInfo(date, author, mesg)  # Add revision info to revision table
                            __file.revisions[rev_num] = rev_info

                        # print key, file.revisions.keys()
