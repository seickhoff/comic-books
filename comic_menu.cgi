#!"C:\xampp\perl\bin\perl.exe"
$web_path      = 'http://localhost/comic-books';
$script_main   = 'http://localhost/comic-books/comic_main.cgi';
$script_report = 'http://localhost/comic-books/comic_report.cgi';
$script_menu   = 'http://localhost/comic-books/comic_menu.cgi';
$help          = 'help.html';
$comic_data_path = '.';

#!/usr/bin/perl
#$web_path        = 'http://www.eskimo.com/~home/comics';
#$script_main     = 'http://www.eskimo.com/~home/cgi-bin/comic_main.cgi';
#$script_report   = 'http://www.eskimo.com/~home/cgi-bin/comic_report.cgi';
#$script_menu     = 'http://www.eskimo.com/~home/cgi-bin/comic_menu.cgi';
#$help            = 'help.htm';
#$comic_data_path = '../comics';

$help_file = $web_path . '/' . $help;

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

if ($FORM{back} ne '') {
  $login = $FORM{back};
}
elsif ($FORM{report} ne '') {
  $login = $FORM{report};
}
elsif ($FORM{main} ne '') {
  $login = $FORM{main};
}
else {
  $login = $FORM{help};
}

$banner .= "<center><hr>";
$banner .= "<table noborder cellpadding=10>";
$banner .= "<tr>";
$banner .= "<td><form method=POST action=\"$script_menu\"><input type=hidden name=help value=$login><input type=submit value=Help></form>";
$banner .= "<td><form method=POST action=\"$script_menu\"><input type=hidden name=report value=$login><input type=submit value=Report></form>";
$banner .= "<td><form method=POST action=\"$script_menu\"><input type=hidden name=main value=$login><input type=submit value=Maintenance></form>";
$banner .= "<td><form method=POST action=\"$script_menu\"><input type=hidden name=back value=$login><input type=submit value=Backup></form>";
$banner .= "</table><hr></center>";

if ($FORM{back} ne '') {
  $file = $comic_data_path . '/' . '.' . $FORM{back};
  $time = localtime();
  print "Content-Type: text/html\n\n";
  print "$time<br>User <i>$FORM{back}</i><br>\n";
  print "<pre>\n";
  print "<b>TITLE|VOLUME|PUBLISHER|ISSUE|COMMENTS|ARTIST|WRITER|CONDITION|VALUE|QUANTITY|MONTH|YEAR|TYPE</b>\n";
  open (D1,"$file");
  while (<D1>) {
    print "$_";
  }
  close (D1);
  print "</pre>\n";
}
elsif ($FORM{help} ne '') {
  $file = $comic_data_path . '/' . $help;
  print "Content-Type: text/html\n\n";
  open (D1,"$file");
  while (<D1>) {
    print "$_";
  }
  close (D1);
}
elsif ($FORM{report} ne '') {
  &Report();
}
else {
  &Main();
}

exit;



sub Reject {
  print "<center><h2>You're Not a Recognized User</h2></center>\n";
  print "<center><h2>Go Back and Check the Form</h2></center>\n";
}

