import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_locales_all(host):
    command = host.run('localectl list-locales')
    assert command.stdout.rstrip("^en_US.UTF-8")
    assert command.stdout.rstrip("^nl_BE.UTF-8")


def test_locales_defaultfile(host):
    deflocale = host.file('/etc/locale.conf')
    assert deflocale.exists
    assert deflocale.user == 'root'
    assert deflocale.group == 'root'
    assert deflocale.contains('^LANG="en_US.UTF-8"')


def test_locales_localectl(host):
    command = host.run("localectl status")
    assert command.rc == 0
    assert command.stdout.rstrip("   System Locale: LANG=en_US.UTF-8")
