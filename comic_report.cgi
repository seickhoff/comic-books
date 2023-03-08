#!"C:\xampp\perl\bin\perl.exe"
$comic_data_path = './';
$tamper_log      = './tamper_log.txt';
$script_menu     = 'http://localhost/comic-books/comic_menu.cgi';

#!/usr/bin/perl 
#$comic_data_path = '../comics/';
#$tamper_log      = '../comics/tamper_log.txt';
#$script_menu     = 'http://www.eskimo.com/~home/cgi-bin/comic_menu.cgi';

$time = gmtime() . " GMT";

## $ENV{'CONTENT_LENGTH'}: w_0=2&o_0=A&t_0=&w_2=&o_2=A&t_2=&w_1=&o_1=A&t_1=&w_3=&o_3=A&t_3=&w_10=&o_10=A&t_10=&ch_11=Y&w_11=1&o_11=D&t_11=&w_9=1&o_9=A&t_9=&w_8=&o_8=A&t_8=&w_7=&o_7=A&t_7=&w_6=&o_6=A&t_6=&w_5=&o_5=A&t_5=&w_4=&o_4=A&t_4= 
## 208

if ($ENV{'CONTENT_LENGTH'} <= 640) {
  read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
}
else {
  print "Content-Type: text/plain\n\n";
  open (ERROR,">>$tamper_log");
  print ERROR "$time: $ENV{'REMOTE_ADDR'}, your tampering has been logged. ($ENV{'CONTENT_LENGTH'})\n";
  print "$time: $ENV{'REMOTE_ADDR'}, your tampering has been logged. ($ENV{'CONTENT_LENGTH'})\n";
  exit;
}

##### Split the name-value pairs
@pairs = split(/&/, $buffer);
foreach $pair (@pairs) {
  ($name, $value) = split(/=/, $pair);

  ##### Un-Webify plus signs and %-encoding
  $value =~ tr/+/ /;
  $value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
  $value =~ s/<!--(.|\n)*-->//g;
  $value =~ s/</(/g;
  $value =~ s/>/)/g;
  $value =~ s/\n/ /g;
  $FORM{$name} = $value;
}

if ($FORM{font} < 1 || $FORM{font} > 99) {
  $FORM{font} = '12';
}

$login = $FORM{user};
$comic_data_path .= '.' . $login;

$over = $FORM{os};

for ($index = 0; $index <= 12; $index++) {
  $tmp = 'ch_' . $index;
  $ch[$index] = $FORM{$tmp};           ## Field Selection
  $tmp = 't_' . $index;
  $rtmp = $FORM{$tmp};
  $x[$index]  = &RegExp($rtmp);        ## Reg Expression
  $z[$index]  = $FORM{$tmp};           ## Typed Expression

  $hk = 'w_' . $index;
  $w[$FORM{$hk}] = $index;             ## Sort Weight
  $tmp = 'o_' . $index;
  $o[$index]  = $FORM{$tmp};           ## Sort Direction
}

# Data Types (t)ext, (n)umeric
$type[0] =  't';   # Title
$type[1] =  'n';   # Volume
$type[2] =  't';   # Publisher
$type[3] =  'n';   # Issue
$type[4] =  't';   # Comments
$type[5] =  't';   # Artist
$type[6] =  't';   # Writer
$type[7] =  't';   # Condition
$type[8] =  'n';   # Value
$type[9] =  'n';   # Quantity
$type[10] = 'n';   # Month
$type[11] = 'n';   # Year
$type[12] = 't';   # Issue Type

$name[0] =  'Title';       # Title
$name[1] =  'Volume';      # Volume
$name[2] =  'Publisher';   # Publisher
$name[3] =  'Issue';       # Issue
$name[4] =  'Comments';    # Comments
$name[5] =  'Artist';      # Artist
$name[6] =  'Writer';      # Writer
$name[7] =  'Condition';   # Condition
$name[8] =  'Value';       # Value
$name[9] =  'Quantity';    # Quantity
$name[10] = 'Month';       # Month
$name[11] = 'Year';        # Year
$name[12] = 'Issue Type';  # Issue Type

$count = 0;

print "Content-Type: text/html\n\n";
print "<html>\n";

