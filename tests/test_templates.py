"""Unit-tests for the `gitignore_builder.config.templates` module."""
import logging
from pathlib import Path
from tempfile import TemporaryDirectory
from textwrap import dedent
from typing import List
from typing import Optional
from unittest import TestCase

from gitignore_builder.config.templates import IDE_TEMPLATES
from gitignore_builder.config.templates import LANG_TEMPLATES
from gitignore_builder.config.templates import OS_TEMPLATES
from gitignore_builder.config.templates import Template
from gitignore_builder.config.templates import Templates

_log = logging.getLogger(__name__)
_log.addHandler(logging.NullHandler())


class TemplateClsTest(TestCase):
    """Unit-tests for the Template class."""

    name: Optional[str]
    urls: Optional[List[str]]
    template: Optional[Template]

    def __init__(self, methodName="runTest"):  # noqa
        super().__init__(methodName)
        self.name = None
        self.urls = None
        self.template = None

    def setUp(self) -> None:
        self.name = "linux"
        self.urls = [
            "https://github.com/github/gitignore/raw/main/Global/Linux.gitignore",
            "https://www.toptal.com/developers/gitignore/api/linux"
        ]
        self.template = Template(self.name, self.urls)

    def tearDown(self) -> None:
        self.template = None
        self.urls = None
        self.name = None

    def test_instance_creation(self):
        self.assertEqual(self.name, self.template.name)
        self.assertListEqual(self.urls, self.template.urls)

    def test_as_dict(self):
        expected = {
            "name": self.name,
            "urls": self.urls
        }
        actual = self.template.as_dict()
        self.assertDictEqual(expected, actual)

    def test_from_dict_with_good_data(self):
        data = {
            "name": self.name,
            "urls": self.urls
        }
        expected = self.template
        actual = Template.from_dict(data)
        self.assertEqual(expected, actual)

    def test_from_dict_with_missing_keys(self):
        data_without_name = dict(urls=self.urls)
        with self.assertRaises(ValueError) as ctx:
            Template.from_dict(data_without_name)
        expected_args = ("data", data_without_name)
        actual_args = ctx.exception.args
        self.assertTupleEqual(expected_args, actual_args)

        data_without_urls = dict(name=self.name)
        with self.assertRaises(ValueError) as ctx:
            Template.from_dict(data_without_urls)
        expected_args = ("data", data_without_urls)
        actual_args = ctx.exception.args
        self.assertTupleEqual(expected_args, actual_args)

    def test_from_dict_bad_name_type(self):
        name = object()
        urls = self.urls
        data = {"name": name, "urls": urls}
        with self.assertRaises(TypeError) as ctx:
            Template.from_dict(data)
        expected_args = ("name", str, object, name)
        actual_args = ctx.exception.args
        self.assertTupleEqual(expected_args, actual_args)

    def test_from_dict_bad_name_value(self):
        name = " "
        urls = self.urls
        data = {"name": name, "urls": urls}
        with self.assertRaises(ValueError) as ctx:
            Template.from_dict(data)
        expected_args = ("name", name)
        actual_args = ctx.exception.args
        self.assertTupleEqual(expected_args, actual_args)

    def test_from_dict_bad_urls_type(self):
        name = self.name
        urls = object()
        data = {"name": name, "urls": urls}
        with self.assertRaises(TypeError) as ctx:
            Template.from_dict(data)
        expected_args = ("urls", list, object, urls)
        actual_args = ctx.exception.args
        self.assertTupleEqual(expected_args, actual_args)

    def test_from_dict_bad_urls_value(self):
        name = self.name
        urls = ["", " ", "\n", "\t"]
        data = {"name": name, "urls": urls}
        with self.assertRaises(ValueError) as ctx:
            Template.from_dict(data)
        expected_args = ("urls", urls)
        actual_args = ctx.exception.args
        self.assertTupleEqual(expected_args, actual_args)

    def test_from_dict_bad_urls_item_type(self):
        name = self.name
        last_url = object()
        urls = self.urls + [last_url, ]  # noqa
        data = {"name": name, "urls": urls}
        with self.assertRaises(TypeError) as ctx:
            Template.from_dict(data)
        expected_args = ("urls[2]", str, object, last_url)
        actual_args = ctx.exception.args
        self.assertTupleEqual(expected_args, actual_args)


