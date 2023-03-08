#!"C:\xampp\perl\bin\perl.exe"
$web_path        = 'http://localhost/comic-books';
$comic_data_path = './';
$script          = 'http://localhost/comic-books/comic_main.cgi';
$script_menu     = 'http://localhost/comic-books/comic_menu.cgi';

#!/usr/bin/perl
#$web_path        = 'http://www.eskimo.com/~home/comics';
#$comic_data_path = '../comics/';
#$script          = 'http://www.eskimo.com/~home/cgi-bin/comic_main.cgi';
#$script_menu     = 'http://www.eskimo.com/~home/cgi-bin/comic_menu.cgi';

$extra = '0';
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

$login = $FORM{user};

if ($login eq '') {
  &Stop();
}

$comic_data_path .= '.' . $login;

$banner .= "<center><hr>";
$banner .= "<table noborder cellpadding=10>";
$banner .= "<tr>";
$banner .= "<td><form method=POST action=\"$script_menu\"><input type=hidden name=help value=$login><input type=submit value=Help></form>";
$banner .= "<td><form method=POST action=\"$script_menu\"><input type=hidden name=report value=$login><input type=submit value=Report></form>";
$banner .= "<td><form method=POST action=\"$script_menu\"><input type=hidden name=main value=$login><input type=submit value=Maintenance></form>";
$banner .= "<td><form method=POST action=\"$script_menu\"><input type=hidden name=back value=$login><input type=submit value=Backup></form>";
$banner .= "</table><hr></center>";

$l_cnt = 20; ## Set the max number of records to display
$s_cnt = $FORM{'count'} + 1;
$e_cnt = $FORM{'count'} + $l_cnt;
$add_modifier = $e_cnt;
if ($FORM{type} eq 'Delete' || $FORM{type} eq 'Modify') {
  $s_cnt = 1;
  $e_cnt = 100;
} 
$count = 0;                ## Record Count

for ($index = 0; $index <= 12; $index++) {       ## Var   Form Var Name
  $ch[$index] = $FORM{"ch_$index"};              ## @ch : ch_[0..11] Y/null, Field Sel Checkbox
  $x[$index]  = &RegExp($FORM{"t_$index"});      ## @x  : t_[0..11]  text, Fixed Reg Expression
  $z[$index]  = $FORM{"t_$index"};               ## @z  : t_[0..11]  text, Typed Search Expression
  
  $hk = 'w_' . $index;
  if ($FORM{$hk} ne '') {
    $w[$FORM{$hk}] = $index;                     ## @w  : w_[0..11]  null,1..12, Field Sort Weight
  }
  $o[$index]  = $FORM{"o_$index"};               ## @o  : o_[0..11]  A/D, Sort Direction
}

$group = $FORM{'gu'};                            ## Group
if (defined($FORM{pattern1})) {                  ## If Group search data, use its data
  @z = split(/\|/,$FORM{pattern1});              ## @z  : pattern1, text, Typed Search Expression
  @x = split(/\|/,$FORM{pattern1});              ## @x  : pattern1, text, Fixed Reg Expression
  @w = split(/\|/,$FORM{pattern2});              ## @w  : pattern2, [0-11], Fields in order by Weight
  @o = split(/\|/,$FORM{pattern3});              ## @o  : pattern3, A/D, Sort Direction
  for ($index = 0; $index <= 12; $index++) { 
    $x[$index] = &RegExp($x[$index]);
  }   
}

$mt = $FORM{mt};                                 ## Any or All

$type = $FORM{type};
if    ($group eq 'G') { $type = 'group'; }       ## Three Types: $type = group, add, mod, first
elsif ($group eq 'A') { $type = 'add'; }    
elsif ($group eq 'X') { $type = 'group_add'; }   
elsif ($group eq 'D') { $type = 'group_del'; }   

$tit = $FORM{'title'};          ## FORM: Add New Record / Group Update the Above Records
$iss = $FORM{'issue'};
$typ = $FORM{'itype'};
$vol = $FORM{'volume'};
$pub = $FORM{'publisher'};
$art = $FORM{'artist'};
$wri = $FORM{'writer'};
$qua = $FORM{'quantity'};
$con = $FORM{'condition'};
$val = $FORM{'value'};
$yea = $FORM{'year'};
$mon = $FORM{'month'};
$com = $FORM{'comments'};

if ($FORM{'title2'} ne '') { $tit = $FORM{'title2'}; }
if ($FORM{'issue2'} ne '') { $iss = $FORM{'issue2'}; }
if ($FORM{'itype2'} ne '') { $typ = $FORM{'itype2'}; }
if ($FORM{'volume2'} ne '') { $vol = $FORM{'volume2'}; }
if ($FORM{'publisher2'} ne '') { $pub = $FORM{'publisher2'}; }
if ($FORM{'artist2'} ne '') { $art = $FORM{'artist2'}; }
if ($FORM{'writer2'} ne '') { $wri = $FORM{'writer2'}; }
if ($FORM{'quantity2'} ne '') { $qua = $FORM{'quantity2'}; }
if ($FORM{'condition2'} ne '') { $con = $FORM{'condition2'}; }
if ($FORM{'value2'} ne '') { $val = $FORM{'value2'}; }
if ($FORM{'month2'} ne '') { $mon = $FORM{'month2'}; }
if ($FORM{'year2'} ne '') { $yea = $FORM{'year2'}; }
if ($FORM{'comments2'} ne '') { $com = $FORM{'comments2'}; }

$new_comic = "$tit|$vol|$pub|$iss|$com|$art|$wri|$con|$val|$qua|$mon|$yea|$typ";
$new_key =   "$tit|$vol|$pub|$iss|$typ";

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
$type[12] =  't';   # Type

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


print "Content-Type: text/html\n\n";
print "<html>\n";

print "<style type=\"text/css\">\n";
print "#ID_Style_1 {color: white}\n";
print "#ID_Style_2 {font: $FORM{font}pt}\n";
print "TR {vertical-align: top}\n";
print "TD {font-size: $FORM{font}pt}\n";
print "TR {font-size: $FORM{font}pt}\n";
print "TABLE {font-size: $FORM{font}pt}\n";
print "TH {font-size: $FORM{font}pt}\n";
print "BODY {font-size: $FORM{font}pt}\n";
print "H1 {font-size: 18pt}\n";
print "H2 {font: 16pt}\n";
print "H3 {font: 14pt}\n";
print "</style>\n";

print "<head>\n";
print "<title>Maintenance</title>\n";
print "</head>\n";

print "<body id=ID_Style_2>";

#foreach $ele (sort(%ENV)) {
#  print "$ele = $ENV{$ele}<br>\n";
#}