print "<style type=\"text/css\">\n";
print "TR {vertical-align: top}\n";
print "TD {vertical-align: top}\n";
print "TR {font-size: $FORM{font}pt}\n";
print "TD {font-size: $FORM{font}pt}\n";
print "BODY {font-size: $FORM{font}pt}\n";
print "</style>\n";

print "<head>\n";
print "<title>Report: $time</title>\n";
print "</head>\n";
print "<body BGCOLOR=WHITE TEXT=BLACK ";
print "LINK=\"FF0080\" VLINK=\"FF8080\" ALINK=\"FF0000\">";

if ($ch[0] eq '' && $ch[1] eq '' && $ch[2] eq '' && $ch[3] eq '' && 
    $ch[4] eq '' && $ch[5] eq '' && $ch[6] eq '' && $ch[7] eq '' &&
    $ch[8] eq '' && $ch[9] eq '' && $ch[10] eq '') { 
  $top = 'T'; 
}

$hits = 0;
$pat = 0;

# Any or All
$mt = $FORM{mt};

## Check weights 1-13
for ($ele = 1; $ele <= 13; $ele++) {
  #print "$ele = $w[$ele] <br>\n";
  if ($w[$ele] ne '') {
    push(@sort_order,$w[$ele]);
    $field_names = $field_names . $name[$w[$ele]] . ' (' . $o[$w[$ele]] . ')' . ', '; 
    push(@dec_order,$o[$w[$ele]]);
  }
}
chop $field_names; chop $field_names; 
if (length($field_names) < 2) {
  $field_names = 'unsorted';
}

open(S1,"$comic_data_path");
while (<S1>) {
  chomp;
  push (@comics , $_);
}
close(S1);

@sorted_comics = sort Sorter @comics;

$width = 0;

if ($FORM{"ch_0"} eq 'Y') {  $width = $width + 200;}
if ($FORM{"ch_2"} eq 'Y') {  $width = $width + 100;}
if ($FORM{"ch_1"} eq 'Y') {  $width = $width + 30;}
if ($FORM{"ch_3"} eq 'Y') {  $width = $width + 30; }
if ($FORM{"ch_12"} eq 'Y') {  $width = $width + 30; }
if ($FORM{"ch_10"} eq 'Y') {  $width = $width + 40;}
if ($FORM{"ch_9"} eq 'Y') {  $width = $width + 30;}
if ($FORM{"ch_8"} eq 'Y') {  $width = $width + 30;}
if ($FORM{"ch_7"} eq 'Y') {  $width = $width + 30;}
if ($FORM{"ch_6"} eq 'Y') {  $width = $width +100;}
if ($FORM{"ch_5"} eq 'Y') {  $width = $width + 100;}
if ($FORM{"ch_4"} eq 'Y') {  $width = $width + 250; }

if ($width == 0 ) { $width = 1000; }

foreach $_ (@sorted_comics) {
  $_ =~ s/ /\&nbsp;/g;
  @t = split (/\|/);
  #Alpha Flight|1|Marvel Comics|12|Double size|Byrne, John|Byrne, John|NM|1.50|2|07|1984

  if ($mt eq 'all') {
    $match = 'T';
    for ($fi = 0; $fi <= 12; $fi++) {
      if ($FORM{"t_$fi"} ne '') {
        if (!($t[$fi] =~ m/$x[$fi]/i)) {
          $match = 'F';
        }
      }
    }
  }
  else {
    $match = 'F';
    for ($fi = 0; $fi <= 12; $fi++) {
      if ($FORM{"t_$fi"} ne '') {
        if ($t[$fi] =~ m/$x[$fi]/i) {
          $match = 'T';
        }
      }
    }
  }

  if ($match eq 'T') {
    $count++;
    $pat++;
    if ($over eq 'Y') {
      push (@overstreet, $_);
      $hits++;
      $csum = $csum + $t[9];
      $sum = $sum + ($t[8] * $t[9]);
    }
    else {
      if ($count == 1) {
        &Header;
      }
      &Body;
    }
  }
}


