from unittest import TestCase
import parse_xml


class TestParseCommits(TestCase):
    projects = parse_xml.parse_assignments()

    def test_parse_commits(self):
        for project in self.projects:
            self.assertTrue(len(self.projects) > 0)
            self.assertTrue(project.name is not None)
            self.assertTrue(project.revision != 0)
            self.assertEqual(project.author, 'chen320')
            self.assertTrue(project.date is not None)
            self.assertTrue(project.message is not None)

    def test_file_types(self):
        types = ['.pdf', '.xml', '.java', '.idea', '.json', '.iml', 'none', '.h', '.cpp', '.obj', '.py', '.html']
        for project in self.projects:
            for fkey in project.files.keys():
                __file = project.files[fkey]
                self.assertTrue(__file.name is not None)
                self.assertTrue(__file.size > 0)
                self.assertTrue(__file.ftype in types)

    def test_revisions(self):
        for project in self.projects:
            for fkey in project.files.keys():
                __file = project.files[fkey]
                for rkey in __file.revisions.keys():
                    __revinfo = __file.revisions[rkey]
                    self.assertTrue(rkey > 0)
                    self.assertTrue(__revinfo.date is not None)
                    self.assertTrue(__revinfo.author == 'chen320')
                    self.assertTrue(__revinfo.message is not None)