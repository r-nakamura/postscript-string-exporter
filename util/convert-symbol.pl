#!/usr/bin/env perl
# 
# 
# Copyright (c) 2018 Ryo Nakamura.
# All rights reserved.
# 
# $Id: convert.pl,v 1.0 2018/04/24 15:56:15 nakamura Exp $
# 

use strict;
use warnings;

use List::MoreUtils qw( any );
use Path::Tiny;

my %SYMBOLE2CHAR = (
  Alpha  => 'A', Beta  => 'B',  Chi   => 'C', Delta   => 'D', Epsilon => 'E',
  Phi    => 'F', Gamma => 'G',  Eta   => 'H', Iota    => 'I', Kappa   => 'K',
  Lambda => 'L', Mu    => 'M',  Nu    => 'N', Omicron => 'O', Pi      => 'P',
  Theta  => 'Q', Rho   => 'R',  Sigma => 'S', Tau     => 'T', Upsilon => 'U',
  Omega  => 'W', Xi    => 'X',  Psi   => 'Y', Zeta    => 'Z',
  alpha  => 'a', beta  => 'b',  chi   => 'c', delta   => 'd', epsilon => 'e',
  phi    => 'f', gamma => 'g',  eta   => 'h', iota    => 'i', kappa   => 'k',
  lambda => 'l', mu    => 'm',  nu    => 'n', omicron => 'o', pi      => 'p',
  theta  => 'q', rho   => 'r',  sigma => 's', tau     => 't', upsilon => 'u',
  omega  => 'w', xi    => 'x',  psi   => 'y', zeta    => 'z',
);

my %ALPHA2SYMBOL = (
  space       => ' ', exclam     => '!',  quotedbl     => '"', numbersign  => '#',
  dollar      => '$', percent    => '%',  ampersand    => '&', quoteright  => '\'',
  parenleft   => '(', parenright => ')',  asterisk     => '*', plus        => '+',
  comma       => ',', hyphen     => '-',  period       => '.', slash       => '/',
  zero        => '0', one        => '1',  two          => '2', three       => '3',
  four        => '4', five       => '5',  six          => '6', seven       => '7',
  eight       => '8', nine       => '9',  colon        => ':', semicolon   => ';',
  less        => '<', equal      => '=',  greater      => '>', question    => '?',
  bracketleft => '[', backslash  => '\\', bracketright => ']', asciicircum => '^',
  underscore  => '_', braceleft  => '{',  bar          => '|', braceright  => '}',
  tilde       => '~',
);

my @chars = (values %SYMBOLE2CHAR, values %ALPHA2SYMBOL);

my $fname = shift or die "usage $0 [afm]";

open my $fh, '<', $fname;

my $db;
while ( <$fh> ) {
    chomp;
    if (/C \d+ ; WX (\d+) ; N ([^\s]+) ; B ([-\d\s]+) ;/) {
        my $char = $2;
           $char = $SYMBOLE2CHAR{$2} if exists $SYMBOLE2CHAR{$2};
           $char = $ALPHA2SYMBOL{$2} if exists $ALPHA2SYMBOL{$2};
        $db->{$char}->{'WX'} = $1;
        $db->{$char}->{'B'}  = $3;
    }
}

close $fh;

my $font = path( $fname )->basename( '.afm' );
   $font =~ s/-/_/;
my $afm = path( $fname )->basename();
my $class = "PostScript::Text::Constants::$font";

print <<"EOF";
#!/usr/bin/python3
# This code was automatically generated from $afm
def symbol2char():
    return {
        'Alpha' : 'A', 'Beta' : 'B', 'Chi'  : 'C', 'Delta'  : 'D', 'Epsilon': 'E',
        'Phi'   : 'F', 'Gamma': 'G', 'Eta'  : 'H', 'Iota'   : 'I', 'Kappa'  : 'K',
        'Lambda': 'L', 'Mu'   : 'M', 'Nu'   : 'N', 'Omicron': 'O', 'Pi'     : 'P',
        'Theta' : 'Q', 'Rho'  : 'R', 'Sigma': 'S', 'Tau'    : 'T', 'Upsilon': 'U',
        'Omega' : 'W', 'Xi'   : 'X', 'Psi'  : 'Y', 'Zeta'   : 'Z',
        'alpha' : 'a', 'beta' : 'b', 'chi'  : 'c', 'delta'  : 'd', 'epsilon': 'e',
        'phi'   : 'f', 'gamma': 'g', 'eta'  : 'h', 'iota'   : 'i', 'kappa'  : 'k',
        'lambda': 'l', 'mu'   : 'm', 'nu'   : 'n', 'omicron': 'o', 'pi'     : 'p',
        'theta' : 'q', 'rho'  : 'r', 'sigma': 's', 'tau'    : 't', 'upsilon': 'u',
        'omega' : 'w', 'xi'   : 'x', 'psi'  : 'y', 'zeta'   : 'z',
    }
EOF

print <<"EOF";
def wx():
    return {
EOF

for my $char ( sort { $a cmp $b } @chars ) {
    next unless exists $db->{$char};
    if ($char eq "'") {
        print "        \"$char\": ", $db->{$char}->{'WX'}, ",\n";
    }
    elsif ($char eq '\\') {
        print "        \'\\\\': ", $db->{$char}->{'WX'}, ",\n";
    }
    else {
        print "        '$char': ", $db->{$char}->{'WX'}, ",\n";
    }
}

print <<"EOF";
    }
EOF

print <<"EOF";
def bounding_box():
    return {
EOF

for my $char ( sort { $a cmp $b } @chars ) {
    next unless exists $db->{$char};
    my $str = join(', ', split /\s+/, $db->{$char}->{'B'});
    if ($char eq "'") {
        print "        \"$char\": [ $str ],\n";
    }
    elsif ($char eq '\\') {
        print "        \'\\\\': [ $str ],\n";
    }
    else {
        print "        '$char': [ $str ],\n";
    }
}

print <<"EOF";
    }
EOF