if ($count == 0) {
  print "<br><br><br><br><center>\n";
  print "<h2><b>Nothing Found - Go Back and Try Again</b></h2>\n";
  print "<br>\n";
  print "</center>\n";
}
else {

  if ($over ne 'Y') {
    ## Print Bottom lines after last record
    print "<tr>\n";
    for ($idx = 0; $idx <= 12; $idx++) {
      if ($FORM{"ch_$idx"} eq 'Y') {
        print "<td align=right><hr>\n";
      }
    } 
  }

  $avg = int($sum / $csum * 100) / 100;
  @pr = split (/\./,$avg);
  if (length($pr[1]) == 0) { $avg = $avg . ".00"; }
  if (length($pr[1]) == 1) { $avg = $avg . "0"; }  

  foreach $key (keys(%distinct)) {
    $dcount++;
  }
  
  @pr = split (/\./,$sum);
  if (length($pr[1]) == 0) { $sum = $sum . ".00"; }
  if (length($pr[1]) == 1) { $sum = $sum . "0"; }  

  if ($over eq 'Y') {

    print "<b>$time</b><br>\n";
    print "<b>Collection:</b> <i> $login</i><br><br>\n";
    print "<b>Sorted by:</b> $field_names <br><br>\n";
    print "<b>Matching " . ucfirst($mt) . "</b><br>\n";
    print "<ol>";

    if ($z[0] ne '') {    print "<b>Title: </b>$z[0]<br>\n"; }
    if ($z[2] ne '') {    print "<b>Publisher: </b>$z[2]<br>\n"; }
    if ($z[1] ne '') {    print "<b>Volume: </b>$z[1]<br>\n"; }
    if ($z[3] ne '') {    print "<b>Issue: </b>$z[3]<br>\n"; }
    if ($z[12] ne '') {    print "<b>Issue Type: </b>$z[12]<br>\n"; }
    if ($z[10] ne '') {    print "<b>Month: </b>$z[10]<br>\n"; }
    if ($z[11] ne '') {    print "<b>Year: </b>$z[11]<br>\n"; }
    if ($z[9] ne '') {    print "<b>Quantity: </b>$z[9]<br>\n"; }
    if ($z[8] ne '') {    print "<b>Value: </b>$z[8]<br>\n"; }
    if ($z[7] ne '') {    print "<b>Condition: </b>$z[7]<br>\n"; }
    if ($z[6] ne '') {    print "<b>Writer: </b>$z[6]<br>\n"; }
    if ($z[5] ne '') {    print "<b>Artist: </b>$z[5]<br>\n"; }
    if ($z[4] ne '') {    print "<b>Comments: </b>$z[4]<br>\n"; }
    print "</ol>";
    print "<br>\n";

    &OverStreet();
  }
  else {
    print "</table>\n<br>\n";
  }
  
  print "<table border=0>\n";

  if ($over ne 'Y') {
    print "<tr><td><b>Total Reported:<b><td align=right><b>$dcount</b>\n";
  }
  print "<tr><td><b>Distinct Issues: </b><td align=right><b>$count</b>\n";
  print "<tr><td><b>Total Count: </b><td align=right><b>$csum</b>\n";

  print "<tr><td><b>\&nbsp;</b><td><b>&nbsp;</b>\n";

  print "<tr><td><b>Average Value: </b><td align=right><b>\$$avg</b>\n";
  print "<tr><td><b>Total Value: </b><td align=right><b>\$$sum</b>\n";
  print "</table>\n<br>\n";
}

print "</body>\n";
print "</html>\n";

exit;