## Security
if ($ENV{'REMOTE_USER'} eq 'guest') {
  print "<br><br><br><br>\n";
  print "<center><h1><i>The user 'guest' is not authorized ";
  print "to add records!</i></h1></center>\n";
  print "</body>\n";
  print "</html>\n";
  exit;
}

# First ----------------------------------------------------------------------------
if ($type eq 'first' || $type eq 'More') {
  &ReadData();
}

# ADD ----------------------------------------------------------------------------
if ($type eq 'add') {

  &Validate($new_comic);

  $hits = 0;
  $pat = 0;

  &ReadData();

  ## New Comic not a Duplicate
  if (!defined($exist{"$new_key"})) {
    open (N1,">>$comic_data_path");
    print N1 "$new_comic\n";
    close (N1);
    push (@comics, $new_comic);
    push (@msg, "<b>Added:</b><i> $tit ($pub); Vol $vol; Issue $iss $typ</i>\n");
  }
  ## Duplicate
  else {
    push (@msg, "<b>Duplicate Ignored:</b><i> $tit ($pub); Vol $vol; Issue $iss $typ</i>\n");
  }
}

# GROUP ADD ----------------------------------------------------------------------------
if ($type eq 'group_add') {

  $start1 = $FORM{'gi'};  # Issue Start
  $start2 = $FORM{'gm'};  # Month Start
  $start3 = $FORM{'gy'};  # Year Start
  $start4 = $FORM{'ge'};  # Issue End

  if ($start1 > $start4) {
    $inv = "Y";
    print "<br><br><center><h2>Ending Issue must be larger than Starting Issue</h2>\n";
    print "<br><h2>Go Back and complete the Form</h2></center>\n";
    print "</body>\n";
    print "</html>\n";
    exit;
  }

  $hits = 0;
  $pat = 0;

  &ReadData();

  for ($issue_loop = $start1; $issue_loop <= $start4; $issue_loop++) {

    if (length($start2) == 1) {
      $start2 = "0$start2";
    } 

    $new_comic = "$tit|$vol|$pub|$issue_loop|$com|$art|$wri|$con|$val|$qua|$start2|$start3|$typ";
    $new_key =   "$tit|$vol|$pub|$issue_loop|$typ";

    &Validate($new_comic);

    ## New Comic not a Duplicate
    if (!defined($exist{"$new_key"})) {
      open (N1,">>$comic_data_path");
      print N1 "$new_comic\n";
      close (N1);
      push (@comics, $new_comic);
      push (@msg, "<b>Added:</b><i> $tit ($pub); Vol $vol; Issue $issue_loop $typ</i><br>\n");
    }
    ## Duplicate
    else {
      push (@msg, "<b>Duplicate Ignored:</b><i> $tit ($pub); Vol $vol; Issue $issue_loop $typ</i><br>\n");
    }

    ## Adjust year
    $start2++;
    if ($start2 == 13) {
      $start3++;  $start2 = 1;
    }
  }
}

## GROUP DELETE ----------------------------------------------------------------------
if ($type eq 'group_del') {

  &ReadData();

  ## Write @comic to keep.txt, but 
  open (N1,">$comic_data_path");
  foreach $ele (@comics) {
    @t = split(/\|/,$ele);

    $match = &Matcher();

    if ($match eq 'F') {
      print N1 "$ele\n";      
      push (@comics2 , $ele);
    }
    else {
      push (@msg, "<b>Deleted:</b> <i>$t[0] ($r[2]); Vol $t[1]; Issue $t[3] $t[12]</i><br>\n");
    }
  }
  close(N1);
  @comics = @comics2;
}


## GROUP ----------------------------------------------------------------------
if ($type eq 'group') {

  &ReadData();

  $start1 = $FORM{gi};
  $start2 = $FORM{gm};
  $start3 = $FORM{gy};

  ## Perform sort if range data
  if ($FORM{gi} ne '' || $FORM{gm} ne '' || $FORM{gy} ne '') {
    ## Set Arrays for sorting
    for ($ele = 0; $ele <= 13; $ele++) {
      if ($w[$ele] ne '') {
        push(@sort_order,$w[$ele]);          # pattern2 value="|0|2|1|3|10|11|9|8|7|6|5|"
        push(@dec_order,$o[$w[$ele]]);       # pattern3 value="D|D|D|D|D|D|D|D|D|D|D|D|"
      }
    }
  }
  @sorted_comics = sort Sorter @comics;

  ## Write @comic to keep.txt, but include group update data
  open (N1,">$comic_data_path");
  foreach $ele (@sorted_comics) {
    @t = split(/\|/,$ele);

    $match = &Matcher();

    if ($match eq 'T') {
      if ($tit ne '') { $t[0] = $tit; }
      if ($vol ne '') { $t[1] = $vol; }
      if ($pub ne '') { $t[2] = $pub; }

      if ($iss ne '') { $t[3] = $iss; }
      if ($start1 ne '') {                       ## Issue Range Update
        $t[3] = $start1; 
        $start1++;        
      }

      if ($com ne '') { $t[4] = $com; }
      if ($art ne '') { $t[5] = $art; }
      if ($wri ne '') { $t[6] = $wri; }
      if ($con ne '') { $t[7] = $con; }
      if ($val ne '') { $t[8] = $val; }
      if ($qua ne '') { $t[9] = $qua; }

      if ($mon ne '') { $t[10] = $mon; }
      if ($start2 == 13) {
        $start3++;  $start2 = 1;
      }
      if ($start2 ne '') {                        ## Month Range update
        $t[10] = $start2; 
        if (length($t[10]) == 1) {
          $t[10] = "0$t[10]";
        } 
        $start2++;        
      }

      if ($yea ne '') { $t[11] = $yea; }
      if ($start3 ne '') {                        ## Year Range update
        $t[11] = $start3;      
      }

      if ($typ ne '') { $t[12] = $typ; }

      $new_comic = "$t[0]|$t[1]|$t[2]|$t[3]|$t[4]|$t[5]|$t[6]|$t[7]|$t[8]|$t[9]|$t[10]|$t[11]|$t[12]";
      push (@comics2 , $new_comic);
      print N1 "$new_comic\n";
    }
    else {
      push (@comics2 , $ele);
      print N1 "$ele\n";
    }  
  }
  close (N1);

  @comics = @comics2;
  undef @comics2;
}

