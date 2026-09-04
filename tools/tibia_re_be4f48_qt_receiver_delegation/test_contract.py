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

    def test_reused_flow_rejects_non64_stack_operation(self):
        from static_flow import trace_paths
        with self.assertRaises(ValueError):trace_paths(bytes.fromhex('576650585fc3'),0x1000)

    def test_reused_flow_rejects_pop_rsp(self):
        from static_flow import trace_paths
        with self.assertRaises(ValueError):trace_paths(bytes.fromhex('505cc3'),0x1000)

    def test_unresolved_callee_is_not_positive_delegation(self):
        m=self.module()
        self.assertFalse(m.resolved_delegation(True,[{'target':'UNKNOWN'}]))
        self.assertFalse(m.resolved_delegation(False,[{'target':'0x1234'}]))
        self.assertTrue(m.resolved_delegation(True,[{'target':'0x1234'}]))

    def test_dependency_elf_identity(self):
        m=self.module()
        m.qualify_core_identity(64,'EM_X86_64',['libQt6Core.so.6'],'STT_FUNC')
        for v in [(32,'EM_X86_64',['libQt6Core.so.6'],'STT_FUNC'),(64,'EM_AARCH64',['libQt6Core.so.6'],'STT_FUNC'),(64,'EM_X86_64',['libOther.so'],'STT_FUNC'),(64,'EM_X86_64',['libQt6Core.so.6'],'STT_OBJECT')]:
            with self.assertRaises(ValueError):m.qualify_core_identity(*v)

    def test_external_conditional_frontier_is_explicit(self):
        from static_flow import trace_paths
        p=trace_paths(bytes.fromhex('85c07510c3'),0x1000,{'rcx':'registered:receiver'})
        self.assertEqual(p['incomplete_boundaries'][0]['site'],'0x1002')
        self.assertEqual(p['incomplete_boundaries'][0]['target'],'0x1014')
        self.assertTrue(self.module().only_external_branches(p))

    def test_loop_is_not_external_source_blocker(self):
        from static_flow import trace_paths
        p=trace_paths(bytes.fromhex('ebfe'),0x1000)
        self.assertFalse(self.module().only_external_branches(p))

    def test_dependency_discovery_does_not_allow_silent_change(self):
        with self.assertRaisesRegex(ValueError,'FENCE'):self.module().qualify_dependency_fence(self.core())

    def test_internal_undecoded_branch_is_not_external_boundary(self):
        from static_flow import trace_paths
        p=trace_paths(bytes.fromhex('85c075fdc3'),0x1000)
        self.assertFalse(self.module().only_external_branches(p))
        self.assertEqual(p['incomplete_boundaries'][0]['kind'],'UNDECODED_INTERNAL_BRANCH')

    def test_internal_undecoded_jump_is_incomplete(self):
        from static_flow import trace_paths
        p=trace_paths(bytes.fromhex('ebffc3'),0x1000)
        self.assertFalse(p['complete'])

    def test_receiver_fixedpoint_closes_identity_preserving_loop(self):
        from receiver_flow import receiver_flow
        # mov rbx,rcx; test eax,eax; jne back to test; mov rcx,rbx; call0x2000;ret
        p=receiver_flow(bytes.fromhex('4889cb85c075fc4889d9e8f10f0000c3'),0x1000)
        self.assertTrue(p['fixedpoint_reached'])
        self.assertEqual(p['receiver_delegations'][0]['receiver_argument_registers'],['rcx'])

    def test_receiver_fixedpoint_joins_clobbering_path(self):
        from receiver_flow import receiver_flow
        # optional xor ebx,ebx on loop, so final rbxbased copy is not proven.
        p=receiver_flow(bytes.fromhex('4889cb85c0740431dbebf84889d9e8ee0f0000c3'),0x1000)
        self.assertEqual(p['receiver_delegations'],[])

    def test_receiver_fixedpoint_call_clobbers_volatile_source(self):
        from receiver_flow import receiver_flow
        p=receiver_flow(bytes.fromhex('e800000000e800000000c3'),0x1000)
        self.assertEqual(len(p['receiver_delegations']),1)

    def test_receiver_fixedpoint_does_not_invent_memory_identity(self):
        from receiver_flow import receiver_flow
        p=receiver_flow(bytes.fromhex('488b0fe800000000c3'),0x1000)
        self.assertEqual(p['receiver_delegations'],[])

    def test_receiver_fixedpoint_fallthrough_is_not_source_boundary(self):
        from receiver_flow import receiver_flow
        p=receiver_flow(bytes.fromhex('4889cb'),0x1000)
        self.assertFalse(self.module().only_external_branches(p))

    def test_receiver_fixedpoint_push_invalidates_overlapping_slot(self):
        from receiver_flow import receiver_flow
        p=receiver_flow(bytes.fromhex('48894c24fc50488b4c2404e800000000c3'),0x1000)
        self.assertEqual(p['receiver_delegations'],[])

    def test_unconditional_scope_exit_is_not_labelled_conditional(self):
        from receiver_flow import receiver_flow
        p=receiver_flow(bytes.fromhex('eb10'),0x1000)
        self.assertIs(p['incomplete_boundaries'][0]['taken'],True)

if __name__=='__main__':unittest.main()