sub Report {

print<<EOF;
Content-Type: text/html


<html>
<head>
<title>Comic Book Database</title>
</head>
<body BGCOLOR="FFFFFF" TEXT="000000" LINK="FF0080" VLINK="FF8080" ALINK="FF0000">
$banner
<center>
<h2>Report Generation - User <i> $login</i></h3>
<form method=POST action="$script_report">
      <table cellpadding=0 cellspacing=5 border=1>
        <tr>
          <td><table cellpadding=0 cellspacing=5 border=0>
                <tr>

                    <tr>
                        <td>
                        <td align=center><b>Col</b>
                        <td align=center><b>Wght</b>
                        <td align=center><b>Asc</b>
                        <td align=center><b>Dec</b>
                        <td align=center><b> Any </b><input type="radio" name=mt value=any>
                                         <b> All </b><input type="radio" name=mt value=all checked>
                                         &nbsp;&nbsp;&nbsp;<b> Font Size </b><input type="text" name=font size=2 maxlength=2 value=9>

                    <tr>
                        <td><b>Title</b>
                        <td><input type="checkbox" name=ch_0 value="Y" checked>
                        <td><select name="w_0" value=1>
                            <option value=""><option value="1" selected>1<option value="2">2<option value="3">3
                            <option value="4">4<option value="5">5<option value="6">6
                            <option value="7">7<option value="8">8<option value="11">11
                            <option value="10">10<option value="11">11<option value="12">12
                            </select>
                        <td><input type="radio" name=o_0 value=A checked>
                        <td><input type="radio" name=o_0 value=D>
                        <td><input type="text" name=t_0 size=30 maxlength=40>
                    <tr>
                        <td><b>Publisher</b>
                        <td><input type="checkbox" name=ch_2 value="Y" checked>
                        <td><select name="w_2">
                            <option value=""><option value="1">1<option value="2" selected>2<option value="3">3
                            <option value="4">4<option value="5">5<option value="6">6
                            <option value="7">7<option value="8">8<option value="11">11
                            <option value="10">10<option value="11">11<option value="12">12
                            </select>
                        <td><input type="radio" name=o_2 value=A checked>
                        <td><input type="radio" name=o_2 value=D>
                        <td><input type="text" name=t_2 size=30 maxlength=40>
                    <tr>
                        <td><b>Volume</b>
                        <td><input type="checkbox" name=ch_1 value="Y" checked>
                        <td><select name="w_1">
                            <option value=""><option value="1">1<option value="2">2<option value="3" selected>3
                            <option value="4">4<option value="5">5<option value="6">6
                            <option value="7">7<option value="8">8<option value="11">11
                            <option value="10">10<option value="11">11<option value="12">12
                            </select>
                        <td><input type="radio" name=o_1 value=A checked>
                        <td><input type="radio" name=o_1 value=D>
                        <td><input type="text" name=t_1 size=30 maxlength=40>
                    <tr>
                        <td><b>Issue Type</b>
                        <td><input type="checkbox" name=ch_12 value="Y" checked>
                         <td><select name="w_12">
                            <option value=""><option value="1">1<option value="2">2<option value="3">3
                            <option value="4" selected>4<option value="5">5<option value="6">6
                            <option value="7">7<option value="8">8<option value="9">9
                            <option value="10">10<option value="11">11<option value="12">12
                            </select>
                        <td><input type="radio" name=o_12 value=A checked>
                        <td><input type="radio" name=o_12 value=D>
                        <td><input type="text" name=t_12 size=30 maxlength=40> 
                    <tr>
                        <td><b>Issue</b>
                        <td><input type="checkbox" name=ch_3 value="Y" checked>
                         <td><select name="w_3">
                            <option value=""><option value="1">1<option value="2">2<option value="3">3
                            <option value="4">4<option value="5" selected>5<option value="6">6
                            <option value="7">7<option value="8">8<option value="9">9
                            <option value="10">10<option value="11">11<option value="12">12
                            </select>
                        <td><input type="radio" name=o_3 value=A checked>
                        <td><input type="radio" name=o_3 value=D>
                        <td><input type="text" name=t_3 size=30 maxlength=40> 
                    <tr>
                        <td><b>Month</b>
                        <td><input type="checkbox" name=ch_10 value="Y" checked>
                        <td><select name="w_10">
                            <option value=""><option value="1">1<option value="2">2<option value="3">3
                            <option value="4">4<option value="5">5<option value="6">6
                            <option value="7">7<option value="8">8<option value="11">11
                            <option value="10">10<option value="11">11<option value="12">12
                            </select>
                        <td><input type="radio" name=o_10 value=A checked>
                        <td><input type="radio" name=o_10 value=D>
                        <td><input type="text" name=t_10 size=30 maxlength=40>  
                    <tr>
                        <td><b>Year</b>
                        <td><input type="checkbox" name=ch_11 value="Y" checked>
                        <td><select name="w_11">
                            <option value=""><option value="1">1<option value="2">2<option value="3">3
                            <option value="4">4<option value="5">5<option value="6">6
                            <option value="7">7<option value="8">8<option value="9">9
                            <option value="10">10<option value="11">11<option value="12">12
                            </select>
                        <td><input type="radio" name=o_11 value=A checked>
                        <td><input type="radio" name=o_11 value=D>
                        <td><input type="text" name=t_11 size=30 maxlength=40>  
                    <tr>
                        <td><b>Quantity</b>
                        <td><input type="checkbox" name=ch_9 value="Y" checked>
                        <td><select name="w_9">
                            <option value=""><option value="1">1<option value="2">2<option value="3">3
                            <option value="4">4<option value="5">5<option value="6">6
                            <option value="7">7<option value="8">8<option value="9">9
                            <option value="10">10<option value="11">11<option value="12">12
                            </select>
                        <td><input type="radio" name=o_9 value=A checked>
                        <td><input type="radio" name=o_9 value=D>
                        <td><input type="text" name=t_9 size=30 maxlength=40>
                    <tr>
                        <td><b>Value</b>
                        <td><input type="checkbox" name=ch_8 value="Y" checked>
                        <td><select name="w_8">
                            <option value=""><option value="1">1<option value="2">2<option value="3">3
                            <option value="4">4<option value="5">5<option value="6">6
                            <option value="7">7<option value="8">8<option value="9">9
                            <option value="10">10<option value="11">11<option value="12">12
                            </select>
                        <td><input type="radio" name=o_8 value=A checked>
                        <td><input type="radio" name=o_8 value=D>
                        <td><input type="text" name=t_8 size=30 maxlength=40>
                    <tr>
                        <td><b>Condition</b>
                        <td><input type="checkbox" name=ch_7 value="Y" checked>
                        <td><select name="w_7">
                            <option value=""><option value="1">1<option value="2">2<option value="3">3
                            <option value="4">4<option value="5">5<option value="6">6
                            <option value="7">7<option value="8">8<option value="9">9
                            <option value="10">10<option value="11">11<option value="12">12
                            </select>
                        <td><input type="radio" name=o_7 value=A checked>
                        <td><input type="radio" name=o_7 value=D>
                        <td><input type="text" name=t_7 size=30 maxlength=40>
                    <tr>
                        <td><b>Writer</b>
                        <td><input type="checkbox" name=ch_6 value="Y" checked>
                        <td><select name="w_6">
                            <option value=""><option value="1">1<option value="2">2<option value="3">3
                            <option value="4">4<option value="5">5<option value="6">6
                            <option value="7">7<option value="8">8<option value="9">9
                            <option value="10">10<option value="11">11<option value="12">12
                            </select>
                        <td><input type="radio" name=o_6 value=A checked>
                        <td><input type="radio" name=o_6 value=D>
                        <td><input type="text" name=t_6 size=30 maxlength=40>
                    <tr>
                        <td><b>Artist</b>
                        <td><input type="checkbox" name=ch_5 value="Y" checked>
                        <td><select name="w_5">
                            <option value=""><option value="1">1<option value="2">2<option value="3">3
                            <option value="4">4<option value="5">5<option value="6">6
                            <option value="7">7<option value="8">8<option value="9">9
                            <option value="10">10<option value="11">11<option value="12">12
                            </select>
                        <td><input type="radio" name=o_5 value=A checked>
                        <td><input type="radio" name=o_5 value=D>
                        <td><input type="text" name=t_5 size=30 maxlength=40>
                    <tr>
                        <td><b>Comments</b>
                        <td><input type="checkbox" name=ch_4 value="Y" checked>
                        <td><select name="w_4">
                            <option value=""><option value="1">1<option value="2">2<option value="3">3
                            <option value="4">4<option value="5">5<option value="6">6
                            <option value="7">7<option value="8">8<option value="9">9
                            <option value="10">10<option value="11">11<option value="12">12
                            </select>
                        <td><input type="radio" name=o_4 value=A checked>
                        <td><input type="radio" name=o_4 value=D>
                        <td><input type="text" name=t_4 size=30 maxlength=40>
                    <tr><td colspan=6 align=center><b>Overstreet Style:</b> Yes <input type="radio" name=os value=Y checked> No <input type="radio" name=os value=N>&nbsp;&nbsp;&nbsp;&nbsp;
                            <input type="reset" value="Reset Form">
                            <input type="submit" value="Create Report">
                </table>
           </table>
<input type=hidden name="user" value="$login">
</form>

</center>
</body>
</html>
EOF
  return();
}