## PERFORM MOD/DELETE FUNCTIONS ----------------------------------------------------------
if ($type eq 'Submit' || $type eq 'Delete') {

  $mod_comic = "$tit|$vol|$pub|$iss|$com|$art|$wri|$con|$val|$qua|$mon|$yea|$typ";

  ## Form the KEY for record to DELETE
  if ($type eq 'Delete') {
    @d = split (/\|/, $FORM{raw});
    $del_key = "$d[0]|$d[1]|$d[2]|$d[3]|$d[12]";
    $d_flag = 'Y';

    ## Incomplete Data Entered
    if ($FORM{raw} eq '') {
      print "<br><br><center><h2>";
      print "Go Back and Select a Comic</h2></center>\n";
      print "</body>\n";
      print "</html>\n";
      exit;
    }

  }
  ## Key of comic before a Mod
  if ($type eq 'Submit') {
    &Validate($mod_comic);
    @d = split (/\|/, $FORM{raw});
    $mod_key = "$d[0]|$d[1]|$d[2]|$d[3]|$d[12]";
    $m_flag = 'Y';
  }

  ## Read Database: 2000 A.D.|2|Eagle|1|6 issue series|Smith, Ron|Wagner, John|NM|2.00|1||
  open(S1,"$comic_data_path");
  while (<S1>) {
    chomp;

    @r = split(/\|/);
    $key = "$r[0]|$r[1]|$r[2]|$r[3]|$r[12]";

    ## Skip over record for a DELETE or MOD
    if ($key eq $del_key || $key eq $mod_key) {


      if ($type eq 'Delete') {
        push (@msg, "<b>Deleted:</b> <i>$r[0] ($r[2]); Vol $r[1]; Issue $r[3] $r[12]</i><br>\n");
      }
      if ($type eq 'Submit') {
        push (@msg, "<b>Modified:</b> <i>$r[0] ($r[2]); Vol $r[1]; Issue $r[3] $r[12]</i><br>\n");
      }
    }
    else {
      push (@comics, $_);
    }
  }
  if ($m_flag eq 'Y') {
    push (@comics, $mod_comic);
  }

  close(S1);

  $count = 0;

  $hits = 0;
  $pat = 0;

  open (NEW,">$comic_data_path");
  foreach $_ (@comics) {
    print NEW "$_\n";
  }
  close (NEW);
}


## MOD --------------------------------------------------------------------------------
if ($type eq 'Modify') {

  &ReadData();
  print "$banner";
  $mod = $FORM{'raw'};

  ## Incomplete Data Entered
  if ($mod eq '') {
    print "<br><br><center><h2>";
    print "Go Back and Select a Comic</h2></center>\n";
    print "</body>\n";
    print "</html>\n";
    exit;
  }

  @rec = split (/\|/,$mod);

  print "<center><h2>Modify the record below:</h2></center>\n";

  print "<center><form method=POST action=\"$script\">\n";
  print "<table border=0 id=ID_Style_2>\n";

  if ($FORM{basic} eq 'Y') {

    print "<tr>\n";
    print "<th align=left>\n";
    print "<th align=left>Enter new comic book details below.";

    print "<tr>\n";
    print "<th align=left>Title:\n";
    print "<th align=left><input type=\"text\" name=title size=40 ";
    print "maxlength=50 value=\"$rec[0]\">\n";

    print "<tr>\n";
    print "<th align=left>Publisher:\n";
    print "<th align=left><input type=\"text\" name=publisher size=40 maxlength=40 value=\"$rec[2]\">\n";

    print "<tr>\n";
    print "<th align=left>Volume:\n";
    print "<th align=left><input type=\"text\" name=volume size=2 maxlength=2 value=\"$rec[1]\">\n";

    print "<tr>\n";
    print "<th align=left>Issue Type:\n";
    print "<th align=left><input type=\"text\" name=itype size=9 maxlength=9 value=\"$rec[12]\">\n";

    print "<tr>\n";
    print "<th align=left>Issue:\n";
    print "<th align=left><input type=\"text\" name=issue size=6 maxlength=6 value=\"$rec[3]\">\n";

    print "<tr>\n";
    print "<th align=left>Month:\n";
    print "<th align=left><input type=\"text\" name=month size=2 maxlength=2 value=\"$rec[10]\">\n";

    print "<tr>\n";
    print "<th align=left>Year:\n";
    print "<th align=left><input type=\"text\" name=year size=4 maxlength=4 value=\"$rec[11]\">\n";

    print "<tr>\n";
    print "<th align=left>Quantity:\n";
    print "<th align=left><input type=\"text\" name=quantity size=3 maxlength=3 value=\"$rec[9]\">\n";

    print "<tr>\n";
    print "<th align=left>Value:\n";
    print "<th align=left><input type=\"text\" name=value size=6 maxlength=6 value=\"$rec[8]\">\n";

    print "<tr>\n";
    print "<th align=left>Condition:\n";
    print "<th align=left><input type=\"text\" name=condition size=2 maxlength=2 value=\"$rec[7]\">\n";

    print "<tr>\n";
    print "<td align=left><b>Writer:</b> (optional)\n";
    print "<td align=left><input type=\"text\" name=writer size=40 maxlength=60 value=\"$rec[6]\">\n";

    print "<tr>\n";
    print "<td align=left><b>Artist:</b> (optional)\n";
    print "<td align=left><input type=\"text\" name=artist size=40 maxlength=60 value=\"$rec[5]\">\n";

    print "<tr>\n";
    print "<td align=left><b>Comments:</b> (optional)\n";
    print "<td align=left><input type=\"text\" name=comments size=40 maxlength=60 value=\"$rec[4]\">\n";
  }
  else {

    print "<tr>\n";
    print "<th align=left>\n";
    print "<th align=left>Enter new comic book details below.";
    print "<th align=left>Select from existing data (overrides any typed data).";

    print "<tr>\n";
    print "<th align=left>Title:\n";
    print "<th align=left><input type=\"text\" name=title size=40 ";
    print "maxlength=50 value=\"$rec[0]\">\n";
    print "<th align=left><select name=\"title2\">\n";
    foreach $el (sort keys(%h_tit)) {
      print "<option>$el\n";
    }
    print "</select>\n";

    print "<tr>\n";
    print "<th align=left>Publisher:\n";
    print "<th align=left><input type=\"text\" name=publisher size=40 maxlength=40 value=\"$rec[2]\">\n";
    print "<th align=left><select name=\"publisher2\">\n";
    foreach $el (sort keys(%h_pub)) {
      print "<option>$el\n";
    }

    print "<tr>\n";
    print "<th align=left>Volume:\n";
    print "<th align=left><input type=\"text\" name=volume size=2 maxlength=2 value=\"$rec[1]\">\n";
    print "<th align=left><select name=\"volume2\">\n";
    foreach $el (sort {$a <=> $b} keys(%h_vol)) {
      print "<option>$el\n";
    }
    print "<tr>\n";
    print "<th align=left>Issue Type:\n";
    print "<th align=left><input type=\"text\" name=itype size=9 maxlength=9 value=\"$rec[12]\">\n";
    print "<th align=left><select name=\"itype2\">\n";
    foreach $el (sort keys(%h_typ)) {
      print "<option>$el\n";
    }
    print "<tr>\n";
    print "<th align=left>Issue:\n";
    print "<th align=left><input type=\"text\" name=issue size=12 maxlength=12 value=\"$rec[3]\">\n";
    print "<th align=left><select name=\"issue2\">\n";
    foreach $el (sort {$a <=> $b} keys(%h_iss)) {
      print "<option>$el\n";
    }
    print "<tr>\n";
    print "<th align=left>Month:\n";
    print "<th align=left><input type=\"text\" name=month size=2 maxlength=2 value=\"$rec[10]\">\n";
    print "<th align=left><select name=\"month2\">\n";
    foreach $el (sort {$a <=> $b} keys(%h_mon)) {
      print "<option>$el\n";
    }

    print "<tr>\n";
    print "<th align=left>Year:\n";
    print "<th align=left><input type=\"text\" name=year size=4 maxlength=4 value=\"$rec[11]\">\n";
    print "<th align=left><select name=\"year2\">\n";
    foreach $el (sort {$a <=> $b} keys(%h_yea)) {
      print "<option>$el\n";
    }

    print "<tr>\n";
    print "<th align=left>Quantity:\n";
    print "<th align=left><input type=\"text\" name=quantity size=3 maxlength=3 value=\"$rec[9]\">\n";
    print "<th align=left><select name=\"quantity2\">\n";
    foreach $el (sort {$a <=> $b} keys(%h_qua)) {
      print "<option>$el\n";
    }

    print "<tr>\n";
    print "<th align=left>Value:\n";
    print "<th align=left><input type=\"text\" name=value size=6 maxlength=6 value=\"$rec[8]\">\n";
    print "<th align=left><select name=\"value2\">\n";
    foreach $el (sort {$a <=> $b} keys(%h_val)) {
      print "<option>$el\n";
    }

    print "<tr>\n";
    print "<th align=left>Condition:\n";
    print "<th align=left><input type=\"text\" name=condition size=2 maxlength=2 value=\"$rec[7]\">\n";
    print "<th align=left><select name=\"condition2\">\n";
    foreach $el (sort keys(%h_con)) {
      print "<option>$el\n";
    }

    print "<tr>\n";
    print "<td align=left><b>Writer:</b> (optional)\n";
    print "<td align=left><input type=\"text\" name=writer size=40 maxlength=60 value=\"$rec[6]\">\n";
    print "<td align=left><select name=\"writer2\">\n";
    foreach $el (sort keys(%h_wri)) {
      print "<option>$el\n";
    }
    print "</select>\n";

    print "<tr>\n";
    print "<td align=left><b>Artist:</b> (optional)\n";
    print "<td align=left><input type=\"text\" name=artist size=40 maxlength=60 value=\"$rec[5]\">\n";
    print "<td align=left><select name=\"artist2\">\n";
    foreach $el (sort keys(%h_art)) {
      print "<option>$el\n";
    }
    print "</select>\n";

    print "<tr>\n";
    print "<td align=left><b>Comments:</b> (optional)\n";
    print "<td align=left><input type=\"text\" name=comments size=40 maxlength=60 value=\"$rec[4]\">\n";
    print "<th align=left><select name=\"comments2\">\n";
    foreach $el (sort keys(%h_com)) {
      print "<option>$el\n";
    }
  }

  ## Recontruct match strings for group/add form
  for ($idx = 0; $idx <= 12; $idx++) {
    $str1 = $str1 . $z[$idx] . '|';
    $str2 = $str2 . $w[$idx] . '|';
    $str3 = $str3 . $o[$idx] . '|';
  }

  print "</table>\n";
  print "<br><input type=submit name=type value=\"Submit\">\n";
  print "<input type=hidden name=raw value=\"$mod\">";
  print "<input type=hidden name=\"pattern1\" value=\"$FORM{pattern1}\">";
  print "<input type=hidden name=\"pattern2\" value=\"$FORM{pattern2}\">";
  print "<input type=hidden name=\"pattern3\" value=\"$FORM{pattern3}\">";
  print "<input type=hidden name=\"mt\" value=$mt>";
  print "<input type=hidden name=\"basic\" value=$FORM{basic}>\n";
  print "<input type=hidden name=\"font\" value=$FORM{font}>\n";
  print "<input type=hidden name=\"user\" value=\"$login\">\n";
  print "</form>\n";


  print "</body>\n";
  print "</html>\n";
  exit;
}


