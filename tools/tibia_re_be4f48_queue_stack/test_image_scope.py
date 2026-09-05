"""The stack task must not resolve any relocation/import metadata."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import static_flow


class ForbiddenRelocation(dict):
    def __init__(self):
        super().__init__(sh_addr=0, sh_size=0, sh_offset=0, sh_flags=0, sh_link=0)

    def iter_relocations(self):
        raise AssertionError('FORBIDDEN_IMPORT_METADATA_TRAVERSAL')


class SectionAndFdeOnly:
    def iter_sections(self):
        return iter([ForbiddenRelocation()])

    def get_section(self, _):
        raise AssertionError('FORBIDDEN_LINKED_SYMBOL_TABLE_READ')

    def get_dwarf_info(self, **kwargs):
        assert kwargs.get('relocate_dwarf_sections') is False
        return self

    def EH_CFI_entries(self):
        return []


class ImageScopeContract(unittest.TestCase):
    def test_image_initialization_never_traverses_relocations(self):
        with tempfile.TemporaryDirectory() as root:
            path = Path(root) / 'synthetic'
            path.write_bytes(b'synthetic fixture')
            with patch.object(static_flow, 'ELFFile', return_value=SectionAndFdeOnly()), \
                    patch.object(static_flow, 'RelocationSection', ForbiddenRelocation, create=True):
                image = static_flow.Image(path)
                image.close()


if __name__ == '__main__':
    unittest.main()
