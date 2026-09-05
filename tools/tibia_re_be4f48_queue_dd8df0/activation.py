"""Bounded queue activation argument proof; repository-only RED scaffold."""
ACTIVATE = '_ZN11QMetaObject8activateEP7QObjectPKS_iPPv'

def qualify_tail(raw, site, target):
    raise NotImplementedError('RED: exact tail kind qualification')

def project(raw, base, entry=None, max_instructions=128):
    raise NotImplementedError('RED: first-transfer argument projection')

def classify(flow, symbol):
    raise NotImplementedError('RED: exact activation import and argument contract')