## Display Comics-to-Modify List -----------------------------------------------------

print "$banner";

## Set Arrays for sorting
$init = 1;
if ($type eq 'group') { $init = 0; }
for ($ele = $init; $ele <= 13; $ele++) {
  if ($w[$ele] ne '') {

    $field_names = $field_names . $name[$w[$ele]] . ' (' . $o[$w[$ele]] . ')' . ', '; 

    push(@sort_order,$w[$ele]);          # pattern2 value="|0|2|1|3|10|11|9|8|7|6|5|"
    push(@dec_order,$o[$w[$ele]]);       # pattern3 value="D|D|D|D|D|D|D|D|D|D|D|D|"
  }
}
chop $field_names; chop $field_names; 
if (length($field_names) < 2) {
  $field_names = 'unsorted';
}

$mmt = ucfirst("$mt");
print "<b>Collection</b> \"<i>$login</i>\".&nbsp;&nbsp;&nbsp;&nbsp; <b>Matching $mmt</b><br>\n";
print "<ol>";
if ($z[0] ne '') {    print "<li><b>Title = </b>$z[0]<br>\n"; }
if ($z[2] ne '') {    print "<li><b>Publisher = </b>$z[2]<br>\n"; }
if ($z[1] ne '') {    print "<li><b>Volume = </b>$z[1]<br>\n"; }
if ($z[12] ne '') {   print "<li><b>Issue Type = </b>$z[12]<br>\n"; }
if ($z[3] ne '') {    print "<li><b>Issue = </b>$z[3]<br>\n"; }
if ($z[10] ne '') {   print "<li><b>Month = </b>$z[10]<br>\n"; }
if ($z[11] ne '') {   print "<li><b>Year = </b>$z[11]<br>\n"; }
if ($z[9] ne '') {    print "<li><b>Quantity = </b>$z[9]<br>\n"; }
if ($z[8] ne '') {    print "<li><b>Value = </b>$z[8]<br>\n"; }
if ($z[7] ne '') {    print "<li><b>Condition = </b>$z[7]<br>\n"; }
if ($z[6] ne '') {    print "<li><b>Writer = </b>$z[6]<br>\n"; }
if ($z[5] ne '') {    print "<li><b>Artist = </b>$z[5]<br>\n"; }
if ($z[4] ne '') {    print "<li><b>Comments = </b>$z[4]<br>\n"; }
print "</ol>";
print "<b>Sorted by:</b> $field_names <br><br>\n";
foreach $note (@msg) {
  print "$note";
}

