#!perl -T

use Test::More tests => 1;

BEGIN {
	use_ok( 'Google::AppEngine::Chunker' );
}

diag( "Testing Google::AppEngine::Chunker $Google::AppEngine::Chunker::VERSION, Perl $], $^X" );
