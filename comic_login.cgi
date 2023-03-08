#!"C:\xampp\perl\bin\perl.exe"
$web_path	       = 'http://localhost/comic-books';
$comic_data_path = '.';
$comic_menu      = 'http://localhost/comic-books/comic_menu.cgi';

#!/usr/bin/perl
#$web_path        = 'http://www.eskimo.com/~home/comics';
#$comic_data_path = '/u/h/home/public_html/comics';
#$comic_menu      = 'http://www.eskimo.com/~home/cgi-bin/comic_menu.cgi';

#$web_path        = 'http://localhost/comics_web';
#$comic_data_path = '../docs/comics_web';
#$comic_menu      = 'http://localhost/cgi-bin/comic_menu.cgi';

$top = 15;

## Data Types for Sorter
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

read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});

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

print "Content-Type: text/html\n\n";
print "<html>\n";

print "<style type=\"text/css\">\n";
print "#ID_Style_1 {color: white}\n";
print "#ID_Style_2 {font: 9pt}\n";
print "#ID_Style_4 {font: 8pt}\n";
print "H1 {font: 18pt}\n";
print "H2 {font: 16pt}\n";
print "H3 {font: 14pt}\n";
print "TABLE {font: 10pt}\n";
print "TR {vertical-align: top}\n";
print "</style>\n";

print "<head>\n";
print "<title>Statistics</title>\n";
print "</head>\n";

print "<body BGCOLOR=\"FFFFFF\" TEXT=\"000000\" LINK=\"FF0080\" VLINK=\"FF8080\" ALINK=\"FF0000\">";

$login  = $FORM{login};
$passwd = $FORM{passwd};

$users = $comic_data_path . '/' . '.users';
open(F1, "$users");
while (<F1>) {
  chomp;
  @a = split(/\:/);
  if ($login eq $a[0] && $passwd eq $a[1]) {
    $OK = 'T';
  }
}
close(F1);

if ($OK eq 'T') {
  $file = $comic_data_path . '/' . '.' . $login;
  if (-e $file) {
    print "<h2>Collection: <i>$login</i></h2>\n";
    &Banner();
    &Stats();
  }
  else {
    open(F1, ">>$file");
    close(F1);
    print "<h2>Welcome <i>\"$login\"</i></h2>\n";
    print "<h2>A new Database has been created</h2>\n";
    &Banner();
  }
}
else {
  &Reject();
}

print "</body></html>\n";
exit;

sub Banner {
  print "<center><hr>";
  print "<table noborder cellpadding=10>\n";
  print "<tr>\n";
  print "<td><form method=POST action=\"$comic_menu\"><input type=hidden name=help value=$login><input type=submit value=Help></form>";
  print "<td><form method=POST action=\"$comic_menu\"><input type=hidden name=report value=$login><input type=submit value=Report></form>";
  print "<td><form method=POST action=\"$comic_menu\"><input type=hidden name=main value=$login><input type=submit value=Maintenance></form>";
  print "<td><form method=POST action=\"$comic_menu\"><input type=hidden name=back value=$login><input type=submit value=Backup></form>";
  print "</table><hr></center>";
}

sub Reject {
  print "<center><h2>You're Not a Recognized User</h2></center>\n";
  print "<center><h2>Go Back and Check the Form</h2></center>\n";
}


