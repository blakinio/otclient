from pathlib import Path

probe = (Path(__file__).resolve().parent / 'probe.py').read_text(encoding='utf-8')

for key in (
    'email', 'password', 'stayloggedin', 'type', 'clientversion', 'clienttype',
    'assetversion', 'devicecookie', 'fromtimestamp', 'isreturner',
    'showrewardnews', 'viewedid',
):
    assert repr(key) in probe, key

for marker in (
    "'runtime_access': 'none'",
    "'login_performed': False",
    "'secret_access': False",
    "'raw_client_uploaded': False",
    'CURRENT_LOGINSERVICE_REQUEST_STATIC_PROBE=PASS',
    'candidate_fdes',
    'candidate_snapshots',
):
    assert marker in probe, marker

for forbidden in ('TIBIA_TEST_EMAIL', 'TIBIA_TEST_PASSWORD', 'loginservice.php -d', 'curl --data'):
    assert forbidden not in probe, forbidden

print('CURRENT_LOGINSERVICE_REQUEST_STATIC_CONTRACT=PASS')
