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

my @chars = qw(
    a b c d e f g h i j k l m o n p q r s t u v w x y z
    A B C D E F G H I J K L M O N P Q R S T U V W X Y Z
);
push @chars, values %ALPHA2SYMBOL;

my $fname = shift or die "usage $0 [afm]";

open my $fh, '<', $fname;

my $db;
while ( <$fh> ) {
    chomp;
    if (/C \d+ ; WX (\d+) ; N ([^\s]+) ; B ([-\d\s]+) ;/) {
        my $char = exists $ALPHA2SYMBOL{$2} ? $ALPHA2SYMBOL{$2} : $2;
        if ( any { $char eq $_ } @chars ) {
            $db->{$char}->{'WX'} = $1;
            $db->{$char}->{'B'}  = $3;
        }
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
