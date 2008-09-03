use inc::Module::Install;

name 'Google-AppEngine-Chunker';
all_from 'lib/Google/AppEngine/Chunker.pm';

build_requires 'Test::More';

auto_install;

WriteAll;

