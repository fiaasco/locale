import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_locales_file(host):
    locale = host.file('/etc/locale.gen')
    assert locale.exists
    assert locale.user == 'root'
    assert locale.group == 'root'
    assert locale.contains('^en_US.UTF-8')
    assert locale.contains('^nl_BE.UTF-8')


def test_locales_defaultfile(host):
    deflocale = host.file('/etc/default/locale')
    assert deflocale.exists
    assert deflocale.user == 'root'
    assert deflocale.group == 'root'
    assert deflocale.contains('^LANG=nl_BE.UTF-8')


def test_locales_localectl(host):
    command = host.run("localectl status")
    assert command.rc == 0
    assert command.stdout.rstrip("   System Locale: LANG=nl_BE.UTF-8")