sub Header {
    print "<b>$time</b><br>\n";
    print "<b>Collection:</b> <i> $login</i><br><br>\n";
    print "<b>Sorted by:</b> $field_names <br><br>\n";
    print "<b>Matching " . ucfirst($mt) . "</b><br>\n";
    print "<ol>";

    if ($z[0] ne '') {    print "<b>Title: </b>$z[0]<br>\n"; }
    if ($z[2] ne '') {    print "<b>Publisher: </b>$z[2]<br>\n"; }
    if ($z[1] ne '') {    print "<b>Volume: </b>$z[1]<br>\n"; }
    if ($z[3] ne '') {    print "<b>Issue: </b>$z[3]<br>\n"; }
    if ($z[12] ne '') {    print "<b>Issue Type: </b>$z[12]<br>\n"; }
    if ($z[10] ne '') {    print "<b>Month: </b>$z[10]<br>\n"; }
    if ($z[11] ne '') {    print "<b>Year: </b>$z[11]<br>\n"; }
    if ($z[9] ne '') {    print "<b>Quantity: </b>$z[9]<br>\n"; }
    if ($z[8] ne '') {    print "<b>Value: </b>$z[8]<br>\n"; }
    if ($z[7] ne '') {    print "<b>Condition: </b>$z[7]<br>\n"; }
    if ($z[6] ne '') {    print "<b>Writer: </b>$z[6]<br>\n"; }
    if ($z[5] ne '') {    print "<b>Artist: </b>$z[5]<br>\n"; }
    if ($z[4] ne '') {    print "<b>Comments: </b>$z[4]<br>\n"; }
    print "</ol>";
    print "<br>\n";

  print "<table>\n";
  print "<tr align=left>\n";

  if ($FORM{"ch_0"} eq 'Y') {    print "<th align=left>Title\n";               print "<hr>\n";  }
  if ($FORM{"ch_2"} eq 'Y') {    print "<th align=left>Publisher\n";           print "<hr>\n";  }
  if ($FORM{"ch_1"} eq 'Y') {    print "<th align=left>Vol\n";    print "<hr>\n";  }
  if ($FORM{"ch_3"} eq 'Y') {    print "<th align=left>Iss\n";    print "<hr>\n";  }
  if ($FORM{"ch_12"} eq 'Y') {    print "<th align=left>Typ\n";    print "<hr>\n";  }
  if ($FORM{"ch_10"} eq 'Y') {    print "<th align=left>Month\n";  print "<hr>\n";  }
  if ($FORM{"ch_11"} eq 'Y') {    print "<th align=left>Year\n";   print "<hr>\n";  }
  if ($FORM{"ch_9"} eq 'Y') {    print "<th align=left>Qnt\n";    print "<hr>\n";  }
  if ($FORM{"ch_8"} eq 'Y') {    print "<th align=right>Value\n";   print "<hr>\n";  }
  if ($FORM{"ch_7"} eq 'Y') {    print "<th align=center>Cond\n";   print "<hr>\n";  }
  if ($FORM{"ch_6"} eq 'Y') {    print "<th align=left>Writer\n";              print "<hr>\n";  }
  if ($FORM{"ch_5"} eq 'Y') {    print "<th align=left>Artist\n";              print "<hr>\n";  }
  if ($FORM{"ch_4"} eq 'Y') {    print "<th align=left>Comments\n";            print "<hr>\n";  }
}