sub Main {

print<<EOF;
Content-Type: text/html


<html>
<head>
<title>Comic Book Database</title>
</head>
<body IMG BGCOLOR="FFFFFF" TEXT="000000" LINK="FF0080" VLINK="FF8080" ALINK="FF0000">
$banner
<center>
<h2>Collection Maintenance - User <i> $login</i></h2>
<form method=POST action="$script_main">
      <table cellpadding=0 cellspacing=5 border=1>
        <tr>
          <td><table cellpadding=0 cellspacing=5 border=0>
                <tr>
                    <tr>
                        <td align=left><b><u>Field&nbsp;Name</u></b>
                        <td align=center><b><u>Order</u></b>
                        <td align=center><b><u>Asc</u></b>
                        <td align=center><b><u>Dec</u>&nbsp;&nbsp;&nbsp;&nbsp;</b>
                        <td align=center><b>Any&nbsp;<input type="radio" name=mt value=any>
                                         &nbsp;All&nbsp;<input type="radio" name=mt value=all checked>
                                         &nbsp;&nbsp;&nbsp; Font Size </b><input type="text" name=font size=2 maxlength=2 value=9>
                    <tr>
                        <td><b>Title</b>
                        <td><select name="w_0" value=1>
                            <option value=""><option value="1" selected>1<option value="2">2<option value="3">3
                            <option value="4">4<option value="5">5<option value="6">6
                            <option value="7">7<option value="8">8<option value="11">11
                            <option value="10">10<option value="11">11<option value="12">12
                            </select>
                        <td><input type="radio" name=o_0 value=A checked>
                        <td><input type="radio" name=o_0 value=D>
                        <td><input type="text" name=t_0 size=30 maxlength=40>
                    <tr>
                        <td><b>Publisher</b>
                        <td><select name="w_2">
                            <option value=""><option value="1">1<option value="2" selected>2<option value="3">3
                            <option value="4">4<option value="5">5<option value="6">6
                            <option value="7">7<option value="8">8<option value="11">11
                            <option value="10">10<option value="11">11<option value="12">12
                            </select>
                        <td><input type="radio" name=o_2 value=A checked>
                        <td><input type="radio" name=o_2 value=D>
                        <td><input type="text" name=t_2 size=30 maxlength=40>
                    <tr>
                        <td><b>Volume</b>
                        <td><select name="w_1">
                            <option value=""><option value="1">1<option value="2">2<option value="3" selected>3
                            <option value="4">4<option value="5">5<option value="6">6
                            <option value="7">7<option value="8">8<option value="11">11
                            <option value="10">10<option value="11">11<option value="12">12
                            </select>
                        <td><input type="radio" name=o_1 value=A checked>
                        <td><input type="radio" name=o_1 value=D>
                        <td><input type="text" name=t_1 size=30 maxlength=40>
                    <tr>
                        <td><b>Issue&nbsp;Type</b>
                         <td><select name="w_12">
                            <option value=""><option value="1">1<option value="2">2<option value="3">3
                            <option value="4" selected>4<option value="5">5<option value="6">6
                            <option value="7">7<option value="8">8<option value="9">9
                            <option value="10">10<option value="11">11<option value="12">12
                            </select>
                        <td><input type="radio" name=o_12 value=A checked>
                        <td><input type="radio" name=o_12 value=D>
                        <td><input type="text" name=t_12 size=30 maxlength=40> 
                    <tr>
                        <td><b>Issue</b>
                         <td><select name="w_3">
                            <option value=""><option value="1">1<option value="2">2<option value="3">3
                            <option value="4">4<option value="5" selected>5<option value="6">6
                            <option value="7">7<option value="8">8<option value="9">9
                            <option value="10">10<option value="11">11<option value="12">12
                            </select>
                        <td><input type="radio" name=o_3 value=A checked>
                        <td><input type="radio" name=o_3 value=D>
                        <td><input type="text" name=t_3 size=30 maxlength=40> 
                    <tr>
                        <td><b>Month</b>
                        <td><select name="w_10">
                            <option value=""><option value="1">1<option value="2">2<option value="3">3
                            <option value="4">4<option value="5">5<option value="6">6
                            <option value="7">7<option value="8">8<option value="11">11
                            <option value="10">10<option value="11">11<option value="12">12
                            </select>
                        <td><input type="radio" name=o_10 value=A checked>
                        <td><input type="radio" name=o_10 value=D>
                        <td><input type="text" name=t_10 size=30 maxlength=40>  
                    <tr>
                        <td><b>Year</b>
                        <td><select name="w_11">
                            <option value=""><option value="1">1<option value="2">2<option value="3">3
                            <option value="4">4<option value="5">5<option value="6">6
                            <option value="7">7<option value="8">8<option value="9">9
                            <option value="10">10<option value="11">11<option value="12">12
                            </select>
                        <td><input type="radio" name=o_11 value=A checked>
                        <td><input type="radio" name=o_11 value=D>
                        <td><input type="text" name=t_11 size=30 maxlength=40>  
                    <tr>
                        <td><b>Quantity</b>
                        <td><select name="w_9">
                            <option value=""><option value="1">1<option value="2">2<option value="3">3
                            <option value="4">4<option value="5">5<option value="6">6
                            <option value="7">7<option value="8">8<option value="9">9
                            <option value="10">10<option value="11">11<option value="12">12
                            </select>
                        <td><input type="radio" name=o_9 value=A checked>
                        <td><input type="radio" name=o_9 value=D>
                        <td><input type="text" name=t_9 size=30 maxlength=40>
                    <tr>
                        <td><b>Value</b>
                        <td><select name="w_8">
                            <option value=""><option value="1">1<option value="2">2<option value="3">3
                            <option value="4">4<option value="5">5<option value="6">6
                            <option value="7">7<option value="8">8<option value="9">9
                            <option value="10">10<option value="11">11<option value="12">12
                            </select>
                        <td><input type="radio" name=o_8 value=A checked>
                        <td><input type="radio" name=o_8 value=D>
                        <td><input type="text" name=t_8 size=30 maxlength=40>
                    <tr>
                        <td><b>Condition</b>
                        <td><select name="w_7">
                            <option value=""><option value="1">1<option value="2">2<option value="3">3
                            <option value="4">4<option value="5">5<option value="6">6
                            <option value="7">7<option value="8">8<option value="9">9
                            <option value="10">10<option value="11">11<option value="12">12
                            </select>
                        <td><input type="radio" name=o_7 value=A checked>
                        <td><input type="radio" name=o_7 value=D>
                        <td><input type="text" name=t_7 size=30 maxlength=40>
                    <tr>
                        <td><b>Writer</b>
                        <td><select name="w_6">
                            <option value=""><option value="1">1<option value="2">2<option value="3">3
                            <option value="4">4<option value="5">5<option value="6">6
                            <option value="7">7<option value="8">8<option value="9">9
                            <option value="10">10<option value="11">11<option value="12">12
                            </select>
                        <td><input type="radio" name=o_6 value=A checked>
                        <td><input type="radio" name=o_6 value=D>
                        <td><input type="text" name=t_6 size=30 maxlength=40>
                    <tr>
                        <td><b>Artist</b>
                        <td><select name="w_5">
                            <option value=""><option value="1">1<option value="2">2<option value="3">3
                            <option value="4">4<option value="5">5<option value="6">6
                            <option value="7">7<option value="8">8<option value="9">9
                            <option value="10">10<option value="11">11<option value="12">12
                            </select>
                        <td><input type="radio" name=o_5 value=A checked>
                        <td><input type="radio" name=o_5 value=D>
                        <td><input type="text" name=t_5 size=30 maxlength=40>
                    <tr>
                        <td><b>Comments</b>
                        <td><select name="w_4">
                            <option value=""><option value="1">1<option value="2">2<option value="3">3
                            <option value="4">4<option value="5">5<option value="6">6
                            <option value="7">7<option value="8">8<option value="9">9
                            <option value="10">10<option value="11">11<option value="12">12
                            </select>
                        <td><input type="radio" name=o_4 value=A checked>
                        <td><input type="radio" name=o_4 value=D>
                        <td><input type="text" name=t_4 size=30 maxlength=40>
                    <tr><td colspan=2><b>Drop&nbsp;Down&nbsp;Lists</b><br>&nbsp;No <input type="radio" name=basic value=Y> Yes <input type="radio" name=basic value=N checked>&nbsp;&nbsp;&nbsp;&nbsp;
                        <td colspan=3 align=right><input type="reset" value="Reset Form">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<input type="submit" value="Retrieve Data">
                </table>
      </table>
<input type=hidden name="type" value="first">
<input type=hidden name="user" value="$login">
</form>

</center>
</body>
</html>
EOF
  return();
}