## Recontruct match strings for group/add form
for ($idx = 0; $idx <= 12; $idx++) {
  $str1 = $str1 . $z[$idx] . '|';
  $str2 = $str2 . $w[$idx] . '|';
  $str3 = $str3 . $o[$idx] . '|';
}

## Print the match list
@sorted_comics = sort Sorter @comics;
foreach $book (@sorted_comics) {
  @t = split (/\|/, $book);

  $tmp = $book;
  $tmp =~ s/ /\&nbsp;/g;
  @tp = split (/\|/,$tmp);

  ## Group  # pattern1 value="st|1|m|1|[a-z]|a|a|nm|.0|1|1|9|"
  if ($group =~ /^[GAXD]$/ || $type eq 'Submit' || $type eq 'Delete' || $type eq 'More') {
    $match = &Matcher();
  }
  else {
    ## Add, mod, initial
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
  }

  if ($match eq 'T') {

    if ($hits != $l_cnt) {
      $count++;
    }

    if ($count == 1) {

      ## RADIO METHOD      
      print "<form method=POST action=\"$script\">";
      print "<table width=100% border=0>\n";
      print "<tr align=left bgcolor=black id=ID_Style_1>\n";
      print "<th>\n";
      print "<th>Title\n";
      print "<th>Publisher\n";
      print "<th>Vol\n";
      print "<th>Issue\n";
      print "<th>Date\n";
      print "<th>Qnt\n";
      print "<th>Value\n";
      print "<th>Cond\n";
      print "<th>Writer\n";
      print "<th>Artist\n";
      print "<th>Comments\n";
    }

    if ($count >= $s_cnt && $count <= $e_cnt) {
        $hits++;
      if ($hits != ($l_cnt + 1)) {
        if ($color == 0) { print "<tr bgcolor=#D0FFD0>\n"; } else { print "<tr bgcolor=#F8F8F8>\n"; }
        print "<td><input type=\"radio\" name=raw value=\"$book\">\n";

        if ($t[0] eq '') { print "<td>&nbsp;\n"; } else { print "<td>$tp[0]\n"; }
        if ($t[2] eq '') { print "<td>&nbsp;\n"; } else { print "<td>$tp[2]\n"; }
        if ($t[1] eq '') { print "<td>&nbsp;\n"; } else { print "<td>$tp[1]\n"; }

        if ($t[3] eq '' && $t[12] eq '') { print "<td>&nbsp;\n"; } 
        else { if ($tp[3] eq '' && $tp[12] ne '') { print "<td>$tp[12]"; }
               else                               { print "<td>$tp[3]&nbsp;$tp[12]"; } }

        if ($t[10] eq '' && $t[11] eq '') { print "<td>&nbsp;\n"; } 
        else { if ($tp[10] eq '' && $tp[11] ne '') { print "<td align=right>$tp[11]"; }
               else                                { print "<td>$tp[10]&nbsp;$tp[11]"; } }

        if ($t[9] eq '') { print "<td>&nbsp;\n"; } else { print "<td>$tp[9]\n"; }
        if ($t[8] eq '') { print "<td>&nbsp;\n"; } else { print "<td>$tp[8]\n"; }
        if ($t[7] eq '') { print "<td>&nbsp;\n"; } else { print "<td>$tp[7]\n"; }

        print "<td>\n";
        if ($t[6] eq '') { print "&nbsp;"; }
        @writers = split(/\+/,$tp[6]);
        foreach $writer (sort @writers) {
          print "$writer<br>\n";
        }

        print "<td>\n";
        if ($t[5] eq '') { print "&nbsp;"; }
        @artists = split(/\+/,$tp[5]);
        foreach $artist (sort @artists) {
          print "$artist<br>\n";
        }

        if ($t[4] eq '') { print "<td>&nbsp;\n"; } else { print "<td>$tp[4]\n"; }
 
        $color++;
        if ($color == 2) {
          $color = 0;
        }
      }
    }
  }
  ##### Break out of matching when limit is reached
  if ($hits == ($l_cnt + 1)) {    # one past the limit  
     $extra = 1;
    last;
  }
}

print "</table>\n\n";

if ($count != 0) {

  print "<input type=hidden name=\"pattern1\" value=\"$str1\">\n";
  print "<input type=hidden name=\"pattern2\" value=\"$str2\">\n";
  print "<input type=hidden name=\"pattern3\" value=\"$str3\">\n";
  print "<input type=hidden name=\"mt\" value=$mt>\n";
  print "<input type=hidden name=\"basic\" value=$FORM{basic}>\n";
  print "<input type=hidden name=\"font\" value=$FORM{font}>\n";
  print "<input type=hidden name=\"user\" value=\"$login\">\n";
  print "<br><input type=\"submit\" name=\"type\" value=\"Modify\">\n";
  print "<input type=\"submit\" name=\"type\" value=\"Delete\">\n";

  if ($hits >= $l_cnt && $extra != 0) {
    print "<center><b>Viewing Matches $s_cnt - $e_cnt </b> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<input type=hidden name=\"count\" value=\"$count\">";
    print "<input type=submit name=\"type\" value=\"More\"></center><br>\n";
  }
  else {
    if ($FORM{'count'} eq '' && $hits == 1) {
      print "<center><b>$hits Total Match<b></center><br>\n";
    }
    elsif ($FORM{'count'} eq '' && $hits > 1) {
      print "<center><b>$hits Total Matches<b></center><br>\n";
    }
    elsif ($FORM{'count'} ne '' && $hits == 1) {
      $hits = $hits + $FORM{'count'};
      print "<center><b>$hits Total Match<b></center><br>\n";
    }
    elsif ($FORM{'count'} ne '' && $hits > 1) {
      $hits = $hits + $FORM{'count'};
      print "<center><b>$hits Total Matches<b></center><br>\n";
    }
  }

  print "</form>\n";
}

if ($FORM{basic} eq 'Y') {
  &Basic_Form($str1, $str2, $str3, $mt); 
}
else {
  &Group_Form($str1, $str2, $str3, $mt); 
}

print "</body>\n";
print "</html>\n";

exit;