sub Body {
  $sent = $i + 1;
  $hits++;
  undef $key;

  $csum = $csum + $t[9];
  $sum = $sum + ($t[8] * $t[9]);
 
  for ($idx = 0; $idx <= 12; $idx++) {
    if ($FORM{"ch_$idx"} eq 'Y') {
      $key = $key . $t[$idx] . '|';
    }
  }

  if (!defined($distinct{"$key"})) {
    if ($color == 0) { print "<tr bgcolor=#FFFFFF>\n"; } else { print "<tr bgcolor=#F7F7F7>\n"; }
    $color++;
    if ($color == 2) {
      $color = 0;
    }
    if ($FORM{"ch_0"} eq 'Y') {    if ($t[0] ne '') { print "<td>$t[0]\n"; } else { print "<td>&nbsp;\n"; }  }
    if ($FORM{"ch_2"} eq 'Y') {    if ($t[2] ne '') { print "<td>$t[2]\n"; } else { print "<td>&nbsp;\n"; }  }
    if ($FORM{"ch_1"} eq 'Y') {    if ($t[1] ne '') { print "<td align=center>$t[1]\n"; } else { print "<td>&nbsp;\n"; }  }
    if ($FORM{"ch_3"} eq 'Y') {    if ($t[3] ne '') { print "<td>$t[3]\n"; } else { print "<td>&nbsp;\n"; }  }
    if ($FORM{"ch_12"} eq 'Y') {   if ($t[12] ne '') { print "<td>$t[12]\n"; } else { print "<td>&nbsp;\n"; }  }
    if ($FORM{"ch_10"} eq 'Y') {   if ($t[10] ne '') { print "<td align=center>$t[10]\n"; } else { print "<td>&nbsp;\n"; }  }
    if ($FORM{"ch_11"} eq 'Y') {   if ($t[11] ne '') { print "<td align=center>$t[11]\n"; } else { print "<td>&nbsp;\n"; }  }
    if ($FORM{"ch_9"} eq 'Y') {    if ($t[9] ne '') { print "<td align=center>$t[9]\n"; } else { print "<td>&nbsp;\n"; }  }
    if ($FORM{"ch_8"} eq 'Y') {    if ($t[8] ne '') { print "<td align=right>$t[8]\n"; } else { print "<td>&nbsp;\n"; }  }
    if ($FORM{"ch_7"} eq 'Y') {    if ($t[7] ne '') { print "<td align=center>$t[7]\n"; } else { print "<td>&nbsp;\n"; }  }
    if ($FORM{"ch_6"} eq 'Y') {      
      print "<td>";
      if ($t[6] eq '') { print "&nbsp;"; }
      @writers = split(/\+/,$t[6]);
      foreach $writer (sort @writers) {
        print "$writer<br>";
      }
      print "\n";    
    }
    if ($FORM{"ch_5"} eq 'Y') {   
       print "<td>";
      if ($t[5] eq '') { print "&nbsp;"; }  
      @artists = split(/\+/,$t[5]);
      foreach $artist (sort @artists) {
        print "$artist<br>";
      }
      print "\n";    
    }
    if ($FORM{"ch_4"} eq 'Y') {    if ($t[4] ne '') { print "<td>$t[4]\n"; } else { print "<td>&nbsp;\n"; }  }
  }
  $distinct{"$key"} = '';
}


sub Sorter { 
  @first = split( '\|', $a ); 
  @second = split( '\|', $b ); 

  # @sort_order = (10,3);      # fields (month, issue) in ascending order of weights (ie: 1,2)
  # @dec_order  = ('A','D');   # respective ascending/descending flag

  $f_cnt = @sort_order;        # count

  ## Process all but the last
  for ($item = 0; $item < $f_cnt; $item++) {

    ## Ascending
    if ($dec_order[$item] eq 'A') {
      ## Numeric
      if ($type[$sort_order[$item]] eq 'n') {
        $compare = ( $first[$sort_order[$item]] <=> $second[$sort_order[$item]] ); 
        if ( $compare != 0 ) { return ( $compare ); } 
      }
      ## Text
      else {
        $compare = ( $first[$sort_order[$item]] cmp $second[$sort_order[$item]] ); 
        if ( $compare != 0 ) { return ( $compare ); } 
      }
    }
    ## Descending
    else {
      ## Numeric
      if ($type[$sort_order[$item]] eq 'n') {
        $compare = ( $second[$sort_order[$item]] <=> $first[$sort_order[$item]] ); 
        if ( $compare != 0 ) { return ( $compare ); } 
      }
      ## Text
      else {
        $compare = ( $second[$sort_order[$item]] cmp $first[$sort_order[$item]] ); 
        if ( $compare != 0 ) { return ( $compare ); } 
      }
    }
  }
  
  ## Last one
  ## Ascending
  if ($dec_order[$item] eq 'A') {
    ## Numeric
    if ($type[$sort_order[$f_cnt - 1]] eq 'n') {
      $compare = ( $first[$f_cnt - 1] <=> $second[$f_cnt - 1] ); 
      return ($compare);
    }
    ## Text
    else {
      $compare = ( $first[$f_cnt - 1] cmp $second[$f_cnt - 1] ); 
      return ($compare);
    }
  }
  else {
    ## Numeric
    if ($type[$sort_order[$f_cnt - 1]] eq 'n') {
      $compare = ( $second[$f_cnt - 1] <=> $first[$f_cnt - 1] ); 
      return ($compare);
    }
    ## Text
    else {
      $compare = ( $second[$f_cnt - 1] cmp $first[$f_cnt - 1] ); 
      return ($compare);
    }
  }
}