sub Stats {
  ## Read Database: 2000 A.D.|2|Eagle|1|6 issue series|Smith, Ron|Wagner, John|NM|2.00|1||
  open(S1,"$file");
  while (<S1>) {
    chomp;
    push (@comics,$_);
    @r = split(/\|/);
    $exist{"$r[0]|$r[1]|$r[2]|$r[3]|$r[12]"} = '';
    $h_tit{$r[0]}++;
    $h_vol{$r[1]}++;
    $h_pub{$r[2]}++;
    $h_iss{$r[3]}++;
    $h_com{$r[4]}++;
    @artists = split(/\+/,$r[5]);
    foreach $artist (@artists) {
      $h_art{$artist}++;
    }
    @writers = split(/\+/,$r[6]);
    foreach $writer (@writers) {
      $h_wri{$writer}++;
    }
    $h_con{$r[7]}++;
    $h_val{$r[8]}++;
    $h_qua{$r[9]}++;
    $h_mon{$r[10]}++;
    $h_yea{$r[11]}++;
    $h_typ{$r[12]}++;

    $total_count = $total_count + $r[9];
    $total_value = $total_value + ($r[9] * $r[8]);
  }
  close(S1);

  print "<br><table align=center cellpadding=5 noborder>\n";
  print "<tr><td><font size=4>Total Comics Count </font><td><font size=4>$total_count</font>\n";
  print "<tr><td><font size=4>Total Collection Value </font><td><font size=4>\$$total_value</font><br>\n";
  if ($total_count > 0) {
    $avg = $total_value / $total_count;
    $avg = int(($avg * 100) + 0.5)/100;
    print "<tr><td><font size=4>Average Comic Value </font><td><font size=4>\$$avg</font>\n";

  }
  print "</table><br>\n";

  print "<center><table cellpadding=10 border=1>\n";
  print "<tr>\n";

  print "<td><b><u><font size=4>Top $top Titles</font></u></b><br>\n";
  $cnt = 0;
  for (sort { $h_tit{$b} <=> $h_tit{$a} } keys %h_tit) {
    if ($_ ne '') {
      if ($h_tit{$_} == $prev) {
      }
      else {
        $cnt++;
      }
      print "$cnt - $_ (" . $h_tit{$_} . ")<br>\n";
      $prev = $h_tit{$_};
      if ($cnt == $top) {
        goto TIT;
      }
    }
  }
  TIT:

  print "<td align=top><b><u><font size=4>Top $top Writers</font></u></b><br>\n";
  $cnt = 0;
  for (sort { $h_wri{$b} <=> $h_wri{$a} } keys %h_wri) {
    if ($_ ne '') {
      if ($h_wri{$_} == $prev) {
      }
      else {
        $cnt++;
      }
      print "$cnt - $_ (" . $h_wri{$_} . ")<br>\n";
      $prev = $h_wri{$_};
      if ($cnt == $top) {
        goto WRI;
      }
    }
  }
  WRI:

  print "<td><b><u><font size=4>Top $top Artists</font></u></b><br>\n";
  $cnt = 0;
  for (sort { $h_art{$b} <=> $h_art{$a} } keys %h_art) {
    if ($_ ne '') {
      if ($h_art{$_} == $prev) {
      }
      else {
        $cnt++;
      }
      print "$cnt - $_ (" . $h_art{$_} . ")<br>\n";
      $prev = $h_art{$_};
      if ($cnt == $top) {
        goto ART;
      }
    }
  }
  ART:

  @sorted_comics = sort Sorter @comics;
  print "<td><b><u><font size=4>Top $top Values</font></u></b><br>\n";

  $cnt = 0;
  $inx = 0;

  # prevent endless loop if you don't have 15 comics
  #$tcnt = @sorted_comics;
  #if ($tcnt < $top) { $top =  $tcnt; }

  while ($cnt < $top) {
    @t = split(/\|/,$sorted_comics[$inx]);
    if ($t[0] eq "") { $cnt = $top; }
    $inx++;
    if ($t[8] == $prev) {
    }
    else {
      $cnt++;
    }

    if ($t[8] ne '') {
      $issue_num = $t[3] . ' ' . $t[12];
      print "$cnt - \$$t[8] ($t[0] - #$issue_num )<br>\n";
      $prev = $t[8];
    }

  }

  print "</table></center>\n";

}

sub Sorter { 
  @first = split( '\|', $a ); 
  @second = split( '\|', $b ); 

   @sort_order = (8,0);      # fields (month, issue) in ascending order of weights (ie: 1,2)
   @dec_order  = ('D','A');   # respective ascending/descending flag

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


