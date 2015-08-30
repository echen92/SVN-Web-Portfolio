from django.shortcuts import render, get_object_or_404
from website.parse_xml import *
from website.models import Project
from django.http import Http404
from django.views.decorators.csrf import csrf_protect
project_list = parse_assignments()


def index(request):
    context = {'project_list': project_list}
    return render(request, 'main/index.html', context)


@csrf_protect
def message(request, id):
    project = get_object_or_404(Project, pk=id)
    context = {'message': project, 'proj_name': project.name}
    return render(request, 'core/message.html', context)


def project_page(request, project_name=None):
    proj = get_project(project_name)

    if proj is None:
        return render(request, 'main/index.html')

    try:
        post = Project.objects.get(name=project_name)
    except Project.DoesNotExist:
        raise Http404

    context = {'project': proj, 'project_list': project_list, 'post': post,
               'message': get_object_or_404(Project, name=project_name)}
    return render(request, 'main/project.html', context)


def file_page(request, project_name=None, file_name=None):
    proj = get_project(project_name)
    file, path, revisions = get_file_and_path(file_name, project_name)

    if proj is None:
        return render(request, 'main/index.html')

    context = {'project': proj, 'project_list': project_list,
               'file': file, 'filepath': path, 'revisions': revisions}
    return render(request, 'main/file.html', context)


def get_rev_info(revisions, rev_num):
    """ Helper function to get a revisions info given rev_num """
    for key in revisions.keys():
        if key == rev_num:
            return revisions[key]

    return None


def get_project(name):
    """ Helper functions to get a project object given the name """
    for proj in project_list:
        if proj.name == name:
            return proj

    return None


def get_file_and_path(name, proj_name):
    """ Helper function to get the file, key, and revisions table of a project """
    proj = get_project(proj_name)
    for key in proj.files.keys():
        file = proj.files[key]
        if file.name == name:
            print key
            return file, key, file.revisions