sub Trim {
  ($field) = @_;
  while ($field =~ /^ / || $field =~ / $/) {
    $field =~ s/^ //;
    $field =~ s/ $//;
  }
  return($field);
}

sub Issues {
  ($st, $end) = @_;
  if ($st == $end) {
    return($st);
  }
  else {
    $t1 = $st . '-' . $end;
    return($t1);
  }
}

sub Dots {
  ($t1, $cnt) = @_;
   $dots = $cnt - length($t1);
   for ($x = 1; $x <= $dots; $x++) {
     $t1 = $t1 . '.';
   }   
   return($t1);
}

sub PreDots {
  ($v1, $cnt) = @_;
   $v1 = '$' . $v1;
   $dots = $cnt - length($v1);
   for ($x = 1; $x <= $dots; $x++) {
     $v1 = '.' . $v1;
   }   
   return($v1);
}

sub OverStreet {

  foreach $_ (@overstreet) {
    @t = split(/\|/);
    $t[12] =~ s/\&nbsp;| /_/g;
    if (defined($ttl{"$t[0]|$t[1]|$t[2]"})) {
      $ele = "$t[3] $t[12]\$$t[8]";
      push (@ovr,$ele);
    }
    else {
      push (@ovr,"<b>$t[0]</b>\n($t[2] - Vol $t[1])");
      $ele = "$t[3] $t[12]\$$t[8]";
      push (@ovr,$ele);
      $ttl{"$t[0]|$t[1]|$t[2]"} = '';
    }
  }

  print "<pre>\n";
  foreach $_ (@ovr) {

    ## Not a Issue/Price
    if (!/\$/) {
      if (defined($start) and defined($end)) {

        ## Prints the LAST issue and any FIRST & ONLY
        $t1 = Issues($start,$end);
        $t1 = Dots($t1,15);
        $v1 = $va[$index];
        $v1 = PreDots($v1,20);
        $t1 =~ s/_/ /g;
        print "$t1$v1\n";;
      }
      if (/\(/) {
        print "\n$_\n";
      }
      $index = 0;
      undef $start;
      undef $end;
    }

    # issue and price
    else {
      $index++;
      ($issue,$value) = split(/\$/);
      $issue = Trim($issue);
      $value = Trim($value);
      $value =~ s/\$//g;

      $is[$index] = Trim($issue);
      $va[$index] = Trim($value);

      # Initialized once
      if (!defined($start)) {
        $start = $issue;
      }

      # consectutive issue, same price
      if ($value == $va[$index-1] and $issue eq ($is[$index-1]+1)) {
        $end = $issue;
      }

      # broken issue continuity or different price
      else {
        $end = $is[$index-1];

        ## Prints the FIRST only if more issue, prints MIDDLE
        if (defined($start) and defined($end)) {
          $t1 = Issues($start,$end);
          $t1 = Dots($t1,15);
          $v1 = $va[$index-1];
          $v1 = PreDots($v1,20);
          $t1 =~ s/_/ /g;
          print "$t1$v1\n";
        }
        $end = $issue;
        $start = $issue;
      }
    }
  }

  ## Prints the very LAST issue
  if (defined($start) and defined($end)) {
    $t1 = Issues($start,$end);
    $t1 = Dots($t1,15);
    $v1 = $va[$index];
    $v1 = PreDots($v1,20);
    $t1 =~ s/_/ /g;
    print "$t1$v1\n";
  }
  print "</pre>\n";
}

sub RegExp {
  $handl = $_[0];

  $handl =~ s/\./\\\./g;     ## '.' (period) matches are allowed
  $handl =~ s/\(/\\(/g;      ## '(' matches are allowed
  $handl =~ s/\)/\\)/g;      ## ')' matches are allowed

  $handl =~ s/ or /\|/g;    ## ' or ' allows alternate matches
  $handl =~ s/{/^/g;        ## '{' is a leftmost boundary
  $handl =~ s/}/\$/g;       ## '}' is a rightmost boundary
  $handl =~ s/\?/./g;       ## '?' is a one-character wildcard
  $handl =~ s/\*/.*/g;      ## '*' is a one-or-many wildcard
  return($handl);
}