class TemplatesClsTest(TestCase):
    """Unit-tests for the Templates class."""

    linux_template: Optional[Template]
    macos_template: Optional[Template]
    windows_template: Optional[Template]

    templates: Optional[Templates]

    def __init__(self, methodName="runTest"):  # noqa
        super().__init__(methodName)
        self.linux_template = None
        self.macos_template = None
        self.windows_template = None
        self.templates = None

    def setUp(self) -> None:
        self.linux_template = Template(
            name="linux",
            urls=[
                "https://github.com/github/gitignore/raw/main/Global/Linux.gitignore",
                "https://www.toptal.com/developers/gitignore/api/linux"
            ]
        )
        self.macos_template = Template(
            name="macos",
            urls=[
                "https://github.com/github/gitignore/raw/main/Global/macOS.gitignore",
                "https://www.toptal.com/developers/gitignore/api/macos"
            ]
        )
        self.windows_template = Template(
            name="windows",
            urls=[
                "https://github.com/github/gitignore/raw/main/Global/Windows.gitignore",
                "https://www.toptal.com/developers/gitignore/api/windows"
            ]
        )
        self.templates = Templates(
            templates=[
                self.linux_template,
                self.macos_template,
                self.windows_template
            ]
        )

    def tearDown(self) -> None:
        self.templates = None
        self.windows_template = None
        self.macos_template = None
        self.linux_template = None

    def test_instance_creation(self):
        self.assertIn(self.linux_template, self.templates.templates)
        self.assertIn(self.macos_template, self.templates.templates)
        self.assertIn(self.windows_template, self.templates.templates)

    def test_as_dict(self):
        expected = {
            "templates": [
                self.linux_template.as_dict(),
                self.macos_template.as_dict(),
                self.windows_template.as_dict()
            ]
        }
        actual = self.templates.as_dict()
        self.assertDictEqual(expected, actual)

    def test_from_dict_with_good_data(self):
        data = {
            "templates": [
                self.linux_template.as_dict(),
                self.macos_template.as_dict(),
                self.windows_template.as_dict()
            ]
        }
        expected = self.templates
        parsed = Templates.from_dict(data)
        self.assertEqual(expected, parsed)

    def test_from_dict_with_missing_templates_key(self):
        templates = [
            self.linux_template,
            self.macos_template,
            self.windows_template
        ]
        data = dict(template=templates)
        with self.assertRaises(ValueError) as ctx:
            Templates.from_dict(data)
        expected_args = ("data", data)
        actual_args = ctx.exception.args
        self.assertTupleEqual(expected_args, actual_args)

    def test_from_dict_with_bad_templates_type(self):
        templates = object()
        data = dict(templates=templates)
        with self.assertRaises(TypeError) as ctx:
            Templates.from_dict(data)  # noqa
        expected_args = ("templates", list, object, templates)
        actual_args = ctx.exception.args
        self.assertTupleEqual(expected_args, actual_args)

    def test_from_dict_with_bad_templates_item_type(self):
        last_template = object()
        templates = [
            self.linux_template.as_dict(),
            self.macos_template.as_dict(),
            self.windows_template.as_dict(),
            last_template
        ]
        data = dict(templates=templates)
        with self.assertRaises(TypeError) as ctx:
            Templates.from_dict(data)
        expected_args = ("templates[3]", dict, object, last_template)
        actual_args = ctx.exception.args
        self.assertTupleEqual(expected_args, actual_args)

    def test_from_dict_with_empty_templates_items_list(self):
        templates = [
        ]
        data = dict(templates=templates)
        with self.assertRaises(ValueError) as ctx:
            Templates.from_dict(data)
        expected_args = ("templates", templates)
        actual_args = ctx.exception.args
        self.assertTupleEqual(expected_args, actual_args)

    def test_from_dict_with_bad_templates_item_value(self):
        last_template = {}
        templates = [
            self.linux_template.as_dict(),
            self.macos_template.as_dict(),
            self.windows_template.as_dict(),
            last_template
        ]
        data = dict(templates=templates)
        with self.assertRaises(ValueError) as ctx:
            Templates.from_dict(data)
        expected_args = ("templates[3]", last_template)
        actual_args = ctx.exception.args
        self.assertTupleEqual(expected_args, actual_args)

    def test_as_json(self):
        expected = dedent("""\
            {
                "templates": [
                    {
                        "name": "linux",
                        "urls": [
                            "https://github.com/github/gitignore/raw/main/Global/Linux.gitignore",
                            "https://www.toptal.com/developers/gitignore/api/linux"
                        ]
                    },
                    {
                        "name": "macos",
                        "urls": [
                            "https://github.com/github/gitignore/raw/main/Global/macOS.gitignore",
                            "https://www.toptal.com/developers/gitignore/api/macos"
                        ]
                    },
                    {
                        "name": "windows",
                        "urls": [
                            "https://github.com/github/gitignore/raw/main/Global/Windows.gitignore",
                            "https://www.toptal.com/developers/gitignore/api/windows"
                        ]
                    }
                ]
            }""")
        actual = self.templates.as_json()
        self.assertEqual(expected, actual)

    def test_from_json(self):
        text = dedent("""\
            {
                "templates": [
                    {
                        "name": "linux",
                        "urls": [
                            "https://github.com/github/gitignore/raw/main/Global/Linux.gitignore",
                            "https://www.toptal.com/developers/gitignore/api/linux"
                        ]
                    },
                    {
                        "name": "macos",
                        "urls": [
                            "https://github.com/github/gitignore/raw/main/Global/macOS.gitignore",
                            "https://www.toptal.com/developers/gitignore/api/macos"
                        ]
                    },
                    {
                        "name": "windows",
                        "urls": [
                            "https://github.com/github/gitignore/raw/main/Global/Windows.gitignore",
                            "https://www.toptal.com/developers/gitignore/api/windows"
                        ]
                    }
                ]
            }""")
        expected = self.templates
        actual = Templates.from_json(text)
        self.assertEqual(expected, actual)

    def test_add_operator_with_good_type(self):
        templates_list = []
        templates_list.extend(OS_TEMPLATES.templates)
        templates_list.extend(IDE_TEMPLATES.templates)
        templates_list.extend(LANG_TEMPLATES.templates)
        expected = Templates(templates=templates_list)
        actual = OS_TEMPLATES + IDE_TEMPLATES + LANG_TEMPLATES
        self.assertIsInstance(actual, Templates)
        self.assertEqual(expected, actual)

    def test_add_operator_with_bad_type(self):
        other = object()
        with self.assertRaises(TypeError) as ctx:
            # pylint: disable=pointless-statement
            OS_TEMPLATES + other  # noqa
        expected_args = (Templates, object, other)
        actual_args = ctx.exception.args
        self.assertTupleEqual(expected_args, actual_args)

    def test_save_to_file_with_existing_parent_location(self):
        templates = self.templates
        expected_contents = templates.as_json()

        with TemporaryDirectory() as temp_dir:
            temp_dir_path = Path(temp_dir)

            file = temp_dir_path / "templates.json"
            self.assertFalse(file.exists())
            self.assertTrue(file.parent.exists())

            templates.save(file)
            self.assertTrue(file.exists())
            self.assertTrue(file.is_file())

            actual_contents = file.read_text(encoding="ascii")
            file.unlink()

        self.assertEqual(expected_contents, actual_contents)

    def test_save_to_file_with_nonexistent_parent_location(self):
        templates = self.templates
        expected_contents = templates.as_json()

        with TemporaryDirectory() as temp_dir:
            temp_dir_path = Path(temp_dir)

            file = temp_dir_path / "my/templates.json"
            self.assertFalse(file.exists())
            self.assertFalse(file.parent.exists())

            templates.save(file)
            self.assertTrue(file.parent.exists())
            self.assertTrue(file.exists())
            self.assertTrue(file.is_file())

            actual_contents = file.read_text(encoding="ascii")
            file.unlink()

        self.assertEqual(expected_contents, actual_contents)

    def test_save_to_file_pointing_existing_folder_location(self):
        templates = self.templates
        file = Path.cwd()
        with self.assertRaises(IsADirectoryError) as ctx:
            templates.save(file)
        expected_args = (file,)
        actual_args = ctx.exception.args
        self.assertTupleEqual(expected_args, actual_args)

    def test_save_to_file_with_bad_object_type(self):
        templates = self.templates
        file = object()
        with self.assertRaises(TypeError) as ctx:
            templates.save(file)  # noqa
        expected_args = ("file", Path, object, file)
        actual_args = ctx.exception.args
        self.assertTupleEqual(expected_args, actual_args)

    def test_load_from_existing_file_with_good_data(self):
        original_templates = self.templates
        with TemporaryDirectory() as temp_dir:
            temp_dir_path = Path(temp_dir)

            file = temp_dir_path / "templates.json"
            self.assertFalse(file.exists())

            original_templates.save(file)
            parsed_templates = Templates.load(file)
            file.unlink()
        self.assertEqual(original_templates, parsed_templates)

    def test_load_from_existing_file_with_no_data(self):
        with TemporaryDirectory() as temp_dir:
            temp_dir_path = Path(temp_dir)

            file = temp_dir_path / "templates.json"
            self.assertFalse(file.exists())

            file.write_text("", encoding="ascii")
            self.assertTrue(file.exists())

            with self.assertRaises(ValueError) as ctx:
                Templates.load(file)
            expected_args = ("text", "")
            actual_args = ctx.exception.args

        self.assertTupleEqual(expected_args, actual_args)

    def test_load_from_existing_file_location_pointing_to_folder(self):
        file = Path.cwd()
        with self.assertRaises(IsADirectoryError) as ctx:
            Templates.load(file)
        expected_args = (file,)
        actual_args = ctx.exception.args
        self.assertTupleEqual(expected_args, actual_args)

    def test_load_from_non_existing_file_location(self):
        with TemporaryDirectory() as temp_dir:
            temp_dir_path = Path(temp_dir)

            file = temp_dir_path / "no_such_file.json"
            self.assertFalse(file.exists())

            with self.assertRaises(FileNotFoundError) as ctx:
                Templates.load(file)
        expected_args = (file,)
        actual_args = ctx.exception.args
        self.assertTupleEqual(expected_args, actual_args)

    def test_load_from_file_with_bad_object_type(self):
        file = object()
        with self.assertRaises(TypeError) as ctx:
            Templates.load(file)  # noqa
        expected_args = ("file", Path, object, file)
        actual_args = ctx.exception.args
        self.assertTupleEqual(expected_args, actual_args)