sub Sorter { 
  @first = split( '\|', $a ); 
  @second = split( '\|', $b ); 

  # @sort_order = (10,3);      # comic fields (month, issue) in order of weight (ie: 1,2)
  # @dec_order  = ('A','D');   # respective comic field's ascending/descending flag

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

sub ReadData {
  ## Read Database: 2000 A.D.|2|Eagle|1|6 issue series|Smith, Ron|Wagner, John|NM|2.00|1||
  open(S1,"$comic_data_path");
  while (<S1>) {
    chomp;
      
    ## fresh read of collection data
    push (@comics,$_);
    
    @r = split(/\|/);
    $exist{"$r[0]|$r[1]|$r[2]|$r[3]|$r[12]"} = '';

    ## data for drop-down lists
    $h_tit{$r[0]} = "";
    $h_vol{$r[1]} = "";
    $h_pub{$r[2]} = "";
    $h_iss{$r[3]} = "";
    $h_com{$r[4]} = "";
    $h_art{$r[5]} = "";
    $h_wri{$r[6]} = "";
    $h_con{$r[7]} = "";
    $h_val{$r[8]} = "";
    $h_qua{$r[9]} = "";
    $h_mon{$r[10]} = "";
    $h_yea{$r[11]} = "";
    $h_typ{$r[12]} = "";
  }
  close(S1);

  ## force all first drop-down entries to blanks
  $null = '';
  $h_tit{$null} = "";
  $h_vol{$null} = "";
  $h_pub{$null} = "";
  $h_iss{$null} = "";
  $h_com{$null} = "";
  $h_art{$null} = "";
  $h_wri{$null} = "";
  $h_con{$null} = "";
  $h_val{$null} = "";
  $h_qua{$null} = "";
  $h_mon{$null} = "";
  $h_yea{$null} = "";
  $h_typ{$null} = "";
}

sub Basic_Form {

  $org = $_[0];
  $w   = $_[1];
  $o   = $_[2];
  $mt  = $_[3];

  foreach $ele (@sorted_comics) {
    @r = split(/\|/,$ele);
    $h_tit{$r[0]} = "";
    $h_vol{$r[1]} = "";
    $h_pub{$r[2]} = "";
    $h_iss{$r[3]} = "";
    $h_com{$r[4]} = "";
    $h_art{$r[5]} = "";
    $h_wri{$r[6]} = "";
    $h_con{$r[7]} = "";
    $h_val{$r[8]} = "";
    $h_qua{$r[9]} = "";
    $h_mon{$r[10]} = "";
    $h_yea{$r[11]} = "";
    $h_typ{$r[12]} = "";
  }

  print "<hr>\n";
  print "<center>\n";

  print "<form method=POST action=\"$script\">\n";
  print "<h3><input type=\"radio\" name=gu value=A checked> <b>Add One | </b>\n";
  print "<input type=\"radio\" name=gu value=G> <b>Modify Group</b> | \n";
  print "<input type=\"radio\" name=gu value=X> <b>Add Group</b> | \n";  
  print "<input type=\"radio\" name=gu value=D> <b>Delete Group</b></h3>\n";

  print "<input type=submit value=\"Update\"><br>\n";
  
  print "<input type=hidden name=\"pattern1\" value=\"$org\">";
  print "<input type=hidden name=\"pattern2\" value=\"$w\">";
  print "<input type=hidden name=\"pattern3\" value=\"$o\">";
  print "<input type=hidden name=\"mt\" value=\"$mt\">";
  print "<input type=hidden name=\"basic\" value=$FORM{basic}>\n";
  print "<input type=hidden name=\"font\" value=$FORM{font}>\n";
  print "<input type=hidden name=\"user\" value=\"$login\">\n";

  print "<table border=0 id=ID_Style_2>\n";
  
  print "<tr>\n";
  print "<th align=left>";
  print "<th align=left>\n";
  
  print "<tr>\n";
  print "<th align=left>Title:\n";
  print "<th align=left>";
  print "<input type=\"text\" name=title size=40 maxlength=50>\n";

  print "<tr>\n";
  print "<th align=left>Publisher:\n";
  print "<th align=left>";
  print "<input type=\"text\" name=publisher size=40 maxlength=40>\n";
  
  print "<tr>\n";
  print "<th align=left>Volume:\n";
  print "<th align=left><input type=\"text\" name=volume size=2 maxlength=2>\n";

  print "<tr>\n";
  print "<th align=left>Issue Type:\n";
  print "<th align=left>";
  print "<input type=\"text\" name=itype size=9 maxlength=9>\n";

  print "<tr>\n";
  print "<th align=left>Issue:\n";
  print "<th align=left>";
  print "<input type=\"text\" name=issue size=6 maxlength=6>\n";

  print "<tr>\n";
  print "<th align=left>Month:\n";
  print "<th align=left><input type=\"text\" name=month size=2 maxlength=2>\n";

  print "<tr>\n";
  print "<th align=left>Year:\n";
  print "<th align=left><input type=\"text\" name=year size=4 maxlength=4>\n";

  print "<tr>\n";
  print "<th align=left>Quantity:\n";
  print "<th align=left><input type=\"text\" name=quantity size=3 maxlength=3>\n";

  print "<tr>\n";
  print "<th align=left>Value:\n";
  print "<th align=left><input type=\"text\" name=value size=6 maxlength=6>\n";

  print "<tr>\n";
  print "<th align=left>Condtion:\n";
  print "<th align=left><input type=\"text\" name=condition size=2 maxlength=2>\n";

  print "<tr>\n";
  print "<td align=left><b>Writer:</b> \n";
  print "<td align=left>";
  print "<input type=\"text\" name=writer size=24 maxlength=60>\n";
  
  print "<tr>\n";
  print "<td align=left><b>Artist:</b> \n";
  print "<td align=left>";
  print "<input type=\"text\" name=artist size=24 maxlength=60>\n";
  
  print "<tr>\n";
  print "<td align=left><b>Comments:</b> \n";
  print "<td align=left>";
  print "<input type=\"text\" name=comments size=40 maxlength=60>\n";

  print "<tr>\n";
  print "<td align=center colspan=3><b>Modify/Add Group:</b> Issue Start <input type=\"text\" name=gi size=4 maxlength=3> \n"; 
  print "Issue End <input type=\"text\" name=ge size=4 maxlength=3> \n";
  print "Month Start <input type=\"text\" name=gm size=3 maxlength=2> \n";
  print "Year Start <input type=\"text\" name=gy size=5 maxlength=4> \n";

  print "</table>\n";
  print "</form>\n";
  print "</center>\n";

  return();
} 

sub Group_Form {

  $org = $_[0];
  $w   = $_[1];
  $o   = $_[2];
  $mt  = $_[3];

  foreach $ele (@sorted_comics) {
    @r = split(/\|/,$ele);
    $h_tit{$r[0]} = "";
    $h_vol{$r[1]} = "";
    $h_pub{$r[2]} = "";
    $h_iss{$r[3]} = "";
    $h_com{$r[4]} = "";
    $h_art{$r[5]} = "";
    $h_wri{$r[6]} = "";
    $h_con{$r[7]} = "";
    $h_val{$r[8]} = "";
    $h_qua{$r[9]} = "";
    $h_mon{$r[10]} = "";
    $h_yea{$r[11]} = "";
    $h_typ{$r[12]} = "";
  }

  $null = '';
  $h_tit{$null} = "";
  $h_vol{$null} = "";
  $h_pub{$null} = "";
  $h_iss{$null} = "";
  $h_com{$null} = "";
  $h_art{$null} = "";
  $h_wri{$null} = "";
  $h_con{$null} = "";
  $h_val{$null} = "";
  $h_qua{$null} = "";
  $h_mon{$null} = "";
  $h_yea{$null} = "";
  $h_typ{$null} = "";

  print "<hr>\n";
  print "<center>\n";

  print "<form method=POST action=\"$script\">\n";
  print "<h3><input type=\"radio\" name=gu value=A checked> <b>Add One | </b>\n";
  print "<input type=\"radio\" name=gu value=G> <b>Modify Group</b> | \n";
  print "<input type=\"radio\" name=gu value=X> <b>Add Group</b> | \n";  
  print "<input type=\"radio\" name=gu value=D> <b>Delete Group</b></h3>\n";

  print "<input type=submit value=\"Update\"><br>\n";
  
  print "<input type=hidden name=\"pattern1\" value=\"$org\">";
  print "<input type=hidden name=\"pattern2\" value=\"$w\">";
  print "<input type=hidden name=\"pattern3\" value=\"$o\">";
  print "<input type=hidden name=\"basic\" value=$FORM{basic}>\n";
  print "<input type=hidden name=\"font\" value=$FORM{font}>\n";
  print "<input type=hidden name=\"mt\" value=\"$mt\">";
  print "<input type=hidden name=\"user\" value=\"$login\">\n";

  print "<table border=0 id=ID_Style_2>\n";
  
  print "<tr>\n";
  print "<th align=left>";
  print "<th align=left>";
  print "<th align=left>\n";
  
  print "<tr>\n";
  print "<th align=left>Title:\n";
  print "<th align=left>";
  print "<input type=\"text\" name=title size=40 maxlength=50>\n";
  print "<th align=left><select name=\"title2\">\n";
  foreach $el (sort keys(%h_tit)) {
    print "<option>$el\n";
  }
  print "</select>\n";

  print "<tr>\n";
  print "<th align=left>Publisher:\n";
  print "<th align=left>";
  print "<input type=\"text\" name=publisher size=40 maxlength=40>\n";
  print "<th align=left><select name=\"publisher2\">\n";
  foreach $el (sort keys(%h_pub)) {
    print "<option>$el\n";
  }
  print "</select>\n";
  
  print "<tr>\n";
  print "<th align=left>Volume:\n";
  print "<th align=left><input type=\"text\" name=volume size=2 maxlength=2>\n";
  print "<th align=left><select name=\"volume2\">\n";
  foreach $el (sort {$a <=> $b} keys(%h_vol)) {
    print "<option>$el\n";
  }
  print "</select>\n";

  print "<tr>\n";
  print "<th align=left>Issue Type:\n";
  print "<th align=left>";
  print "<input type=\"text\" name=itype size=9 maxlength=9>\n";
  print "<th align=left><select name=\"itype2\">\n";
  foreach $el (sort keys(%h_typ)) {
    print "<option>$el\n";
  }
  print "</select>\n";  

  print "<tr>\n";
  print "<th align=left>Issue:\n";
  print "<th align=left>";
  print "<input type=\"text\" name=issue size=12 maxlength=12>\n";
  print "<th align=left><select name=\"issue2\">\n";
  foreach $el (sort {$a <=> $b} keys(%h_iss)) {
    print "<option>$el\n";
  }
  print "</select>\n";  

  print "<tr>\n";
  print "<th align=left>Month:\n";
  print "<th align=left><input type=\"text\" name=month size=2 maxlength=2>\n";
  print "<th align=left><select name=\"month2\">\n";
  foreach $el (sort {$a <=> $b} keys(%h_mon)) {
    print "<option>$el\n";
  }
  print "</select>\n";

  print "<tr>\n";
  print "<th align=left>Year:\n";
  print "<th align=left><input type=\"text\" name=year size=4 maxlength=4>\n";
  print "<th align=left><select name=\"year2\">\n";
  foreach $el (sort {$a <=> $b} keys(%h_yea)) {
    print "<option>$el\n";
  }
  print "</select>\n";

  print "<tr>\n";
  print "<th align=left>Quantity:\n";
  print "<th align=left><input type=\"text\" name=quantity size=3 maxlength=3>\n";
  print "<th align=left><select name=\"quantity2\">\n";
  foreach $el (sort {$a <=> $b} keys(%h_qua)) {
    print "<option>$el\n";
  }
  print "</select>\n";

  print "<tr>\n";
  print "<th align=left>Value:\n";
  print "<th align=left><input type=\"text\" name=value size=6 maxlength=6>\n";
  print "<th align=left><select name=\"value2\">\n";
  foreach $el (sort {$a <=> $b} keys(%h_val)) {
    print "<option>$el\n";
  }
  print "</select>\n";
  print "<tr>\n";
  print "<th align=left>Condtion:\n";
  print "<th align=left><input type=\"text\" name=condition size=2 maxlength=2>\n";
  print "<th align=left><select name=\"condition2\">\n";
  foreach $el (sort keys(%h_con)) {
    print "<option>$el\n";
  }
  print "</select>\n";

  print "<tr>\n";
  print "<td align=left><b>Writer:</b> \n";
  print "<td align=left>";
  print "<input type=\"text\" name=writer size=24 maxlength=60>\n";
  print "<td align=left><select name=\"writer2\">\n";
  foreach $el (sort keys(%h_wri)) {
    print "<option>$el\n";
  }
  print "</select>\n";
  
  print "<tr>\n";
  print "<td align=left><b>Artist:</b> \n";
  print "<td align=left>";
  print "<input type=\"text\" name=artist size=24 maxlength=60>\n";
  print "<td align=left><select name=\"artist2\">\n";
  foreach $el (sort keys(%h_art)) {
    print "<option>$el\n";
  }
  print "</select>\n";
  
  print "<tr>\n";
  print "<td align=left><b>Comments:</b> \n";
  print "<td align=left>";
  print "<input type=\"text\" name=comments size=40 maxlength=60>\n";
  print "<td align=left><select name=\"comments2\">\n";
  foreach $el (sort keys(%h_com)) {
    print "<option>$el\n";
  }
  print "</select>\n";  

  print "<tr>\n";
  print "<td align=center colspan=3><b>Modify/Add Group:</b> Issue Start <input type=\"text\" name=gi size=4 maxlength=3> \n"; 
  print "Issue End <input type=\"text\" name=ge size=4 maxlength=3> \n";
  print "Month Start <input type=\"text\" name=gm size=3 maxlength=2> \n";
  print "Year Start <input type=\"text\" name=gy size=5 maxlength=4> \n";

  print "</table>\n";
  print "</form>\n";
  print "</center>\n";

  return();
} 

sub RegExp {
  $handle = $_[0];

  $handle =~ s/\./\\\./g;     ## '.' (period) matches are allowed
  $handle =~ s/\(/\\(/g;      ## '(' matches are allowed
  $handle =~ s/\)/\\)/g;      ## ')' matches are allowed

  $handle =~ s/ or /\|/g;    ## ' or ' allows alternate matches
  $handle =~ s/{/^/g;        ## '{' is a leftmost boundary
  $handle =~ s/}/\$/g;       ## '}' is a rightmost boundary
  $handle =~ s/\?/./g;       ## '?' is a one-character wildcard
  $handle =~ s/\*/.*/g;      ## '*' is a one-or-many wildcard
  return($handle);
}

sub Matcher {
  if ($mt eq 'all') {
    $match = 'T';                       ## ALL Field by Field Fixed Reg Exp Matching
    for ($fi = 0; $fi <= 12; $fi++) {
      if ($x[$fi] ne '') {
        if (!($t[$fi] =~ m/$x[$fi]/i)) {
          $match = 'F';
        }
      }
    }
  }
  else {
    $match = 'F';                       ## ANY  Field by Field Fixed Reg Exp Matching
    for ($fi = 0; $fi <= 12; $fi++) {
      if ($x[$fi] ne '') {
        if ($t[$fi] =~ m/$x[$fi]/i) {
          $match = 'T';
        }
      }
    }
  }
  return($match);
}

sub Validate {

  @v = split(/\|/,$_[0]);

  if ($v[0] =~ m/[a-zA-Z0-9]+?/) {  }  
  else {
    $bad = 'T';
    push (@err,"<b>Title</b> is required<br>\n");
  }
  if ($v[1] =~ m/(^[0-9]$)|(^[0-9][0-9]$)/) {  }
  else {
    $bad = 'T';
    push (@err,"<b>Volume</b> is required<br>\n");
  } 
  if ($v[2] =~ m/[a-zA-Z0-9]+?/) {  }
  else {
    $bad = 'T';
    push (@err,"<b>Publisher</b> is required<br>\n");
  } 
  if ($v[3] =~ m/^([0-9]{1,3})$/ || ($v[3] eq '' && $v[12] ne '')) {  }
  else {
    $bad = 'T';
    push (@err,"<b>Issue</b> is required<br>\n");
  }
  @artists = split(/\+/,$v[5]);
  foreach $artist (sort @artists) { 
    if ($artist eq '' || $artist =~ m/[a-z], [A-Z]/) {  }
    else {
      $bad = 'T';
      push (@err,"<b>Artist</b> is invalid (format: Last_name1, First_name1+Last_name2, First_name2+...)<br>\n");
      last;
    }
  } 
  @writers = split(/\+/,$v[6]);
  foreach $writer (sort @writers) {
    if ($writer eq '' || $writer =~ m/[a-z], [A-Z]/) {  }
    else {
      $bad = 'T';
      push (@err,"<b>Writer</b> is invalid (format: Last_name1, First_name1+Last_name2, First_name2+...)<br>\n");
      last;
    } 
  }
  if ($v[7] =~ m/^[A-Z][A-Z]$/) {  }
  else {
    $bad = 'T';
    push (@err,"<b>Condition</b> is invalid (format: XX where X is any capital letter)<br>\n");
  } 
  if ($v[8] =~ m/^[0-9]+?\.[0-9][0-9]$/) {  }
  else {
    $bad = 'T';
    push (@err,"<b>Value</b> is invalid (format: X.XX where X is any number)<br>\n");
  }
  if ($v[9] =~ m/^[0-9]{1,2}$/) {  }
  else {
    $bad = 'T';
    push (@err,"<b>Quantity</b> is invalid (format: X or XX where X is any number)<br>\n");
  }
  if ($v[10] eq '' || $v[10] =~ m/^([0][1-9])|([1][0-2])$/) {  }
  else {
    $bad = 'T';
    push (@err,"<b>Month</b> is invalid (format: 01 to 12, or blank)<br>\n");
  }
  if ($v[11] =~ m/^[0-9]{4}$/) {  }
  else {
    $bad = 'T';
    push (@err,"<b>Year</b> is invalid (format: XXXX where X is any number)<br>\n");
  }

  if ($bad eq 'T') {
    print "<h2>Validation Errors - Go Back and complete the Form</h2>\n";
    print "<ol>\n";
    foreach $e_msg (@err) {
      print "<li>$e_msg";
    }
    print "</ol></body>\n";
    print "</html>\n";
    exit;
  }
  return();
}

sub Stop {

print "Content-Type: text/html\n\n";
print "<html>\n";
print "<head>\n";
print "<title>Online Comic Book Database</title>\n";
print "</head>\n";
print "<body BGCOLOR=\"FFFFFF\" TEXT=\"000000\" LINK=\"FF0080\" VLINK=\"FF8080\" ALINK=\"FF0000\">\n";

print "<center>\n";
print "<IMG SRC=\"http://www.eskimo.com/~home/comics/c_images/Image139.jpg\"><br>\n";
print "<font size=2pt color=lightblue>&#169; 1998-2001 SCE</font>\n";
print "<form method=POST action=\"http://www.eskimo.com/~home/cgi-bin/comic_login.cgi\">\n";
print "<br><br><br><br>\n";
print "<table border=1>\n";
print "<tr>\n";
print "  <td><font size=4pt face=\"comic sans ms\" color=purple>Login </font>\n";
print "  <td><input type=text name=login size=8>\n";
print "<tr>\n";
print "  <td><font size=4pt face=\"comic sans ms\" color=purple>Password </font>\n";
print "  <td><input type=password name=passwd size=8>\n";
print "</table>\n";

print "<br><input type=submit value=Submit>\n";
print "</form>\n";

print "</center>\n";

print "</body>\n";
print "</html>\n";
exit;

  return();
}
