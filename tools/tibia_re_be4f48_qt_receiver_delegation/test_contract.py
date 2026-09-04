import unittest

class Contract(unittest.TestCase):
    def module(self):
        import qt_receiver
        return qt_receiver

    def package(self):
        return {'version':'15.32.be4f48','files':[{'localfile':'bin/client','unpackedhash':'552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1','unpackedsize':52105824,'packedhash':'a'*64,'packedsize':4,'url':'client.lzma'}]}

    def core(self,path='bin/lib/libQt6Core.so.6'):
        return {'localfile':path,'unpackedhash':'b'*64,'unpackedsize':100,'packedhash':'c'*64,'packedsize':4,'url':'core.lzma'}

    def test_one_named_core_selected(self):
        p=self.package();p['files'].append(self.core())
        self.assertEqual(self.module().select_package(p)['qtcore']['localfile'],'bin/lib/libQt6Core.so.6')

    def test_missing_core_is_package_scoped_blocker(self):
        self.assertEqual(self.module().select_package(self.package())['selection_boundary'],'NO_UNIQUE_PACKAGED_QTCORE_MEMBER')

    def test_ambiguous_core_rejected(self):
        p=self.package();p['files'] += [self.core(),self.core('bin/lib/libQt6Core.so.6.10.0')]
        self.assertIsNone(self.module().select_package(p)['qtcore'])

    def test_new_executable_fence_rejected(self):
        p=self.package();p['files'][0]['unpackedhash']='0'*64
        with self.assertRaisesRegex(ValueError,'FENCE'):self.module().select_package(p)

    def test_source_url_cannot_escape_package(self):
        p=self.package();p['files'][0]['url']='../../other'
        with self.assertRaises(ValueError):self.module().select_package(p)

    def test_dependency_hash_mismatch(self):
        with self.assertRaises(ValueError):self.module().verify_member(b'other',self.core())

    def test_only_unique_defined_symbol_is_admitted(self):
        m=self.module()
        with self.assertRaises(ValueError):m.unique_definition([('SHN_UNDEF',0,0)])
        with self.assertRaises(ValueError):m.unique_definition([(1,0x1000,20),(1,0x2000,20)])
        self.assertEqual(m.unique_definition([(1,0x1000,20)]),(0x1000,20))

if __name__=='__main__':unittest.main()
